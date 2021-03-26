define([
    'jquery',
    'jquery/ui',
    'Magento_ConfigurableProduct/js/configurable'
], function($){

    $.widget('semexpert.configurable', $.mage.configurable, {
        /**
         * Show or hide regular price block
         *
         * @param {*} optionId
         * @private
         */
        _displayRegularPriceBlock: function (optionId) {
            var simpleIsSelected = true;

            _.each(this.options.settings, function (element) {
                if (element.value === '') {
                    simpleIsSelected = false;
                }
            });

            if (simpleIsSelected) {
                if (
                    this.options.spConfig.optionPrices[optionId].oldPrice.amount !==
                    this.options.spConfig.optionPrices[optionId].finalPrice.amount
                ) {
                    $(this.options.slyOldPriceSelector).show();
                } else {
                    $(this.options.slyOldPriceSelector).hide();
                }
            } else {
                $(this.options.slyOldPriceSelector).show();
            }
        },
    });

    return $.semexpert.configurable;
});