define(
    ['jquery'],
    function ($) {
        'use strict';

        var mixin = {
            options: {
                disableDimensionsChangedEvents: false
            },
            _create: function () {
                var constructor = this._super();

                if (this.options.disableDimensionsChangedEvents) {
                    this.element.off('dimensionsChanged');
                    this.element.on('dimensionsChanged', function (event) {
                       event.stopPropagation();
                       return false;
                    });
                }

                return constructor;
            }
        };

        return function (widget) {
            return $.widget('mage.collapsible', widget, mixin);
        }
    }
);