define([
    'jquery',
    'Magento_GoogleTagManager/js/google-tag-manager'
], function ($) {
    'use strict';

    /**
     * Dispatch common data to GA
     *
     * @param {Object} commonData - common data 
     *
     * @private
     */
    function notify(commonData) {

        console.log('common.js');

        var dlUpdate = {
                'event': 'page',
                'ecommerce': {
                    'data': []
                }
            };

        dlUpdate.ecommerce.data = commonData;
        //dlUpdate.ecommerce.catalogSearch.keyword = searchQuery;
        
        window.dataLayer.push(dlUpdate);
    }

    return function (data) {
        
        window.dataLayer ?
            notify(data.commonData) :
            $(document).on(
                'ga:inited',
                notify.bind(this, data.commonData)
            );
    };
});