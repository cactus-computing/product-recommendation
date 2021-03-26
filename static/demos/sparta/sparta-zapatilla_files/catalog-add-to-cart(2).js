define([
    'jquery',
    'mage/translate',
    'underscore',
    'Magento_Catalog/js/product/view/product-ids-resolver',
    'jquery-ui-modules/widget'
],

/**
 * Expands original add-to-cart to force open the mini cart after success
 *
 * @param {jQuery} $
 * @returns {function(*=): *}
 */
function ($, $t, _, idsResolver) {
    'use strict';
    /**
     * Mixin constructor
     */
    return function (widget) {
        $.widget('mage.catalogAddToCart', widget, {    
            /**
             * @param {jQuery} form
             */
            ajaxSubmit: function (form) {
                var self = this,
                    productIds = idsResolver(form),
                    formData;

                $(self.options.minicartSelector).trigger('contentLoading');
                self.disableAddToCartButton(form);
                formData = new FormData(form[0]);

                $.ajax({
                    url: form.attr('action'),
                    data: formData,
                    type: 'post',
                    dataType: 'json',
                    cache: false,
                    contentType: false,
                    processData: false,

                    /** @inheritdoc */
                    beforeSend: function () {
                        if (self.isLoaderEnabled()) {
                            $('body').trigger(self.options.processStart);
                        }
                    },

                    /** @inheritdoc */
                    success: function (res) {

                        var eventData, parameters;

                        $(document).trigger('ajax:addToCart', {
                            'sku': form.data().productSku,
                            'productIds': productIds,
                            'form': form,
                            'response': res
                        });

                        if (self.isLoaderEnabled()) {
                            $('body').trigger(self.options.processStop);
                        }

                        if (res.backUrl) {
                            eventData = {
                                'form': form,
                                'redirectParameters': []
                            };
                            // trigger global event, so other modules will be able add parameters to redirect url
                            $('body').trigger('catalogCategoryAddToCartRedirect', eventData);

                            if (eventData.redirectParameters.length > 0 &&
                                window.location.href.split(/[?#]/)[0] === res.backUrl
                            ) {
                                parameters = res.backUrl.split('#');
                                parameters.push(eventData.redirectParameters.join('&'));
                                res.backUrl = parameters.join('#');
                            }

                            self._redirect(res.backUrl);

                            return;
                        }

                        if (res.messages) {
                            $(self.options.messagesSelector).html(res.messages);
                        }

                        if (res.minicart) {
                            $(self.options.minicartSelector).replaceWith(res.minicart);
                            $(self.options.minicartSelector).trigger('contentUpdated');
                        }

                        if (res.product && res.product.statusText) {
                            $(self.options.productStatusSelector)
                                .removeClass('available')
                                .addClass('unavailable')
                                .find('span')
                                .html(res.product.statusText);
                        }
                        self.enableAddToCartButton(form);
                                                
                        $('[data-block="minicart"]').off('contentUpdated');
                        $(self.options.minicartSelector).on('contentUpdated', function (ev) {
                            ev.stopPropagation();
                            self.openMiniCart();
                            $('[data-block="minicart"]').off('contentUpdated');
                        });
                    },
                    /** @inheritdoc */
                    error: function (res) {
                        $(document).trigger('ajax:addToCart:error', {
                            'sku': form.data().productSku,
                            'productIds': productIds,
                            'form': form,
                            'response': res
                        });
                    },

                    /** @inheritdoc */
                    complete: function (res) {
                        if (res.state() === 'rejected') {
                            location.reload();
                        }
                    }
                });
            },
            /**
             * Opens minicart window and sets a timer to close it back
             */
            openMiniCart: function () {
                var close;
                
                function closeMiniCart() {
                    close = setTimeout(function() {
                        $('[data-block="minicart"]').find('[data-role="dropdownDialog"]').dropdownDialog('close');
                    }, 6000);
                }

                function stopCloseMiniCart() {
                    clearTimeout(close);
                }

                $('[data-block="minicart"]').find('[data-role="dropdownDialog"]').dropdownDialog('open');

                closeMiniCart();

                $('[data-block="minicart"]').on('dropdowndialogopen', function () {
                    stopCloseMiniCart();
                    $('[data-block="minicart"]').find('[data-role="dropdownDialog"]').dropdownDialog('open');
                });
            }
        });

        return $.mage.catalogAddToCart;
    };

});
