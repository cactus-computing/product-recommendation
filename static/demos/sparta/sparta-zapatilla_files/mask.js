define([
    'ko',
    'jquery',
    'iMask'
], function (ko, $, iMask) {
    "use strict";

    return function (target) {
        if (ko.bindingHandlers.mask == undefined) {
            ko.bindingHandlers.mask = {
                init: function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
                    element.value = viewModel.value();
                    var mask = viewModel.mask;
                    if (mask) {
                        bindingContext.$data.masked(new IMask(element, {
                            mask: mask
                        }));
                    }
                }
            }
        }
        return target;
    };
});
