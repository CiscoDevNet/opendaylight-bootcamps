$('.single-demo-wrap a').on('click', function(ev) {
	// just to make sure the page won't scroll to the top
	ev.preventDefault();
});

// Demo 1
$('#master-menu').slightSubmenu();

// Demo 2
$('#master-menu-horizontal-absolute').slightSubmenu({
	submenuUlClass : $.fn.slightSubmenu.defaults.submenuUlClass
			+ ' horizontal absolute',
	multipleSubmenusOpenedAllowed : false,
	buttonCloseNotSubmenuEvents : 'mouseenter click'
});

// Demo 3
$('#master-menu-horizontal-no-transition').slightSubmenu({
	handlerButtonIn : function($submenu) {
		$submenu.show();
	},
	handlerForceClose : function($submenu) {
		$submenu.hide();
	}
});

// Demo 4
$('#master-menu-clickonly').slightSubmenu({
	buttonActivateEvents : 'click'
});

// Demo 5
$('#master-menu-clickonly-single').slightSubmenu({
	buttonActivateEvents : 'click',
	multipleSubmenusOpenedAllowed : false
});

// Demo 6
$('#master-menu-clickonly-single-openonly').slightSubmenu({
	buttonActivateEvents : 'click',
	buttonCloseNotSubmenuEvents : 'click',
	multipleSubmenusOpenedAllowed : false
});

// Demo 7
var fancyOptions = {
	prependButtons: true,
	applyInlineCss: true,

    buttonInlineCss: (function() {
    	// nothing to be scared of here, simply using the nifty $.extend 
    	// utility of jQuery, so that I can keep the current styles and 
    	// override some of them by keeping myself from copy-pasting like  
    	// an idiot
        return $.extend({}, $.fn.slightSubmenu.defButtonInlineCss, {
			// new css:
        	borderRadius: '15px 15px / 3px 3px',
    		boxShadow: '0 0 6px #c2c2fd',
    		position: 'relative',
    		left: '-28px',
    		display: 'inline-block'
		});
    })(),
    
    topLiWithUlClass: 
    	$.fn.slightSubmenu.defaults.topLiWithUlClass +
    		' unpadded'
};

$('#master-menu-deeper-nesting').slightSubmenu(fancyOptions);

//Demo 8
$.extend($.fn.slightSubmenu.defaults, fancyOptions);

$('#master-menu-overriden-defaults').slightSubmenu();

//Demo 9
$('.with-submenu').slightSubmenu();