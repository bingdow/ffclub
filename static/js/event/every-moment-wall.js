"use strict";


(function() {
    $('.eventPhoto').mouseover(function() {
        $('#fxos-phone-frame').show();
        $('#fxos-phone-frame').position({
            my: 'center',
            at: 'center',
            of: $(this),
            using: function(css) {
                $('#fxos-phone-frame').animate(css, 350);
            }
        });
    });
})();