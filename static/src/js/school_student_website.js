/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
publicWidget.registry.StudentWebsite = publicWidget.Widget.extend({
    selector: '#request_form',
    events: {
        'change #same': '_onChangeSame',
    },
    _onChangeSame(events){
    if ($('#same').prop("checked")) {
    $('#permanent_add_id').hide();
    }
    else {
    $('#permanent_add_id').show();
    }
    },
});
