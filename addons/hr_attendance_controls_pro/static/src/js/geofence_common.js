odoo.define('hr_attendance_controls_pro.GeofenceCommon', function () {
    "use strict";
    var GeofenceCommon = {
        cssLibs: [
            '/hr_attendance_controls_pro/static/src/js/lib/ol-6.12.0/ol.css',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-ext.css',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-geocoder.min.css',
        ],
        jsLibs: [
            '/hr_attendance_controls_pro/static/src/js/lib/ol-6.12.0/ol.js',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-ext.js',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-geocoder.min.js',
        ],
    };

    return {
        GeofenceCommon: GeofenceCommon,
    };
});
