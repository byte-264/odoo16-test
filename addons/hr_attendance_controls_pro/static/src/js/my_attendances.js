odoo.define('hr_attendance_controls_pro.my_attendances', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var KioskMode = require('hr_attendance.kiosk_mode');

    var GeofenceCommon = require('hr_attendance_controls_pro.GeofenceCommon');
    var session = require("web.session");
    var Dialog = require('web.Dialog');

    var core = require('web.core');
    var _t = core._t;

    var MyAttendances = MyAttendances.include({
        cssLibs: [
            '/hr_attendance_controls_pro/static/src/js/lib/ol-6.12.0/ol.css',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-ext.css',
        ],
        jsLibs: [
            '/hr_attendance_controls_pro/static/src/js/lib/ol-6.12.0/ol.js',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-ext.js',
        ],
        events: _.extend({}, MyAttendances.prototype.events, {
            'click .gmap_kisok_toggle': '_toggle_gmap',
            'click .gip_kisok_toggle': '_toggle_gip',
            'click .glocation_kisok_toggle': '_toggle_glocation',
            'change .oe_attendance_reasons': '_on_change_reason',
        }),
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.labeledFaceDescriptors = [];
        },
        willStart: function () {
            var self = this;
            var superDef = this._super.apply(this, arguments);
            var def = this._rpc({
                model: 'hr.attendance.reasons',
                method: 'search_read',
                args: [[], ['id', 'name', 'attendance_state']],
            }).then(function (reasons) {
                self.reasons = reasons;
            });
            return Promise.all([superDef, def]);
        },
        start: function () {
            var self = this;
            this.olmap = null;
            this.ip = null;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_hr_attendance_kiosk_mode').addClass('o_hr_attendance_kiosk_mode_top');
                if (window.location.protocol == 'https:') {

                    self.$('.o_hr_attendance_sign_in_out_icon').css('pointer-events','none');

                    self.def_geofence = $.Deferred();
                    if (session.hr_attendance_geofence) {
                        self._initMap();
                    } else {
                        self.$('.gmap_kisok_container').css('display', 'none');
                        self.def_geofence.resolve();
                    }

                    self.def_geolocation = $.Deferred();
                    if (session.hr_attendance_geolocation) {
                        self._getGeolocation();
                    } else {
                        self.$('.glocation_kisok_container').css('display', 'none');
                        self.def_geolocation.resolve();
                    }

                    self.def_face_recognition = $.Deferred();
                    if (session.hr_attendance_face_recognition) {
                        self.$('a.o_hr_attendance_sign_in_out_icon').addClass('icon_disabled');
                        if (!("Human" in window)) {
                            self._loadHuman();
                        } else {
                            self._loadModels();
                            self.def_face_recognition.resolve();
                        }
                    } else {
                        self.def_face_recognition.resolve();
                    }

                    self.def_ipaddress = $.Deferred();
                    if (session.hr_attendance_ip) {
                        self._getUserIP();
                    } else {
                        self.$('.gip_kisok_container').css('display', 'none');
                        self.def_ipaddress.resolve();
                    }
                    $.when(self.def_geofence, self.def_ipaddress, self.def_face_recognition, self.def_geolocation).then(function(){
                        self.$('.o_hr_attendance_sign_in_out_icon').css('pointer-events','');
                    })
                }

                self.def_reason = $.Deferred();
                if (session.hr_attendance_reason) {
                    self._showReasons();
                } else {
                    self.$('.attendance_reason').css('display', 'none');
                    self.def_reason.resolve();
                }
            });
        },
        _loadHuman: function () {
            var self = this;
            if (!("Human" in window)) {
                (function (w, d, s, g, js, fjs) {
                    g = w.Human || (w.Human = {});
                    g.Human = { q: [], ready: function (cb) { this.q.push(cb); } };
                    js = d.createElement(s); fjs = d.getElementsByTagName(s)[0];
                    js.src = window.origin + '/hr_attendance_controls_pro/static/src/js/lib/human/source/human.js';
                    fjs.parentNode.insertBefore(js, fjs); js.onload = function () {
                        console.log("apis loaded");
                        self._loadModels();
                        self.def_face_recognition.resolve();
                    };
                }(window, document, 'script'));
            }
        },
        _loadModels: async function () {
            var self = this;
            let modelsDef = $.Deferred();
            this.humanConfig = {
                debug: false,
                backend: 'humangl', //webgl, humangl
                async: true,
                warmup: 'none', //none, face
                cacheSensitivity: 0,
                deallocate: true,
                modelBasePath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/',
                filter: {
                    enabled: true,
                    equalization: true,
                },
                face: {
                    enabled: true, 
                    detector: { 
                        rotation: false,
                        minConfidence: 0.6,
                        maxDetected: 1,
                        mask: false,
                        skipInitial: true,
                    }, 
                    mesh: { 
                        enabled: true 
                    }, 
                    attention: { 
                        enabled: false 
                    }, 
                    iris: { 
                        enabled: true 
                    }, 
                    description: { 
                        enabled: true 
                    }, 
                    emotion: { 
                        enabled: true 
                    }, 
                    antispoof: { 
                        enabled: true 
                    }, 
                    liveness: { 
                        enabled: true 
                    } 
                },
                body: { 
                    enabled: false 
                },
                hand: { 
                    enabled: false 
                },
                object: { 
                    enabled: false 
                },
                segmentation: { 
                    enabled: false 
                },
                gesture: { 
                    enabled: true 
                },
            };
            this.human = new Human.Human(this.humanConfig);
            this.human.env['perfadd'] = false; // is performance data showing instant or total values
            this.human.draw.options.font = 'small-caps 18px "Lato"'; // set font used to draw labels when using draw methods
            this.human.draw.options.lineHeight = 20;
            this.human.validate(this.humanConfig);
            await this.human.load();
            if (true) {
                const warmup = new ImageData(50, 50);
                await this.human.detect(warmup);
            }
            modelsDef.resolve().then(async function () {
                self.$('a.o_hr_attendance_sign_in_out_icon').removeClass('icon_disabled');
                self.loadLabeledImages();
            });
            return modelsDef
        },
        warmup: function(){
            var self = this;            
            var xhr = new XMLHttpRequest();       
            xhr.open("GET", "/hr_attendance_controls_pro/static/src/img/startFaceDetect.jpg", true); 
            xhr.responseType = "blob";
            xhr.onload = function (e) {
                var reader = new FileReader();
                reader.onload = async function(event) {
                var res = event.target.result;
                    var img = document.createElement('img');
                    img.src = res;
                    var face = await self.human.detect(img, self.humanConfig); 
                    self.humanConfig.videoOptimized = true;
                    if (face.tensor)   
                        self.human.tf.dispose(face.tensor);
                }
                var file = this.response;
                reader.readAsDataURL(file)
            };
            xhr.send();
        },
        loadLabeledImages: async function () {
            var self = this;
            self.load_label = $.Deferred();
            return await this._rpc({
                route: '/hr_attendance_controls_pro/loadLabeledImages/'
            }).then(async function (data) {
                data.map((data, i) => {
                    const descriptors = [];
                    for (var i = 0; i < data.descriptors.length; i++) {
                        if (data.descriptors[i]) {
                            var buffer = self.base64ToArrayBuffer(data.descriptors[i]);
                            self.labeledFaceDescriptors.push({
                                'name': data.name,
                                'label': data.label,
                                'descriptors': Array.from(buffer),
                            });
                        }
                    }
                });
                self.load_label.resolve();
            });
        },
        base64ToArrayBuffer: function (base64) {
            var self = this;
            var binary_string = window.atob(base64);
            var len = binary_string.length;
            var bytes = new Uint8Array(len);
            for (var i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return new Float32Array(bytes.buffer);
        },
        on_attach_callback: function () {
            this._super.apply(this, arguments);
            if (this.olmap) {
                this.olmap.updateSize();
            }
        },
        _toggle_gmap: function () {
            var self = this;
            if (self.$(".gmap_kisok_toggle").hasClass('fa-angle-double-down')) {
                self.$('.gmap_kisok_view').toggle('show');
                self.$("i.gmap_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
                self.$(".o_hr_attendance_kiosk_backdrop")[0].setAttribute('style', 'height: calc(100vh + 197px);');
                setTimeout(function () {
                    self.olmap.updateSize()
                }, 400);
            } else {
                self.$('.gmap_kisok_view').toggle('hide');
                self.$("i.gmap_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
                self.$(".o_hr_attendance_kiosk_backdrop")[0].setAttribute('style', 'height: calc(100vh);');
                setTimeout(function () {
                    self.olmap.updateSize()
                }, 400);
            }
        },
        _toggle_gip: function () {
            var self = this;
            if (self.$(".gip_kisok_toggle").hasClass('fa-angle-double-down')) {
                self.$('.gip_kisok_view').toggle('show');
                self.$("i.gip_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
                if (self.ip) {
                    self.$('.gip_kisok_view span')[0].innerText = "IP: " + self.ip;
                }
            } else {
                self.$('.gip_kisok_view').toggle('hide');
                self.$("i.gip_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
            }
        },
        _toggle_glocation: function () {
            var self = this;
            if (self.$(".glocation_kisok_toggle").hasClass('fa-angle-double-down')) {
                self.$('.glocation_kisok_view').toggle('show');
                self.$("i.glocation_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
                if (self.latitude && self.longitude) {
                    self.$('.glocation_kisok_view span')[0].innerText = "Lattitude:" + self.latitude + ", Longitude:" + self.longitude;
                }
            } else {
                self.$('.glocation_kisok_view').toggle('hide');
                self.$("i.glocation_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
            }
        },
        _showReasons: function () {
            var self = this;
            self.$('.attendance_reason').css('display', '');
            self.def_reason.resolve();
        },
        _on_change_reason: function () {
            var self = this;
            var inputReason = this.$('.oe_attendance_reasons')[0];
            if (inputReason.value !== '') {
                self.attendance_reason = inputReason.value;
            }
        },
        _initMap: function () {
            var self = this;
            if (window.location.protocol == 'https:') {
                var options = {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 27000
                };
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
                } else {
                    self.geolocation = false;
                }

                function successCallback(position) {
                    self.latitude = position.coords.latitude;
                    self.longitude = position.coords.longitude;
                    if (!self.olmap) {
                        var olmap_div = self.$('.gmap_kisok_view').get(0);
                        $(olmap_div).css({
                            width: '425px !important',
                            height: '200px !important'
                        });
                        var vectorSource = new ol.source.Vector({});
                        self.olmap = new ol.Map({
                            layers: [
                                new ol.layer.Tile({
                                    source: new ol.source.OSM(),
                                }),
                                new ol.layer.Vector({
                                    source: vectorSource
                                })
                            ],

                            loadTilesWhileInteracting: true,
                            target: olmap_div,
                            view: new ol.View({
                                center: [self.latitude, self.longitude],
                                zoom: 2,
                            }),
                        });
                        const coords = [position.coords.longitude, position.coords.latitude];
                        const accuracy = ol.geom.Polygon.circular(coords, position.coords.accuracy);
                        vectorSource.clear(true);
                        vectorSource.addFeatures([
                            new ol.Feature(accuracy.transform('EPSG:4326', self.olmap.getView().getProjection())),
                            new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat(coords)))
                        ]);
                        self.olmap.getView().fit(vectorSource.getExtent(), { duration: 100, maxZoom: 6 });
                        self.olmap.updateSize();
                    }
                    self.$('.gmap_kisok_container').css('display', '');
                    self.def_geofence.resolve();
                }

                function errorCallback(err) {
                    switch (err.code) {
                        case err.PERMISSION_DENIED:
                            console.log("The request for geolocation was refused by the user.");
                            break;
                        case err.POSITION_UNAVAILABLE:
                            console.log("There is no information about the location available.");
                            break;
                        case err.TIMEOUT:
                            console.log("The request for the user's location was unsuccessful.");
                            break;
                        case err.UNKNOWN_ERROR:
                            console.log("An unidentified error has occurred.");
                            break;
                    }
                    self.def_geofence.resolve();
                }
            }
            else {
                self.$('.gmap_kisok_container').addClass('d-none');
                self.do_notify(false, _t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."));
            }
        },
        _getUserIP: function (onNewIP) {
            var self = this;
            $.getJSON("https://api.ipify.org?format=json", function (data) {
                if (data.ip) {
                    self.ip = data.ip;
                    self.$('.gip_kisok_container').css('display', '');
                    self.def_ipaddress.resolve();
                }
            });
        },
        _getGeolocation: function () {
            var self = this;
            var options = {
                enableHighAccuracy: true,
                maximumAge: 30000,
                timeout: 27000
            };
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
            } else {
                self.geolocation = false;
                self.def_geolocation.resolve();
            }

            function successCallback(position) {
                self.latitude = position.coords.latitude;
                self.longitude = position.coords.longitude;
                self.$('.glocation_kisok_container').css('display', '');
                self.def_geolocation.resolve();
            }

            function errorCallback(err) {
                switch (err.code) {
                    case err.PERMISSION_DENIED:
                        console.log("The request for geolocation was refused by the user.");
                        break;
                    case err.POSITION_UNAVAILABLE:
                        console.log("There is no information about the location available.");
                        break;
                    case err.TIMEOUT:
                        console.log("The request for the user's location was unsuccessful.");
                        break;
                    case err.UNKNOWN_ERROR:
                        console.log("An unidentified error has occurred.");
                        break;
                }
                self.def_geolocation.reject();
            }
        },
        update_attendance: function () {
            var self = this;
            if (window.location.protocol == 'https:') {
                self._validate_attendances();
            } else {
                this._rpc({
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                })
                    .then(function (result) {
                        if (result.action) {
                            var action = result.action;
                            self.do_action(action);
                            var employee_id = action.attendance.employee_id[0];
                            var attendance_id = action.attendance['id'];
                            self._rpc({
                                model: 'hr.attendance',
                                method: 'update_reason',
                                args: [[attendance_id], employee_id, self.attendance_reason],
                            });
                        } else if (result.warning) {
                            self.do_warn(result.warning);
                        }
                    });
            }
        },
        _validate_attendances: function () {
            var self = this;

            self.data_ip_address = null;
            self.data_latitude = null;
            self.data_longitude = null;
            self.data_is_inside = false;
            self.data_geofence_ids = null;
            self.data_photo = false;
            self.data_employee_id = null;

            self.def_geolocation_data = new $.Deferred();
            if (session.hr_attendance_geolocation) {
                if (window.location.protocol == 'https:') {
                    self._validate_Geolocation();
                } else {
                    self.def_geolocation_data.resolve();
                }
            } else {
                self.def_geolocation_data.resolve();
            }

            self.def_geofence_data = new $.Deferred();
            if (session.hr_attendance_geofence) {
                if (window.location.protocol == 'https:') {
                    self._validate_Geofence();
                } else {
                    self.def_geofence_data.resolve();
                }
            } else {
                self.def_geofence_data.resolve();
            }

            self.def_ip_data = new $.Deferred();
            if (session.hr_attendance_ip) {
                if (window.location.protocol == 'https:') {
                    self._validate_IP();
                } else {
                    self.def_ip_data.resolve();
                }
            } else {
                self.def_ip_data.resolve();
            }

            self.def_face_recognition = new $.Deferred();
            if (session.hr_attendance_face_recognition) {
                if (window.location.protocol == 'https:') {
                    self._open_recognition_dialog();
                } else {
                    self.def_face_recognition.resolve();
                }
            } else {
                self.def_face_recognition.resolve();
            }

            self.def_photo_data = new $.Deferred();
            if (session.hr_attendance_photo) {                
                if (window.location.protocol == 'https:') {
                self._validate_Photo();
            }else{
                self.def_photo_data.resolve();
            }
            }else{
                self.def_photo_data.resolve();
            }

            $.when(self.def_geolocation_data, self.def_geofence_data, self.def_face_recognition, self.def_photo_data, self.def_ip_data).then(function () {                
                self._manual_attendance();
            })
        },
        _open_recognition_dialog: function () {
            var self = this;
            var options = {};
            if (self.labeledFaceDescriptors && self.labeledFaceDescriptors.length != 0) {
                self.matchedEmployee = new FaceRecognitionDialog(this, options, self.labeledFaceDescriptors).open();
            } else {
                self.displayNotification({ message: _t('Detection Failed: Resource not found, Please add it to your employee profile.'), type: 'danger' });
            }
        },
        _validate_face_recognition(employee_id, img) {
            var self = this;
            if (employee_id && img) {
                self.data_photo = img;
                self.data_employee_id = employee_id;
                if (parseInt(self.employee.id) === parseInt(self.data_employee_id)) {
                    self.def_face_recognition.resolve();
                } else {
                    self.displayNotification({ message: _t('Detection Failed: Detected employee is not matched with login employee profile.'), type: 'danger' });
                }
            } else {
                self.def_face_recognition.reject();
            }
        },
        _validate_Photo: function () {
            var self = this;
            this.dialogPhoto = new Dialog(this, {
                size: 'medium',
                title: _t("Capture Snapshot"),
                $content: `
                <div class="container-fluid">
                    <div class="col-12 controls mb8">
                        <fieldset class="reader-config-group">
                            <div class="row">
                                <div class="col-3">
                                    <label>
                                        <span>Select Camera</span>
                                    </label>
                                </div>
                                <div class="col-6">
                                    <select name="video_source" class="videoSource" id="videoSource">                                       
                                    </select>
                                </div>
                                <div class="col-3">
                                </div>
                            </div>
                        </fieldset>
                    </div>
                    <div class="row">                                
                        <div class="col-12" id="videoContainer">
                            <video autoplay muted playsinline id="video" style="width: 100%; max-height: 100%; box-sizing: border-box;" autoplay="1"/>
                            <canvas id="image" style="display: none;"/>
                        </div>
                    </div>
                </div>`,
                buttons: [
                    {
                        text: _t("Capture Snapshot"), classes: 'btn-primary captureSnapshot',
                    },
                    {
                        text: _t("Close"), classes: 'btn-secondary captureClose', close: true,
                    }
                ]
            }).open();

            this.dialogPhoto.opened().then(async function () {
                var videoElement = self.dialogPhoto.$('#video').get(0);
                var videoSelect = self.dialogPhoto.$('select#videoSource').get(0);
                videoSelect.onchange = getStream;

                getStream().then(getDevices).then(gotDevices);

                function getStream() {
                    if (window.stream) {
                        window.stream.getTracks().forEach(track => {
                            track.stop();
                        });
                    }
                    const videoSource = videoSelect.value;
                    const constraints = {
                        video: { deviceId: videoSource ? { exact: videoSource } : undefined }
                    };
                    return navigator.mediaDevices.getUserMedia(constraints).then(gotStream).catch(handleError);
                }

                function getDevices() {
                    return navigator.mediaDevices.enumerateDevices();
                }

                function gotDevices(deviceInfos) {
                    window.deviceInfos = deviceInfos;
                    for (const deviceInfo of deviceInfos) {
                        const option = document.createElement('option');
                        option.value = deviceInfo.deviceId;
                        if (deviceInfo.kind === 'videoinput') {
                            option.text = deviceInfo.label || "Camera" + (videoSelect.length + 1) + "";
                            videoSelect.appendChild(option);
                        }
                    }
                }

                function gotStream(stream) {
                    window.stream = stream;
                    videoSelect.selectedIndex = [...videoSelect.options].
                        findIndex(option => option.text === stream.getVideoTracks()[0].label);
                    videoElement.srcObject = stream;
                }

                function handleError(error) {
                    console.error('Error: ', error);
                }

                var $captureSnapshot = self.dialogPhoto.$footer.find('.captureSnapshot');
                var $closeBtn = self.dialogPhoto.$footer.find('.captureClose');

                $captureSnapshot.on('click', function (event) {
                    var img64 = "";
                    var image = self.dialogPhoto.$('#image').get(0);
                    image.width = $(video).width();
                    image.height = $(video).height();
                    image.getContext('2d').drawImage(video, 0, 0, image.width, image.height);
                    var img64 = image.toDataURL("image/jpeg");
                    img64 = img64.replace(/^data:image\/(png|jpg|jpeg|webp);base64,/, "");
                    if (img64) {
                        self.data_photo = img64;
                        self.def_photo_data.resolve();
                        $closeBtn.click();
                    }else{
                        self.def_photo_data.reject();
                    }
                    $captureSnapshot.text("uploading....").addClass('disabled');
                });

            });
        },
        _validate_Geolocation: function () {
            var self = this;
            if (self.latitude && self.longitude) {
                self.data_latitude = self.latitude || null;
                self.data_longitude = self.longitude || null;
                self.def_geolocation_data.resolve();
            } else {
                self.def_geolocation_data.reject();
            }
        },
        _validate_IP: function () {
            var self = this;
            if (self.ip) {
                self.data_ip_address = self.ip || null;
                self.def_ip_data.resolve();
            } else {
                self.def_ip_data.reject();
            }
        },
        _validate_Geofence: async function () {
            var self = this;
            var insidePolygon = false;
            var insideGeofences = []

            await self._rpc({
                model: 'hr.attendance.geofence',
                method: 'search_read',
                args: [[['company_id', '=', self.getSession().company_id], ['employee_ids', 'in', self.employee.id]], ['id', 'name', 'overlay_paths']],
            }).then(function (res) {
                self.geofence_data = res.length && res;
                if (!res.length) {
                    self.def_geofence_data.reject();
                }

                var options = {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 27000
                };
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
                }

                function successCallback(position) {
                    self.latitude = position.coords.latitude;
                    self.longitude = position.coords.longitude;
                    if (self.olmap) {
                        for (let i = 0; i < self.geofence_data.length; i++) {
                            var path = self.geofence_data[i].overlay_paths;
                            var value = JSON.parse(path);
                            if (Object.keys(value).length > 0) {
                                let coords = ol.proj.fromLonLat([self.longitude, self.latitude]);
                                var features = new ol.format.GeoJSON().readFeatures(value);
                                var geometry = features[0].getGeometry();
                                insidePolygon = geometry.intersectsCoordinate(coords);
                                if (insidePolygon === true) {
                                    insideGeofences.push(self.geofence_data[i].id);
                                }
                            }
                        }

                        if (insideGeofences.length > 0) {
                            self.data_is_inside = true;
                            self.data_geofence_ids = insideGeofences;
                            self.def_geofence_data.resolve();
                        } else {
                            Swal.fire({
                                title: 'Access Denied',
                                text: "You haven't entered any of the geofence zones.",
                                icon: 'error',
                                confirmButtonColor: '#3085d6',
                                confirmButtonText: 'Ok'
                            }).then(function () {
                                if (self.dialogPhoto && self.dialogPhoto != undefined) {
                                    var $closeBtn = self.dialogPhoto.$footer.find('.captureClose');
                                    $closeBtn.click();
                                }
                                if (self.matchedEmployee && self.matchedEmployee != undefined) {
                                    var $closeBtn = self.matchedEmployee.$footer.find('.captureClose');
                                    $closeBtn.click();
                                }
                            });
                            self.def_geofence_data.reject();
                        }
                    }
                }
                function errorCallback(err) {
                    console.log(err);
                }
            })
        },

        _manual_attendance: function () {
            var self = this;
            var data_ip_address = self.data_ip_address || null;
            var data_latitude = self.data_latitude || null;
            var data_longitude = self.data_longitude || null;
            var data_geofence_ids = self.data_geofence_ids || null;
            var data_photo = self.data_photo || null;

            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', null, [data_latitude, data_longitude], data_ip_address, data_geofence_ids, [data_photo]],
            }).then(function (result) {
                if (result.action) {
                    var action = result.action;
                    self.do_action(action);
                    var employee_id = action.attendance.employee_id[0];
                    var attendance_id = action.attendance['id'];
                    self._rpc({
                        model: 'hr.attendance',
                        method: 'update_reason',
                        args: [[attendance_id], employee_id, self.attendance_reason],
                    });
                } else if (result.warning) {
                    self.do_warn(result.warning);
                }
            });
        },
    });

    var KioskMode = KioskMode.include({
        cssLibs: [
            '/hr_attendance_controls_pro/static/src/js/lib/ol-6.12.0/ol.css',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-ext.css',
        ],
        jsLibs: [
            '/hr_attendance_controls_pro/static/src/js/lib/ol-6.12.0/ol.js',
            '/hr_attendance_controls_pro/static/src/js/lib/ol-ext/ol-ext.js',
        ],
        events: _.extend(KioskMode.prototype.events, {
            "click .o_hr_kiosk_face_recognition": _.debounce(function () {
                this.update_kiosk_attendance();
            }, 200, true),
            'click .gmap_kisok_toggle': '_toggle_gmap',
            'click .glocation_kisok_toggle': '_toggle_glocation',
            'click .gip_kisok_toggle': '_toggle_gip',
        }),
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.labeledFaceDescriptors = [];
        },
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                if (window.location.protocol == 'https:') {
                    self.def_geofence = $.Deferred();
                    if (session.hr_attendance_geofence_k) {
                        self._initMap();
                    } else {
                        self.$('.gmap_kisok_container').css('display', 'none');
                        self.def_geofence.resolve();
                    }

                    self.def_geolocation = $.Deferred();
                    if (session.hr_attendance_geolocation_k) {
                        self._getGeolocation();
                    } else {
                        self.$('.glocation_kisok_container').css('display', 'none');
                        self.def_geolocation.resolve();
                    }

                    self.def_face_recognition = $.Deferred();
                    if (session.hr_attendance_face_recognition_k) {
                        if (!("Human" in window)) {
                            self._loadHuman();
                        } else {
                            self._loadModels();
                            self.def_face_recognition.resolve();
                        }
                    } else {
                        self.$('.face_recognition_kisok_container').css('display', 'none');
                        self.def_face_recognition.resolve();
                    }

                    self.def_ipaddress = $.Deferred();
                    if (session.hr_attendance_ip_k) {
                        self._getUserIP();
                    } else {
                        self.$('.gip_kisok_container').css('display', 'none');
                        self.def_ipaddress.resolve();
                    }
                }
            });
        },
        _toggle_gmap: function () {
            var self = this;
            if (self.$(".gmap_kisok_toggle").hasClass('fa-angle-double-down')) {
                self.$('.gmap_kisok_view').toggle('show');
                self.$("i.gmap_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
                self.$(".o_hr_attendance_kiosk_backdrop")[0].setAttribute('style', 'height: calc(100vh + 197px);');
                setTimeout(function () {
                    self.olmap.updateSize()
                }, 400);
            } else {
                self.$('.gmap_kisok_view').toggle('hide');
                self.$("i.gmap_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
                self.$(".o_hr_attendance_kiosk_backdrop")[0].setAttribute('style', 'height: calc(100vh);');
                setTimeout(function () {
                    self.olmap.updateSize()
                }, 400);
            }
        },
        _toggle_glocation: function () {
            var self = this;
            if (self.$(".glocation_kisok_toggle").hasClass('fa-angle-double-down')) {
                self.$('.glocation_kisok_view').toggle('show');
                self.$("i.glocation_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
                if (self.latitude && self.longitude) {
                    self.$('.glocation_kisok_view span')[0].innerText = "Lattitude:" + self.latitude + ", Longitude:" + self.longitude;
                }
            } else {
                self.$('.glocation_kisok_view').toggle('hide');
                self.$("i.glocation_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
            }
        },
        _toggle_gip: function () {
            var self = this;
            if (self.$(".gip_kisok_toggle").hasClass('fa-angle-double-down')) {
                self.$('.gip_kisok_view').toggle('show');
                self.$("i.gip_kisok_toggle", self).toggleClass("fa-angle-double-down fa-angle-double-up");
                if (self.ip) {
                    self.$('.gip_kisok_view span')[0].innerText = "IP: " + self.ip;
                }
            } else {
                self.$('.gip_kisok_view').toggle('hide');
                self.$("i.gip_kisok_toggle", self).toggleClass("fa-angle-double-up fa-angle-double-down");
            }
        },
        _getUserIP: function (onNewIP) {
            var self = this;
            $.getJSON("https://api.ipify.org?format=json", function (data) {
                if (data.ip) {
                    self.ip = data.ip;
                    self.$('.gip_kisok_container').css('display', '');
                    self.def_ipaddress.resolve();
                }
            });
        },
        _initMap: function () {
            var self = this;
            if (window.location.protocol == 'https:') {
                var options = {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 27000
                };
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
                } else {
                    self.geolocation = false;
                }

                function successCallback(position) {
                    self.latitude = position.coords.latitude;
                    self.longitude = position.coords.longitude;
                    if (!self.olmap) {
                        var olmap_div = self.$('.gmap_kisok_view').get(0);
                        $(olmap_div).css({
                            width: '425px !important',
                            height: '200px !important'
                        });
                        var vectorSource = new ol.source.Vector({});
                        self.olmap = new ol.Map({
                            layers: [
                                new ol.layer.Tile({
                                    source: new ol.source.OSM(),
                                }),
                                new ol.layer.Vector({
                                    source: vectorSource
                                })
                            ],

                            loadTilesWhileInteracting: true,
                            target: olmap_div,
                            view: new ol.View({
                                center: [self.latitude, self.longitude],
                                zoom: 2,
                            }),
                        });
                        const coords = [position.coords.longitude, position.coords.latitude];
                        const accuracy = ol.geom.Polygon.circular(coords, position.coords.accuracy);
                        vectorSource.clear(true);
                        vectorSource.addFeatures([
                            new ol.Feature(accuracy.transform('EPSG:4326', self.olmap.getView().getProjection())),
                            new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat(coords)))
                        ]);
                        self.olmap.getView().fit(vectorSource.getExtent(), { duration: 100, maxZoom: 6 });
                        self.olmap.updateSize();
                    }
                    self.$('.gmap_kisok_container').css('display', '');
                    self.def_geofence.resolve();
                }

                function errorCallback(err) {
                    switch (err.code) {
                        case err.PERMISSION_DENIED:
                            console.log("The request for geolocation was refused by the user.");
                            break;
                        case err.POSITION_UNAVAILABLE:
                            console.log("There is no information about the location available.");
                            break;
                        case err.TIMEOUT:
                            console.log("The request for the user's location was unsuccessful.");
                            break;
                        case err.UNKNOWN_ERROR:
                            console.log("An unidentified error has occurred.");
                            break;
                    }
                    self.def_geofence.resolve();
                }
            }
            else {
                self.$('.gmap_kisok_container').addClass('d-none');
                self.do_notify(false, _t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."));
            }
        },
        _getGeolocation: function () {
            var self = this;
            var options = {
                enableHighAccuracy: true,
                maximumAge: 30000,
                timeout: 27000
            };
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
            } else {
                self.geolocation = false;
                self.def_geolocation.resolve();
            }

            function successCallback(position) {
                self.latitude = position.coords.latitude;
                self.longitude = position.coords.longitude;
                self.$('.glocation_kisok_container').css('display', '');
                self.def_geolocation.resolve();
            }

            function errorCallback(err) {
                switch (err.code) {
                    case err.PERMISSION_DENIED:
                        console.log("The request for geolocation was refused by the user.");
                        break;
                    case err.POSITION_UNAVAILABLE:
                        console.log("There is no information about the location available.");
                        break;
                    case err.TIMEOUT:
                        console.log("The request for the user's location was unsuccessful.");
                        break;
                    case err.UNKNOWN_ERROR:
                        console.log("An unidentified error has occurred.");
                        break;
                }
                self.def_geolocation.reject();
            }
        },
        _loadHuman: function () {
            var self = this;
            if (!("Human" in window)) {
                (function (w, d, s, g, js, fjs) {
                    g = w.Human || (w.Human = {});
                    g.Human = { q: [], ready: function (cb) { this.q.push(cb); } };
                    js = d.createElement(s); fjs = d.getElementsByTagName(s)[0];
                    js.src = window.origin + '/hr_attendance_controls_pro/static/src/js/lib/human/source/human.js';
                    fjs.parentNode.insertBefore(js, fjs); js.onload = function () {
                        console.log("apis loaded");
                        self._loadModels();
                        self.def_face_recognition.resolve();
                    };
                }(window, document, 'script'));
            }
        },
        _loadModels: async function () {
            var self = this;
            let modelsDef = $.Deferred();
            this.humanConfig = {
                debug: false,
                backend: 'humangl', //webgl, humangl
                async: true,
                warmup: 'none', //none, face
                cacheSensitivity: 0,
                deallocate: true,
                modelBasePath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/',
                filter: {
                    enabled: true,
                    equalization: true,
                },
                face: {
                    enabled: true, 
                    detector: { 
                        rotation: false,
                        minConfidence: 0.6,
                        maxDetected: 1,
                        mask: false,
                        skipInitial: true,
                    }, 
                    mesh: { 
                        enabled: true 
                    }, 
                    attention: { 
                        enabled: false 
                    }, 
                    iris: { 
                        enabled: true 
                    }, 
                    description: { 
                        enabled: true 
                    }, 
                    emotion: { 
                        enabled: true 
                    }, 
                    antispoof: { 
                        enabled: true 
                    }, 
                    liveness: { 
                        enabled: true 
                    } 
                },
                body: { 
                    enabled: false 
                },
                hand: { 
                    enabled: false 
                },
                object: { 
                    enabled: false 
                },
                segmentation: { 
                    enabled: false 
                },
                gesture: { 
                    enabled: true 
                },
            };
            this.human = new Human.Human(this.humanConfig);
            this.human.env['perfadd'] = false; // is performance data showing instant or total values
            this.human.draw.options.font = 'small-caps 18px "Lato"'; // set font used to draw labels when using draw methods
            this.human.draw.options.lineHeight = 20;
            this.human.validate(this.humanConfig);
            await this.human.load();
            if (true) {
                const warmup = new ImageData(50, 50);
                await this.human.detect(warmup);
            }
            modelsDef.resolve().then(async function () {
                if (session.hr_attendance_face_recognition_k) {
                    self.$('.face_recognition_kisok_container').css('display', '');
                }
                self.loadLabeledImages();
            });
            return modelsDef
        },
        warmup: function(){
            var self = this;            
            var xhr = new XMLHttpRequest();       
            xhr.open("GET", "/hr_attendance_controls_pro/static/src/img/startFaceDetect.jpg", true); 
            xhr.responseType = "blob";
            xhr.onload = function (e) {
                var reader = new FileReader();
                reader.onload = async function(event) {
                var res = event.target.result;
                    var img = document.createElement('img');
                    img.src = res;
                    var face = await self.human.detect(img, self.humanConfig); 
                    self.humanConfig.videoOptimized = true;
                    if (face.tensor)   
                        self.human.tf.dispose(face.tensor);
                }
                var file = this.response;
                reader.readAsDataURL(file)
            };
            xhr.send();
        },
        loadLabeledImages: async function () {
            var self = this;
            self.load_label = $.Deferred();
            return await this._rpc({
                route: '/hr_attendance_controls_pro/loadLabeledImages/'
            }).then(async function (data) {
                data.map((data, i) => {
                    const descriptors = [];
                    for (var i = 0; i < data.descriptors.length; i++) {
                        if (data.descriptors[i]) {
                            var buffer = self.base64ToArrayBuffer(data.descriptors[i]);
                            self.labeledFaceDescriptors.push({
                                'name': data.name,
                                'label': data.label,
                                'descriptors': Array.from(buffer),
                            });
                        }
                    }
                });
                self.load_label.resolve();
            });
        },
        base64ToArrayBuffer: function (base64) {
            var self = this;
            var binary_string = window.atob(base64);
            var len = binary_string.length;
            var bytes = new Uint8Array(len);
            for (var i = 0; i < len; i++) {
                bytes[i] = binary_string.charCodeAt(i);
            }
            return new Float32Array(bytes.buffer);
        },
        update_kiosk_attendance: function () {
            var self = this;
            if (window.location.protocol == 'https:') {
                self._validate_attendances();
            } else {
                self.do_notify(false, _t("GEOLOCATION API MAY ONLY WORKS WITH HTTPS CONNECTIONS."));
            }
        },
        _validate_attendances: function () {
            var self = this;

            self.data_ip_address = null;
            self.data_photo = false;
            self.data_employee_id = null;
            self.data_is_inside = false;
            self.data_geofence_ids = null;

            self.def_geolocation_data = new $.Deferred();
            if (session.hr_attendance_geolocation_k) {
                if (window.location.protocol == 'https:') {
                    self._validate_Geolocation();
                } else {
                    self.def_geolocation_data.resolve();
                }
            } else {
                self.def_geolocation_data.resolve();
            }

            self.def_ip_data = new $.Deferred();
            if (session.hr_attendance_ip_k) {
                if (window.location.protocol == 'https:') {
                    self._validate_IP();
                } else {
                    self.def_ip_data.resolve();
                }
            } else {
                self.def_ip_data.resolve();
            }

            self.def_face_recognition = new $.Deferred();
            if (session.hr_attendance_face_recognition_k) {
                if (window.location.protocol == 'https:') {
                    self._open_recognition_dialog();
                } else {
                    self.def_face_recognition.resolve();
                }
            } else {
                self.def_face_recognition.resolve();
            }

            $.when(self.def_geolocation_data, self.def_geofence_data, self.def_face_recognition, self.def_ip_data).then(function () {
                self._update_attendance();
            });
        },
        _validate_Geolocation: function () {
            var self = this;
            if (self.latitude && self.longitude) {
                self.data_latitude = self.latitude || null;
                self.data_longitude = self.longitude || null;
                self.def_geolocation_data.resolve();
            } else {
                self.def_geolocation_data.reject();
            }
        },
        _validate_IP: function () {
            var self = this;
            if (self.ip) {
                self.data_ip_address = self.ip || null;
                self.def_ip_data.resolve();
            } else {
                self.def_ip_data.reject();
            }
        },
        _open_recognition_dialog: function () {
            var self = this;
            var options = {};
            if (self.labeledFaceDescriptors && self.labeledFaceDescriptors.length != 0) {
                self.matchedEmployee = new FaceRecognitionDialog(this, options, self.labeledFaceDescriptors).open();
            } else {
                self.displayNotification({ message: _t('Detection Failed: Resource not found, Please add it to your employee profile.'), type: 'danger' });
            }
        },
        _update_attendance: function () {
            var self = this;

            var data_ip_address = self.data_ip_address || null;
            var data_photo = self.data_photo || null;
            var data_employee_id = self.data_employee_id || null;
            var data_latitude = self.data_latitude || null;
            var data_longitude = self.data_longitude || null;
            var data_geofence_ids = self.data_geofence_ids || null;

            this._rpc({
                model: 'hr.employee',
                method: 'attendance_kiosk_recognition',
                args: [[parseInt(data_employee_id)], [data_latitude, data_longitude], data_ip_address, data_geofence_ids, [data_photo]],
            })
                .then(function (result) {
                    if (result.action) {
                        self.do_action(result.action);

                    } else if (result.warning) {
                        self.displayNotification({ message: result.warning, type: 'danger' });
                    }
                });
        },
        _validate_face_recognition: async function(employee_id, img) {
            var self = this;
            if (employee_id && img) {
                self.data_photo = img;
                self.data_employee_id = employee_id;
                self.def_geofence_data = new $.Deferred();
                await self.def_face_recognition.resolve().then(async function(){
                    if (self.data_employee_id && self.data_employee_id != undefined) {
                        
                        if (session.hr_attendance_geofence_k) {
                            if (window.location.protocol == 'https:') {
                                await self._validate_Geofence();
                            } else {
                                self.def_geofence_data.resolve();
                            }
                        } else {
                            self.def_geofence_data.resolve();
                        }
                    }
                });
            } else {
                self.def_face_recognition.reject();
            }
        },
        _validate_Geofence: async function () {
            var self = this;
            var insidePolygon = false;
            var insideGeofences = []

            await self._rpc({
                model: 'hr.attendance.geofence',
                method: 'search_read',
                args: [[['company_id', '=', self.getSession().company_id], ['employee_ids', 'in', parseInt(self.data_employee_id)]], ['id', 'name', 'overlay_paths']],
            }).then(function (res) {
                self.geofence_data = res.length && res;
                if (!res.length) {
                    self.def_geofence_data.reject();
                }

                var options = {
                    enableHighAccuracy: true,
                    maximumAge: 30000,
                    timeout: 27000
                };
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
                }

                function successCallback(position) {
                    self.latitude = position.coords.latitude;
                    self.longitude = position.coords.longitude;
                    if (self.olmap) {
                        for (let i = 0; i < self.geofence_data.length; i++) {
                            var path = self.geofence_data[i].overlay_paths;
                            var value = JSON.parse(path);
                            if (Object.keys(value).length > 0) {
                                let coords = ol.proj.fromLonLat([self.longitude, self.latitude]);
                                var features = new ol.format.GeoJSON().readFeatures(value);
                                var geometry = features[0].getGeometry();
                                insidePolygon = geometry.intersectsCoordinate(coords);
                                if (insidePolygon === true) {
                                    insideGeofences.push(self.geofence_data[i].id);
                                }
                            }
                        }

                        if (insideGeofences.length > 0) {
                            self.data_is_inside = true;
                            self.data_geofence_ids = insideGeofences;
                            self.def_geofence_data.resolve();
                        } else {
                            Swal.fire({
                                title: 'Access Denied',
                                text: "You haven't entered any of the geofence zones.",
                                icon: 'error',
                                confirmButtonColor: '#3085d6',
                                confirmButtonText: 'Ok'
                            }).then(function () {
                                if (self.dialogPhoto && self.dialogPhoto != undefined) {
                                    var $closeBtn = self.dialogPhoto.$footer.find('.captureClose');
                                    $closeBtn.click();
                                }
                                if (self.matchedEmployee && self.matchedEmployee != undefined) {
                                    var $closeBtn = self.matchedEmployee.$footer.find('.captureClose');
                                    $closeBtn.click();
                                }
                            });
                            self.def_geofence_data.reject();
                        }
                    }
                }
                function errorCallback(err) {
                    console.log(err);
                }
            })
        },
    });

    var FaceRecognitionDialog = Dialog.extend({
        template: "FaceRecognitionDialog",
        events: _.extend({}, Dialog.events, {
            'change select#videoSource': 'getStream',
            'click .close': '_onDestroy',
        }),
        init: function (parent, options, descriptors) {
            options = options || {};
            this._super(parent, _.extend({
                size: 'medium',
                title: _t('Face Recognition'),
                buttons: [
                    {
                        text: _t("Close"), classes: 'btn-secondary captureClose', close: true, click: this._onDestroy.bind(this)
                    }
                ],
            }, this.options));

            this.is_update_attendance = false;
            this.parent = parent;
            this.descriptors = descriptors;
            this.faceDialog = false;

            this.blinkMin = 10; // minimum duration of a valid blink
            this.blinkMax = 800;  // maximum duration of a valid blink
            this.blink = {
                start: 0,
                end: 0,
                time: 0,
            };

            this.faceCount = false;
            this.faceConfidence = false;
            this.blinkDetected= false;
            this.facingCenter = false;
            this.lookingCenter = false;
            this.antispoofCheck  = false;
            this.livenessCheck  = false;
            this.headCheck = false;
        },
        start: async function () {
            var self = this;
            self.opened().then(function () {
                self.detectionLoop();
                self.drawLoop();
                self.$el.find('.video-controls').removeClass('d-none');
                self.getStream().then(self.getDevices.bind(self)).then(self.gotDevices.bind(self));
            });
            return this._super.apply(this, arguments);
        },
        on_attach_callback: async function () {
            let $modalBodyEl = this.$el.closest('.modal-body');
            if ($modalBodyEl.length !== 0) {
                $modalBodyEl.css('height', 'auto');
            }  
        },
        getStream: function () {
            var self = this;
            if (window.stream) {
                window.stream.getTracks().forEach(track => {
                    track.stop();
                });
            }
            var videoSelect = self.$el.find('select#videoSource').get(0);
            const videoSource = videoSelect.value;
            const constraints = {
                video: { deviceId: videoSource ? { exact: videoSource } : undefined }
            };
            return navigator.mediaDevices.getUserMedia(constraints)
                .then(self.gotStream.bind(self))
                .catch(self.handleError.bind(self));;
        },

        getDevices: function () {
            var self = this;
            return navigator.mediaDevices.enumerateDevices();
        },

        gotDevices: function (deviceInfos) {
            var self = this;
            var videoSelect = self.$el.find('select#videoSource').get(0);
            window.deviceInfos = deviceInfos;
            for (const deviceInfo of deviceInfos) {
                const option = document.createElement('option');
                option.selected = deviceInfo.label;
                option.value = deviceInfo.deviceId;
                if (deviceInfo.kind === 'videoinput') {
                    option.text = deviceInfo.label || "Camera" + (videoSelect.length + 1) + "";
                    videoSelect.appendChild(option);
                }
            }
        },

        gotStream: function (stream) {
            var self = this;
            var videoElement = self.$el.find('#video').get(0);
            var videoSelect = self.$el.find('select#videoSource').get(0);
            window.stream = stream;
            videoSelect.selectedIndex = [...videoSelect.options].findIndex(option => option.text === stream.getVideoTracks()[0].label);
            videoElement.srcObject = stream;
            videoElement.play();
        },
        handleError: function (error) {
            var self = this;
            console.log('Error: ', error);
        },
        _onDestroy: function () {            
            this.destroy();
        },
        destroy: function () {
            if (this.isDestroyed()) {
                return;
            }
            this.faceDialog  = true;
            clearTimeout(this.detectionTimeout);
            clearTimeout(this.drawTimeout);
            if (window.stream) {
                window.stream.getTracks().forEach(track => {
                    track.stop();
                });
            }
            this._super.apply(this, arguments);
        },
        detectionLoop: async function () {
            var self = this;
            var canvas = self.$el.find("#canvas").get(0);
            if (!canvas) {
                return;
            }
            var detectionFace = await self.detectionFace(canvas);
            if (detectionFace == 'break') {
                return;
            }
            
            return new Promise(function(resolve){
                self.detectionTimeout = setTimeout(function(){
                    if(!self.faceDialog){
                        self.detectionLoop();
                        resolve();
                    }                    
                });
            });
        },
        drawLoop: async function () {
            var self = this;
            var video = self.$el.find("#video").get(0);
            var canvas = self.$el.find("#canvas").get(0);
            if (!canvas) {
                return;
            }

            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            if (!video.paused) {
                const interpolated = await self.parent.human.next(self.parent.human.result);
                await self.parent.human.draw.canvas(video, canvas);
                await self.parent.human.draw.all(canvas, interpolated);
                
                //Validating Face
                const faceCount = self.parent.human.result.face.length;
                if (faceCount === 1){
                    self.faceCount = true;

                    if ((self.parent.human.result.face[0].faceScore || 0) > 0.6){
                        self.faceConfidence  = true;
                    }

                    const gestures = Object.values(self.parent.human.result.gesture).map((gesture) => gesture.gesture);

                    if (gestures.includes('blink left eye') || gestures.includes('blink right eye')) {
                        self.blink.start = self.parent.human.now();
                    }

                    if (self.blink.start > 0 && !gestures.includes('blink left eye') && !gestures.includes('blink right eye')) {
                        self.blink.end = self.parent.human.now();
                    }

                    self.blinkDetected = self.blinkDetected || (Math.abs(self.blink.end - self.blink.start) > self.blinkMin && Math.abs(self.blink.end - self.blink.start) < self.blinkMax);
                    if (self.blinkDetected && self.blink.time === 0) {
                        self.blink.time = Math.trunc(self.blink.end - self.blink.start);
                    }

                    if (gestures.includes('facing center')){
                        self.facingCenter = true;
                    }

                    if (gestures.includes('looking center')){
                        self.lookingCenter = true;
                    }

                    if ((self.parent.human.result.face[0].real || 0) > 0.6){
                        self.antispoofCheck = true;
                    }
                    
                    if ((self.parent.human.result.face[0].live || 0) > 0.6){
                        self.livenessCheck = true;
                    }

                    
                    if (gestures.includes('head down') || gestures.includes('head up')) {
                        self.headCheck = true;
                    }
                    
                }
            }

            return new Promise(function(resolve){
                self.drawTimeout = setTimeout(function(){
                    if(!self.faceDialog){
                        self.drawLoop();
                        resolve();
                    }
                },30);
            });
        },

        detectionFace: async function (canvas) {
            var self = this;

            const detect = await self.parent.human.detect(canvas);
            self.parent.human.draw.all(canvas, detect);

            if (!self.faceCount || !self.faceConfidence || !self.blinkDetected || !self.facingCenter || !self.lookingCenter|| !self.antispoofCheck || !self.livenessCheck || !self.headCheck){
                return;
            }

            if (detect && detect.face) {
                for (var face of detect.face) {

                    const matchOptions = { order: 2, multiplier: 25, min: 0.2, max: 0.8 };
                    const descriptor = await self.descriptors.map((rec) => rec.descriptors).filter((desc) => desc.length > 0);
                    const match = await self.parent.human.match.find(face.embedding, descriptor, matchOptions);
                    if ((match.similarity * 100).toFixed(2) >= 60) {
                        var image = self.$el.find("#image").get(0);
                        image.width = $(canvas).width();
                        image.height = $(canvas).height();
                        image.getContext('2d').drawImage(canvas, 0, 0);
                        var img64 = image.toDataURL("image/jpeg");
                        self.update_attendance(self.descriptors[match.index].label, img64);
                        self.parent.human.tf.dispose(face.tensor);
                        return 'break';
                    }
                    self.parent.human.tf.dispose(face.tensor);
                }
            }
        },
        update_attendance: function(employee_id, img){
            var self = this;
            if (!self.is_update_attendance){
                var img = img.replace("data:image/jpeg;base64,", "");
                self.parent._validate_face_recognition(employee_id, img);
                self.is_update_attendance = true;
                self._onDestroy();
            }
        },
    });
    return { FaceRecognitionDialog: FaceRecognitionDialog }
});
