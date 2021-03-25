define([
    'jquery'
], function ($) {
    'use strict';

    return function () {

        var showLabel;

        showLabel = $.validator.prototype.showLabel;
        $.extend(true, $.validator.prototype, {
            /**
             * @param {*} element
             * @param {*} message
             */
            showLabel: function (element, message) {
                var label, elem;

                showLabel.call(this, element, message);

                // ARIA (adding aria-invalid & aria-describedby)
                label = this.errorsFor(element);
                elem = $(element);

                if (!label.attr('id')) {
                    label.attr('id', this.idOrName(element) + '-error');
                }
                elem.attr('aria-invalid', 'true')
                    .attr('aria-describedby', label.attr('id'));

                elem.parents('.field, .swatch-attribute').attr('aria-invalid', 'true');
            }
        });

        /**
         * Extend form validation to support swatch accessibility
         */
        $.widget('mage.validation', $.mage.validation, {
            /**
             * Handle form validation. Focus on first invalid form field.
             *
             * @param {jQuery.Event} event
             * @param {Object} validation
             */
            listenFormValidateHandler:  function (event, validation) {
                var firstActive = $(validation.errorList[0].element || []),
                    lastActive = $(validation.findLastActive() ||
                        validation.errorList.length && validation.errorList[0].element || []),
                    parent, windowHeight, successList;

                if (lastActive.is(':hidden')) {
                    parent = lastActive.parent();
                    windowHeight = $(window).height();
                    $('html, body').animate({
                        scrollTop: parent.offset().top - windowHeight / 2
                    });
                }

                // ARIA (removing aria attributes if success)
                successList = validation.successList;

                if (successList.length) {
                    $.each(successList, function () {
                        $(this)
                            .removeAttr('aria-describedby')
                            .removeAttr('aria-invalid');
                        $(this).parents('.field, .swatch-attribute').removeAttr('aria-invalid');
                    });
                }

                if (firstActive.length) {
                    firstActive.focus();
                }
            }
        });
    };
});
