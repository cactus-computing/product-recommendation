!(function($) {
    var $myGroup = $('#show-products');
    $myGroup.on('show.bs.collapse','.collapse', function() {
        $myGroup.find('.collapse.show').collapse('hide');
    });
}