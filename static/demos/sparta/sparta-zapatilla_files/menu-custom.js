define([
    'jquery',
    'jquery/ui',
    'mage/menu'
], function ($) {
    'use strict';

    $.widget('sparta.menu', $.mage.menu, {
        /**
         * @private
         */
        _toggleDesktopMode: function () {
            var categoryParent, html, subMenus, catImg;

            this._on({
                /**
                 * Prevent focus from sticking to links inside menu after clicking
                 * them (focus should always stay on UL during navigation).
                 */
                'mousedown .ui-menu-item > a': function (event) {
                    event.preventDefault();
                },

                /**
                 * Prevent focus from sticking to links inside menu after clicking
                 * them (focus should always stay on UL during navigation).
                 */
                'click .ui-state-disabled > a': function (event) {
                    event.preventDefault();
                },

                /**
                 * @param {jQuer.Event} event
                 */
                'click .ui-menu-item:has(a)': function (event) {
                    var target = $(event.target).closest('.ui-menu-item');

                    if (!this.mouseHandled && target.not('.ui-state-disabled').length) {
                        this.select(event);

                        // Only set the mouseHandled flag if the event will bubble, see #9469.
                        if (!event.isPropagationStopped()) {
                            this.mouseHandled = true;
                        }

                        // Open submenu on click
                        if (target.has('.ui-menu').length) {
                            this.expand(event);
                        } else if (!this.element.is(':focus') &&
                            $(this.document[0].activeElement).closest('.ui-menu').length
                        ) {
                            // Redirect focus to the menu
                            this.element.trigger('focus', [true]);

                            // If the active item is on the top level, let it stay active.
                            // Otherwise, blur the active item since it is no longer visible.
                            if (this.active && this.active.parents('.ui-menu').length === 1) { //eslint-disable-line
                                clearTimeout(this.timer);
                            }
                        }
                    }
                },

                /**
                 * @param {jQuery.Event} event
                 */
                'mouseenter .ui-menu-item': function (event) {
                    var target = $(event.currentTarget),
                        submenu = this.options.menus,
                        ulElement,
                        ulElementWidth,
                        width,
                        targetPageX,
                        rightBound;

                    target.siblings('.nav-cat-img').removeClass('parent-is-expanded');

                    if (target.has(submenu)) {
                        ulElement = target.find(submenu);
                        ulElementWidth = ulElement.outerWidth(true);
                        width = target.outerWidth() * 2;
                        targetPageX = target.offset().left;
                        rightBound = $(window).width();

                        if (ulElementWidth + width + targetPageX > rightBound) {
                            ulElement.addClass('submenu-reverse');
                        }

                        if (targetPageX - ulElementWidth < 0) {
                            ulElement.removeClass('submenu-reverse');
                        }

                        if (ulElement.length > 0) {
                            this.element.addClass('opened');
                            target.siblings('.nav-cat-img').addClass('parent-is-expanded');
                        } else if (target.hasClass('level0')) {
                            this.element.removeClass('opened');
                        }
                    }

                    // Remove ui-state-active class from siblings of the newly focused menu item
                    // to avoid a jump caused by adjacent elements both having a class with a border
                    target.siblings().children('.ui-state-active').removeClass('ui-state-active');
                    this.focus(event, target);

                },

                /**
                 * @param {jQuery.Event} event
                 */
                'mouseleave': function (event) {
                    this.collapseAll(event, true);
                    this.element.removeClass('opened');
                    this.element.find('.nav-cat-img').removeClass('parent-is-expanded');
                },

                /**
                 * @param {jQuery.Event} event
                 */
                'mouseleave .ui-menu': function (event) {
                    this.collapseAll(event, true);
                    this.element.removeClass('opened');
                    this.element.find('.nav-cat-img').removeClass('parent-is-expanded');
                }
            });

            categoryParent = this.element.find('.all-category');
            html = $('html');

            categoryParent.remove();

            if (html.hasClass('nav-open')) {
                html.removeClass('nav-open');
                setTimeout(function () {
                    html.removeClass('nav-before-open');
                }, 300);
            }

            catImg = this.element.find('.level0 > .nav-cat-img');
            $.each(catImg, $.proxy(function (index, item) {
                $(item).appendTo($(item).parents('.ui-menu-item.parent'));
            }, this));

            subMenus = this.element.find('ul.submenu');

            $.each(subMenus, $.proxy(function (index, item) {
                var category = $(item).parent().find('> a span').not('.ui-menu-icon').text(),
                    categoryUrl = $(item).parent().find('> a').attr('href'),
                    menu = $(item);

                this.categoryLink = $('<a>')
                    .attr('href', categoryUrl)
                    .text($.mage.__('All '));

                this.categoryParent = $('<li>')
                    .addClass('ui-menu-item all-category')
                    .html(this.categoryLink);

                if (menu.find('.all-category').length === 0) {
                    if ($(item).hasClass('level0')) {
                        this.categoryLink = $('<a>')
                            .attr('href', categoryUrl)
                            .text($.mage.__('All ') + ' ' + category);

                        this.categoryParent = $('<li>')
                            .addClass('ui-menu-item all-category')
                            .html(this.categoryLink);

                        menu.prepend(this.categoryParent);
                    } else {
                        menu.append(this.categoryParent);
                    }
                }

            }, this));

            $('.navigation > ul > li.level0.parent > a').on('click', function (e) {
                e.preventDefault();
            });

            $('.navigation > ul > li.level0.parent li.level0.parent > a').on('click', function (e) {
                e.preventDefault();
            });

            $('.navigation > ul > li.level0.parent').on('mouseenter', function () {
                $('.navigation').addClass('hover');
            });

            $('.navigation > ul > li.level0.parent').on('mouseleave', function () {
                $('.navigation').removeClass('hover');
            });
        },

        /**
         * @private
         */
        _toggleMobileMode: function () {
            var subMenus, categoryParent, headerHeight;

            $(this.element).off('mouseenter mouseleave');
            this._on({
                /**
                 * @param {jQuery.Event} event
                 */
                'click .ui-menu-item:has(a)': function (event) {
                    var target;

                    event.preventDefault();
                    target = $(event.target).closest('.ui-menu-item');

                    if (!target.has('.ui-menu').length) {
                        window.location.href = target.find('> a').attr('href');
                    }
                },

                /**
                 * @param {jQuery.Event} event
                 */
                'click .ui-menu-item:has(.ui-state-active)': function (event) {
                    event.preventDefault();
                    this.collapseAll(event, false);
                },

                /**
                 * @param {jQuery.Event} event
                 */
                'click .ui-menu-item.parent:has(a)': function (event) {
                    event.preventDefault();

                    $(this).parent().find('.submenu').slideToggle();
                }
            });

            categoryParent = this.element.find('.all-category');

            categoryParent.remove();

            subMenus = this.element.find('.level-top');
            $.each(subMenus, $.proxy(function (index, item) {
                var category = $(item).find('> a span').not('.ui-menu-icon').text(),
                    categoryUrl = $(item).find('> a').attr('href'),
                    menu = $(item).find('> .ui-menu');

                this.categoryLink = $('<a>')
                    .attr('href', categoryUrl)
                    .text($.mage.__('All ') + ' ' + category);

                this.categoryParent = $('<li>')
                    .addClass('ui-menu-item all-category')
                    .html(this.categoryLink);

                if (menu.find('.all-category').length === 0) {
                    menu.prepend(this.categoryParent);
                }

            }, this));

            $('.navigation .trigger-link').on('click', function (e) {
                e.preventDefault();
                $(this).toggleClass('ui-state-active');
                $(this).parent().find('.submenu-container').toggle();
            });

            headerHeight = $('.page-header').height();

            $('.nav-sections').css('top', headerHeight);
            $( "<style>.nav-open .nav-toggle::after { top: " + headerHeight + "px; }</style>" ).appendTo( "head" );
        }

    });

    return $.sparta.menu;
});
