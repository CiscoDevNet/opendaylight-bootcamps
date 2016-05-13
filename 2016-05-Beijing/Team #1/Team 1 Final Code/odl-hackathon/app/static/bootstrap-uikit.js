//common
(function ($) {
    $.fn.UI = {
        uuid: function (number) {
            return new Array(number).join('x').replace(/[xy]/g, function (c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }
    };

    $.fn.serializeJSON = function () {
        var o = {};
        var a = this.serializeArray();
        jQuery.each(a, function (index, li) {
            if (o[li.name]) {
                o[li.name] = o[li.name] + ',' + li.value;
            } else {
                o[li.name] = li.value;
            }
        });
        return o;
    };

    $.extend(String.prototype, {
        format: function () {
            var s = this,
                i = arguments.length;

            while (i--) {
                s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
            }
            return s;
        },
        trim: function () {
            return this.replace(/^\s+|\s+$/g, '');
        },
        isInteger: function () {
            return (new RegExp(/^\d+$/).test(this));
        },
        isNumber: function (value, element) {
            return (new RegExp(/^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/).test(this));
        },
        startsWith: function (pattern) {
            return this.indexOf(pattern) === 0;
        },
        endsWith: function (pattern) {
            var d = this.length - pattern.length;
            return d >= 0 && this.lastIndexOf(pattern) === d;
        },
        replaceAll: function (os, ns) {
            return this.replace(new RegExp(os, 'gm'), ns);
        }
    });

}(jQuery));
//widget
(function ($) {
    $.extend($, {
        UIAjax: {
            get: function (u, data, callback) {
                return this.ajax(u, 'GET', data, callback);
            },
            post: function (u, data, callback) {
                return this.ajax(u, 'POST', data, callback);
            },
            ajax: function (u, method, data, callback) {
                $.ajax({
                    url: u,
                    cache: false,
                    type: method,
                    dataType: 'json',
                    data: data,
                    success: callback || $.proxy(this.standardJson, this)
                });
                return false;
            },
            closeDialog: function () {
                var dialog = $('#append_parent');
                $('.modal').modal('hide');
            },
            showDialog: function (title, content, type) {
                var dialog_header = '<button type="button" class="close" data-dismiss="modal">&times;</button>';
                var dialog_html = '<div class="modal fade" role="dialog" >' +
                    '<div class="modal-dialog">' +
                    '<div class="modal-content">' +
                    '<div class="modal-header">{0}<h4 class="modal-title blue bigger">{1}</h4></div>' +
                    '<div class="modal-body" style="font-size:14px;">{2}</div>{3}</div></div></div>';
                if (type == "wait") {
                    dialog_html = dialog_html.format("", title,
                        '<i class="icon-spinner icon-spin green bigger-125"></i>' + content, "");
                } else if (type == "error") {
                    dialog_html = dialog_html.format(dialog_header, title,
                        '<i class="icon-bolt red bigger-125"></i>&nbsp;&nbsp;' + content, "");
                } else {
                    var footer = '<div class="modal-footer">' +
                        '<button type="button" class="btn btn-primary" onclick="window.location.reload();">确定</button></div>';
                    dialog_html = dialog_html.format(dialog_header, title, '<i class="icon-ok green bigger-125"></i>' + content, footer);
                }
                this.boxShow(dialog_html);
            },
            boxShow: function (innerHTML, height, width) {
                var dialog = $('#append_parent');
                dialog.html(innerHTML);
                //$('.modal').css('margin-top', '10px');
                if (width) {
                    $('.modal').css('width', width);
                    $('.modal').css('margin-left', function () {
                        return -($(this).width() / 2);
                    });
                }
                if (height) {
                    $('.modal-body').css('max-height', height);
                }
                $('.modal').modal({keyboard: true, show: true});
                $('.modal').on('hidden.bs.modal', function (e) {
                    dialog.html('');
                });
                return true;
            },
            standardJson: function (r) {
                var type = r['type'];
                var data = r['data'];
                var success = r['success'];
                if (type == 'alert') {
                    alert(data);
                } else if (type == 'toastr') {
                    $.UIAjax.closeDialog();
                    toastr.options = {
                        closeButton: true,
                        progressBar: true,
                        showMethod: 'slideDown',
                        timeOut: 4000,
                        onHidden: function () {
                            window.location.reload();
                        }
                    };
                    if (success) {
                        toastr.success(data, '操作结果');
                    } else {
                        toastr.error(data, '操作结果');
                    }
                } else if (type == 'refresh') {
                    if (data) {
                        $.UIAjax.showDialog(data.title, data.message, data.type);
                        //重新加载当前页面
                        $('.modal').on('hidden.bs.modal', function () {
                            window.location.reload();
                        });
                        return;
                    }
                    window.location.reload();
                } else if (type == 'updater') {
                    jQuery('#append_parent').html(data);
                } else if (type == 'dialog') {
                    var width = data['width'] || 0;
                    var height = data['height'] || 0;
                    var html = data['html'] || '';
                    this.boxShow(html, height, width);
                    var e = jQuery.Event('ajaxShowDialog');
                    jQuery('body').trigger(e);
                } else if (type == 'redirect') {
                    window.location.href = data;
                } else if (type == 'data') {
                    if (data) {
                        eval(data);
                    }
                }
            }
        }
    });

    var UISingle = function (element, options) {
        this.$this = $(element);
        this.onClick(options.click)
    };

    UISingle.prototype.onClick = function (func) {
        this.$this.click($.proxy(func, this.$this));
    };

    $.fn.UISingle = function (options) {
        var t = options;
        return this.map(function () {
            var $this = $(this);
            var data = $this.data('ui.single');
            if (!data) $this.data('ui.single', (data = new UISingle(this, t)));
            return data;
        });
    };

    var UIForm = function (element, options) {
        this.$this = $(element);
        this.$this.bind('submit', $.proxy(this.submit, this));
        this.id = this.$this.attr('id') == undefined ? 'from_' + $.fn.UI.uuid(5) : this.$this.attr('id'); //随机生成id
        this.$this.attr('id', this.id);
        this.options = options || {
                layout: {
                    auto: true,
                    label: 'col-md-3',
                    input: 'col-md-6',
                    button: 'col-md-offset-2 col-md-10'
                },
                validate: {}
            };
        this.validateOption = $.extend({
            highlight: function (element) {
                $(element).closest('.form-group').addClass('has-error');
            },
            unhighlight: function (element) {
                $(element).closest('.form-group').removeClass('has-error');
            },
            errorElement: 'div',
            errorClass: 'help-block col-sm-3',
            errorPlacement: function (error, element) {
                if (element.parents('.control-input').length) {
                    error.insertAfter(element.parents('.control-input')[0]);
                } else {
                    error.insertAfter(element);
                }
            }
        }, this.options.validate);

        //添加必填输入标志
        $('.control-label', $('.required', this.$this).closest('.form-group')).append('<span style="color:red">*</span>');
        //自动布局
        if (this.options.layout.auto) {
            this.autoLayout();
        }
    };

    UIForm.prototype.autoLayout = function () {
        $('.control-label', this.$this).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.hasClass(this.options.layout.label)) {
                $this.addClass(this.options.layout.label);
            }
        }, this));
        $('.control-input', this.$this).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.hasClass(this.options.layout.input)) {
                $this.addClass(this.options.layout.input);
            }
        }, this));
        $('.form-button', this.$this).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.hasClass(this.options.layout.button)) {
                $this.addClass(this.options.layout.button);
            }
        }, this));
    };

    UIForm.prototype.validate = function () {
        this.$this.validate(this.validateOption);
        return this.$this.valid();
    };
    UIForm.prototype.submit = function () {
        //去除空格
        $('input[type=text]',this.$this).each(function(){
            $(this).val($(this).val().trim());
        });
        if (!this.validate()) {
            return false;
        }
        if (this.$this.hasClass('ui-form-ajax')) {
            $.UIAjax.showDialog('操作提示', '正在玩命提交中，请稍后...', 'wait');
            $.UIAjax.post(this.$this.attr('action'), this.$this.serializeJSON());
            return false;
        }
        return true;
    };



    $.fn.UIForm = function (options) {
        var t = options;
        return this.map(function () {
            var $this = $(this);
            var data = $this.data('ui.form');
            if (!data) $this.data('ui.form', (data = new UIForm(this, t)));
            return data;
        })
    };

    var UIMemoryForm = function (element, options) {
        this.$this = $(element);
        this.options = options || {expires: 365};
    };

    UIMemoryForm.prototype.ensureNumber = function (n) {
        n = parseInt(n, 10);
        if (isNaN(n) || n <= 0) {
            n = 0;
        }
        return n;
    };

    UIMemoryForm.prototype.writeToCookie = function () {
        var name = this.$this.attr('name');
        var data = JSON.stringify(this.$this.serializeJSON());
        $.cookie(name, data, {expires: this.options.expires});
    };

    UIMemoryForm.prototype.readFormCookie = function () {
        var name = this.$this.attr('name');
        if (!name) {
            return;
        }
        var data = $.cookie(name);
        if (typeof data === 'undefined') {
            return;
        }
        var self = this.$this;
        JSON.parse(data, function (key, value) {
            if (typeof (value) !== 'object') {
                var el = self.find('*[name="' + key + '"]');

                if (el.is('input')) {
                    if (el.attr('type') === 'number') {
                        el.val(self.ensureNumber(value));
                    } else if (el.attr('type') === 'checkbox') {
                        el.attr('checked', value === 'on');
                    } else if (el.attr('type') === 'radio') {
                        $("input[type='radio'][name='" + key + "'][value='" + value + "']").attr("checked", "checked");
                    } else {
                        el.val(value);
                    }
                } else if (el.is('select')) {
                    el.val(value);
                } else if (el.is('textarea')) {
                    el.val(value);
                }
            }
        });
    };

    $.fn.UIMemoryForm = function (options) {
        var t = options;
        return this.map(function () {
            var $this = $(this);
            var data = $this.data('ui.memory.form');
            if (!data) $this.data('ui.memory.form', (data = new UIMemoryForm(this, t)));
            return data;
        })
    };

    //uitable
    var UITable = function (element, options) {
        this.$this = $(element);
        this.$options = options;
        this.$body = $('.ui-table-body', this.$this);
        this.serverSideUrl = this.$body.data('url');
        this.$searchForm = $('.ui-table-search', this.$this);
        this.$searchFormMemory = $('.ui-table-search', this.$this).UIMemoryForm()[0];
        var $this = this.$this;
        var searchForm = this.$searchForm;
        var searchFormMemory = this.$searchFormMemory;
        var stateSave = this.$body.data('state') == undefined ? true : this.$body.data('state');
        this.$data_key = this.$body.data('key') == undefined ? 'id' : this.$body.data('key');

        if (stateSave && this.$searchFormMemory) {
            this.$searchFormMemory.readFormCookie();
        }

        this.setting = {
            'searching': false,//不使用它的搜索
            'stateSave': stateSave,
            'order': [],//默认不进行任何排序
            'columnDefs': [],
            'columns': [],
            'drawCallback': function () {
                $('.ui-table-delete', $this).click(function () {
                    var ids = '';
                    for (var i = 0; i < api.rows('.selected').data().length; i++) {
                        ids += i + ',';
                    }
                    //哨兵
                    ids += '-1';
                    $.UIAjax.post($(this).attr('href'), {"ids": ids});
                    return false;
                });
                var e = jQuery.Event('UITableComplete');
                jQuery('body').trigger(e);
            },
            'initComplete': function () {
                var api = this.api();
                searchForm.submit(function () {
                    api.ajax.reload();
                    if (stateSave && searchFormMemory) {
                        searchFormMemory.writeToCookie();
                    }
                    return false;
                });
            },
            'language': {
                'buttons.copy': '复制',
                'select': {
                    'rows': {
                        _: '已选中了 %d 行',
                        0: '',
                        1: '已选中了 1 行'
                    }
                },
                'sProcessing': '处理中...',
                'sLengthMenu': '显示 _MENU_ 项结果',
                'sZeroRecords': '没有匹配结果',
                'sInfo': '显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项',
                'sInfoEmpty': '显示第 0 至 0 项结果，共 0 项',
                'sInfoFiltered': '',//'(由 _MAX_ 项结果过滤)',
                'sInfoPostFix': '',
                'sSearch': '搜索:',
                'sUrl': '',
                'sEmptyTable': '表中数据为空',
                'sLoadingRecords': '载入中...',
                'sInfoThousands': ',',
                'oPaginate': {
                    'sFirst': '首页',
                    'sPrevious': '上页',
                    'sNext': '下页',
                    'sLast': '末页'
                },
                'oAria': {
                    'sSortAscending': ': 以升序排列此列',
                    'sSortDescending': ': 以降序排列此列'
                }
            }
        };

        //this.setting['select'] = {'style': 'os'};
        if (this.$body.data('select')) {
            this.setting['select'] = {'style': this.$body.data('select')};
        }
        if (this.$body.data('processing')) {
            this.setting['processing'] = true;
        }
        this.layoutHeader({
            'group': 'col-sm-4',
            'label': 'col-sm-3',
            'input': 'col-sm-9',
            'button': {'col': 'col-sm-12', 'offset': 'col-sm-offset-5'}
        });
        this.layout();
    };

    UITable.prototype.layoutHeader = function (options) {
        $('.form-group', this.$searchForm).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.hasClass('form-button') && !$this.hasClass(options.group)) {
                $this.addClass(options.group);
            }
        }, this));
        $('.control-label', this.$searchForm).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.hasClass(options.label)) {
                $this.addClass(options.label);
            }
        }, this));
        $('.form-control', this.$searchForm).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.parent().hasClass(options.input)) {
                $this.parent().addClass(options.input);
            }
        }, this));
        $('.form-button', this.$searchForm).each($.proxy(function (idx, item) {
            var $this = $(item);
            if (!$this.hasClass(options.button.col)) {
                //$this.addClass(options.button.col);
                $this.css('float','left').css('margin-right','30px');
            }
            var button = $('.btn', $this);
            if (!button.hasClass(options.button.offset)) {
                button.addClass(options.button.offset);
            }
        }, this));
    };

    UITable.prototype.serverLayout = function (options) {
        this.staticLayout(options);
        //ajax请求
        this.setting['serverSide'] = true;
        this.setting['ajax'] = $.proxy(function (data, callback, setting) {
            var postData = {};
            postData['pageNo'] = (data['start'] + data['length']) / data['length'];
            postData['pageSize'] = data['length'];
            if (data['order'] && data['order'].length != 0) {
                var column = data['order'][0]['column'];
                postData['order'] = data['columns'][column]['data'];
                var td = $("[data-field='" + postData['order'] + "']", this.$body);
                postData['order'] = td.data('orderby')|| postData['order'];
                postData['sort'] = data['order'][0]['dir'];
            }
            $.extend(postData, this.$searchForm.serializeJSON());
            $.ajax({
                url: this.serverSideUrl,
                cache: false,
                type: 'POST',
                dataType: 'json',
                data: postData,
                success: $.proxy(function (response) {
                    var dataTablesData = {};
                    if (response.success) {
                        if (response['type'] != 'data') {
                            $.UIAjax.standardJson(response);
                        }
                        dataTablesData['recordsTotal'] = response.data['total'] || 0;
                        dataTablesData['recordsFiltered'] = response.data['total'] || 0;
                        dataTablesData['data'] = [];
                        for (var i = 0; i < (response.data['rows'] || []).length; i++) {
                            var item = response.data['rows'][i];

                            item['DT_RowId'] = 'row_' + item[this.$data_key];
                            item['DT_RowData'] = {'pkey': item[this.$data_key]};
                            dataTablesData['data'].push(item);
                        }
                    } else {
                        dataTablesData['error'] = response.message;
                    }
                    callback(dataTablesData);
                }, this)
            });
        }, this)
    };

    UITable.prototype._renderRow = function (type, $item) {
        if (type == 'html') {
            var html = $item.html();
            this.setting['columns'].push({
                'orderable': false,
                'render': function render(data, type, row, meta) {
                    var copyHtml = html;
                    for (var k in row) {
                        copyHtml = copyHtml.replaceAll('{{' + k + '}}', row[k]);
                    }
                    return copyHtml;
                },
                'data': $item.data('title')
            });
        }
        if (type == 'date') {
            this.setting['columns'].push({
                'orderable': $item.data('sortable') || false,
                'data': $item.data('field'),
                'render': function render(data, type, row, meta) {
                    if ($item.data('now')) {
                        return moment(data).fromNow();
                    }
                    return moment(data).format($item.data('format') || 'YYYY-MM-DD');
                }
            });
        }
        if (type == 'image') {
            this.setting['columns'].push({
                'orderable': $item.data('sortable') || false,
                'data': $item.data('field'),
                'render': function render(data, type, row, meta) {
                    var width = $item.data("image-width") || 35;
                    var height = $item.data("image-height") || 35;
                    return '<div style="text-align: center;"><img  src=' + data + ' width=' + width + ' height=' + height + ' class="img-circle"/></div> ';
                }
            });
        }
    };

    UITable.prototype.staticLayout = function (options) {
        this.$body.addClass('table table-striped table-bordered');
        $('thead th', this.$body).each($.proxy(function (idx, item) {
            var $item = $(item);
            if ($item.data('checkbox')) {
                this.setting['columns'].push({
                    'orderable': false,
                    'className': 'select-checkbox',
                    'render': function render(data, type, row, meta) {
                        return '';
                    },
                    'data': $item.data('field')
                });
            } else if ($item.data("type")) {
                //不同类型使用不同的渲染器
                this._renderRow($item.data("type"), $item);
            } else {
                var def = {
                    'data': $item.data('field'),
                    'orderable': $item.data('sortable') || false
                };
                if ($item.data('render') && typeof window[$item.data('render')] === 'function') {
                    def['render'] = window[$item.data('render')];
                }
                this.setting['columns'].push(def);
            }
        }, this));
    };

    UITable.prototype.layout = function (options) {
        if (this.serverSideUrl) {
            this.serverLayout();
        } else {
            this.staticLayout();
        }
        this.$dataTable = this.$body.dataTable(this.setting);
    };

    UITable.prototype.getSelectedOne = function () {
        return this.$dataTable.api().rows('.selected').data()[0];
    };

    UITable.prototype.getSelectedAll = function () {
        return this.$dataTable.api().rows('.selected').data();
    };

    $.fn.UITable = function (options) {
        var t = options;
        return this.map(function () {
            var $this = $(this);
            var data = $this.data('ui.table');
            if (!data) $this.data('ui.table', (data = new UITable(this, t)));
            return data;
        })
    };
}(jQuery));

