define([
    'jquery',
    'jquery/ui',
    'jquery/validate',
    'Magento_Ui/js/lib/validation/validator',
    'mage/translate',
], function ($, ui, validte, validator) {
    'use strict';
    return function () {
        var validateRut = function (v) {
            if (v.length == 0)
                return true;

            if (v.length < 8)
                return false;

            let i1 = v.indexOf("-");
            let dv = v.substr(i1 + 1);
            dv = dv.toUpperCase();
            let nu = v.substr(0, i1);
            if (nu.length > 8)
                return false;

            let cnt = 0;
            let suma = 0;
            for (let i = nu.length - 1; i >= 0; i--) {
                let dig = nu.substr(i, 1);
                let fc = cnt + 2;
                suma += parseInt(dig) * fc;
                cnt = (cnt + 1) % 6;
            }
            let dvok = 11 - (suma % 11);
            let dvokstr = "";
            if (dvok == 11) dvokstr = "0";
            if (dvok == 10) dvokstr = "K";
            if ((dvok != 11) && (dvok != 10)) dvokstr = "" + dvok;

            if (dvokstr == dv)
                return true;

            return false;
        };
        $.validator.addMethod("validate-rut", validateRut, $.mage.__("Invalid RUT format"));
        validator.addRule("validate-rut", validateRut, $.mage.__("Invalid RUT format"));
    }
});
