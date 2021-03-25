define([
    'jquery',
    'Magento_GoogleTagManager/js/google-tag-manager'
], function ($, gtm) {
    'use strict';

    /**
     * Dispatch product click event to GA
     *
     * @param {Object} data - product data
     *
     * @private
     */
    function notify(listType, productData) {
        window.dataLayer.push({
            'event': 'productClick',
            'ecommerce': {
                'click': {
                    'actionField': {
                        'list': listType
                    },
                    'products': [
                        productData
                    ]
                },
                'eventCallback': function () {
                    console.log('Callback');
                    document.location = data.url
                }
            }
        });
    }

    return function (productsData) {
        let blockType = productsData.blockType,
            eventBlock

        switch (blockType) {
            case 'catalog.product.related':
                eventBlock = '.products-related .products';
                break;

            case 'product.info.upsell':
                eventBlock = '.products-upsell .products';
                break;

            case 'checkout.cart.crosssell':
                eventBlock = '.products-crosssell .products';
                break;

            case 'category.products.list':
            case 'search_result_list':
                eventBlock = '.products .product.product-item';
                break;
        }

        $(eventBlock).each(function (index, productItemElement) {
            let productLinks = $(productItemElement).find('a, .tocart')

            let productData = productsData.products[index];
            let listType = productsData.listName
            productLinks.each(function (index, element) {
                $(element).on('click', function (listType, productData) {
                    productData.url = $(this).attr('href')
                    window.dataLayer ?
                        notify(listType, productData) :
                        $(document).on('ga:inited', notify.bind(this, listType, productData));
                }.bind(this, listType, productData));
            }.bind(this));
        });
    };
});
