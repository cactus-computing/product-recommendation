define([
    'jquery',
    'mage/translate',
    'iMask'
], function ($, $t) {
    'use strict';

    return function () {
        $.validator.addMethod(
            'validate-mask',
            function (value, element) {
                if (value == '' && $(element).hasClass('required-entry') == false) {
                    return true;
                }

                var mask = $(element).attr('mask');
                if (mask) {
                    var retorno;
                    $(element).trigger('mask-validate', [
                        function (valor) {
                            retorno = valor;
                            return valor;
                        }
                    ]);

                    return retorno;
                }

                return true;
            },
            $t('Invalid format.')
        )
    }
});
