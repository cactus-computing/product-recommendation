define([
    'jquery',
    'jquery/ui',
    'mage/translate',
    'mage/dropdown'
], function ($) {
    'use strict';

    $.widget('semexpert.dropdownDialog', $.mage.dropdownDialog, {
        /**
         * Extend default functionality to close the dropdown
         * closing other dropdowns when openning a dropdownDialog
         */
        open: function () {
            this._super();
            $(document).trigger('click.hideDropdown');
        }
    });

    return $.semexpert.dropdownDialog;
});
