/*
 * jQuery Slight Submenu plugin
 * Version 1.1.0
 * Author: Velidar Petrov
 * Licensed under the MIT license
 */
;(function($, window, document, undefined) {
	$.fn.slightSubmenu = function(options) {

		var defaults = $.fn.slightSubmenu.defaults;
		var settings = $.extend(true, {}, defaults, options);
		
		this.each(function() {
			var submenuButtons = [];

			var $this = $(this).is('ul') ? $(this) : $('ul', this).first();
			var $liItems = $this.find('> li');

			$this.addClass(settings.topUlClass);
			$liItems.addClass(settings.topLiClass);
			if (settings.applyInlineCss) {
				$this.css(settings.topContainerInlineCss);
				$liItems.css(settings.directLiInlineCss);
			}

			var buttonMarkup = settings.handlerGenerateButtonMarkup(settings.buttonClass);
			$liItems.each(function() {
				var $this = $(this);
				var $submenu = $('ul:first', this);
				
				// proceed if there is an ul (submenu) in this list item
				if ($submenu.length) {
					$submenu.addClass(settings.submenuUlClass);
					$this.addClass(settings.topLiWithUlClass);

					$submenu.hide(0);
					$submenu.addClass(settings.submenuUlClass);

					var $submenuButton = $(buttonMarkup);
					if (settings.applyInlineCss) {
						$submenuButton.css(settings.buttonInlineCss);
						$submenu.css(settings.submenuUlInlineCss);
					}
					
					submenuButtons.push($submenuButton[0]);

					if (settings.prependButtons) {
						$this.prepend($submenuButton);
					} else {
						$submenu.before($submenuButton);
					}
				}
			});
			
			var onSubmenuButtonClose = function($button) {
				$button.removeClass(settings.buttonSubmenuOpenedClass);
				if (settings.applyInlineCss) {
					var cleared = {}; 
					$.each(settings.buttonActiveInlineCss, function(el) {
						cleared[el] = '';
					});
					$button.css(cleared);
				}
			};
			
			$(submenuButtons).on(settings.buttonActivateEvents, function(event) {
				// find the corresponding to the button submenu
				var $this = $(this);
				var $submenuUl = $this.parents('li').eq(0).find('ul:first'); 
					
				if ($submenuUl.is(':animated') ||  $submenuUl.find('> li').is(':animated')) {
					return;
				}
				
				if ($.inArray(event.type, settings.buttonCloseNotSubmenuEvents.split(/\s+/)) 
						<= -1 && $submenuUl.is(':visible')) {
					onSubmenuButtonClose($this);
					settings.handlerForceClose($submenuUl);
					return;
				}

				$submenuUl = $submenuUl || $this.parents('li').eq(0).find('ul:first');

				if (!settings.multipleSubmenusOpenedAllowed) {
					var currentUl = $submenuUl[0];
					var $stillVisible = $submenuUl.parents('ul').eq(0).find('> li').find('ul:first')
						.filter(function(i, el) {
							return el !== currentUl && $(el).is(':visible');
						});
					if ($stillVisible.length) {
						onSubmenuButtonClose($this);
						$stillVisible.parent().find('.' + settings.buttonSubmenuOpenedClass).
							removeClass(settings.buttonSubmenuOpenedClass);
						settings.handlerForceClose($stillVisible);
					}
				}
				
				$this.addClass(settings.buttonSubmenuOpenedClass);
				if (settings.applyInlineCss) {
					$this.css(settings.buttonActiveInlineCss);
				}
				
				if (!$submenuUl.is(':visible')) {
					settings.handlerButtonIn($submenuUl);
				}
			});

		});
		return this;
	};
	
	$.fn.slightSubmenu.handlerButtonIn = function($submenuUl) {
		$submenuUl.show(1000);
	};

	$.fn.slightSubmenu.handlerForceClose = function($submenuUl) {
		$submenuUl.hide(1000);
	};
	
	$.fn.slightSubmenu.handlerGenerateButtonMarkup = function(buttonClass) {
		return '<span class="' + buttonClass + '"></span>';
	};

	$.fn.slightSubmenu.defTopContainerInlineCss = { position: 'relative' };
	$.fn.slightSubmenu.defDirectLiInlineCss = {};	
	$.fn.slightSubmenu.defSubmenuUlInlineCss = {};
	$.fn.slightSubmenu.defButtonActiveInlineCss = {};
	
	$.fn.slightSubmenu.defButtonInlineCss = {
		background: '#ccc',
		display: 'inline',
		marginLeft: '8px',
		width: '10px',
		height: '18px',
		position: 'absolute',
		cursor: 'pointer'	// this might be the difference 
							// between the 'click' working on iOS and not
	};

	$.fn.slightSubmenu.defaults = {
		buttonActivateEvents: 'click mouseenter',
		buttonCloseNotSubmenuEvents: 'mouseenter',
		multipleSubmenusOpenedAllowed: true,
		prependButtons: false,
		applyInlineCss: false,
		topUlClass: 'slight-submenu-master-ul',
		topLiClass: '',
		topLiWithUlClass: 'li-with-ul',
		buttonClass: 'slight-submenu-button',
		buttonSubmenuOpenedClass: 'opened',
		submenuUlClass: 'slight-submenu-ul',
		directLiInlineCss: $.fn.slightSubmenu.defDirectLiInlineCss,
		submenuUlInlineCss: $.fn.slightSubmenu.defSubmenuUlInlineCss,
		topContainerInlineCss: $.fn.slightSubmenu.defTopContainerInlineCss,
		buttonInlineCss: $.fn.slightSubmenu.defButtonInlineCss,
		buttonActiveInlineCss: $.fn.slightSubmenu.defButtonActiveInlineCss,
		handlerButtonIn: $.fn.slightSubmenu.handlerButtonIn,
		handlerForceClose: $.fn.slightSubmenu.handlerForceClose,
		handlerGenerateButtonMarkup: $.fn.slightSubmenu.handlerGenerateButtonMarkup
	};
})(jQuery, window, document);