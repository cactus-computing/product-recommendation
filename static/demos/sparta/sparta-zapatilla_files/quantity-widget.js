define([
    'jquery',
    'jquery/ui'
], function ($) {
    'use strict';

    $.widget('semexpert.quantityWidget', {

        /**
         * Creates widget 'semexpert.quantityWidget'
         * @private
         */
        _create: function () {
            var $qtyInput = $(this.element),
                $wrapper = $qtyInput.parent(),
                $qtyIncrease = $('<button class="qty-mod qty-increase" type="button">+</button>'),
                $qtyDecrease = $('<button class="qty-mod qty-decrease" type="button">-</button>'),
                step = 1,
                max = this.options.max,
                min = this.options.min;

            $wrapper.addClass('qty-input-wrapper');
            $wrapper.prepend($qtyDecrease);
            $wrapper.append($qtyIncrease);

            $qtyIncrease.on('click', function () {
                var oldVal = parseFloat($qtyInput.val()),
                    newVal = oldVal + step;

                if (newVal <= max) {
                    $qtyInput.val(newVal);
                    $qtyInput.trigger('keyup');
                }
            });
            $qtyDecrease.on('click', function () {
                var oldVal = parseFloat($qtyInput.val()),
                    newVal = oldVal - step;

                if (newVal >= min) {
                    $qtyInput.val(newVal);
                    $qtyInput.trigger('keyup');
                }
            });
        }

    });

    return $.semexpert.quantityWidget;

});
