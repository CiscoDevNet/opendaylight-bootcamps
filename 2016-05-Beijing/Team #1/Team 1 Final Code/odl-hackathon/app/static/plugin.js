function bindAll() {
    $('.ajax').UISingle({
        'click': function () {
            var ask = this.attr('ask');
            if (ask && !confirm(ask)) {
                return false;
            }
            var is_modal = this.hasClass('show_modal');
            if (is_modal) {
                $.UIAjax.showDialog('操作提示', '正在等待系统回复，请稍后...', 'wait');
            }
            $.UIAjax.get(this.attr('href'));
            return false;
        }
    });
    $('.delete').UISingle({
        'click': function () {
            if (!confirm("该操作无法恢复，确认删除该数据？")) {
                return false;
            }
            $.UIAjax.get(this.attr('href'));
            return false;
        }
    });
    $('.ui-form').UIForm();
    $('.history').UISingle({
        'click': function () {
            history.back();
            return false;
        }
    });

    $('input[type="checkbox"].icheck, input[type="radio"].icheck').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue'
    });
}
$(document).ready(function () {
    moment.locale('zh-cn');
    bindAll();
    $('body').on('ajaxShowDialog', function () {
        bindAll();
    });
    $('body').on('UITableComplete', function () {
        bindAll();
    });
});