/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { X2ManyFieldDialog } from "@web/views/fields/relational_utils";
import { makeDeferred } from '@mail/utils/deferred';
import { useService } from "@web/core/utils/hooks";
import { blockUI, unblockUI } from "web.framework";

patch(X2ManyFieldDialog.prototype, "one2many_description", {
    setup() {
        this._super(...arguments);
        this.notification = useService("notification");

    },

    async load_models(){
        var self = this;
        let modelsDef = makeDeferred();
        this.humanConfig = {
            backend: 'webgl', //webgl, humangl
            async: true,
            warmup: 'none', //none, face
            cacheSensitivity: 0,
            debug: true,
            deallocate: true,
            modelBasePath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/',
            hand: {
                enabled: false
            },
            body: {
                enabled: false
            },
            gesture: {
                enabled: false
            },
            object: {
                enabled: false
            },
            face: {
                enabled: true,
                detector: {
                    return: true,
                    rotation: false,
                    maxDetected: 1,
                    iouThreshold: 0.01,
                    minConfidence: 0.4,
                    modelPath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/blazeface.json',
                },
                mesh: { 
                    enabled: true,
                    modelPath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/facemesh.json',
                },
                iris: { 
                    enabled: false,
                    modelPath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/iris.json',
                },
                emotion: { 
                    enabled: true,
                    modelPath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/emotion.json',
                },
                description: { 
                    enabled: true,
                    modelPath: '/hr_attendance_controls_pro/static/src/js/lib/human/models/faceres.json',
                },
            },
            body: { enabled: false },
            hand: { enabled: false },
            object: { enabled: false },
            gesture: { enabled: false },
        };
        this.human = new Human.Human(this.humanConfig);
        this.human.env['perfadd'] = false; // is performance data showing instant or total values
        this.human.validate(this.humanConfig);            
        await this.human.load();
        if (true) {
            const warmup = new ImageData(50, 50);
            await this.human.detect(warmup);
        }
        modelsDef.resolve();
        return modelsDef
    },

    async save({ saveAndNew }) {
        if(this.record.resModel === 'hr.employee.faces'){
            var self = this;
            var image = this.record.data.image || false;            
            if (image){
                var image = $('#face_image div img')[0];        
                self.getDescriptor(image);
            }
        }else{
            return this._super(...arguments);
        }
    },

    async getDescriptor(image){
        var self = this;
        if (image.src.indexOf("placeholder.png") > -1) {
            self.notification.add(this.env._t("Photo unavailable."),{ 
                type: "danger" 
            });
            return;
        }
        blockUI();
        self.load_models().then(async function(){
            console.log(self.human);          
            if (("Human" in window)) {
                var img = document.createElement('img');
                img.src= image.src;

                await self.human.detect(img, self.humanConfig).then((res) => {
                    for (const i in res.face) {
                        // did not get valid results
                        if (!res.face[i].tensor) {
                            unblockUI();
                            self.notification.add(this.env._t("Did not get valid results from uploaded photo."), {
                                type: "danger",
                            });
                            return;
                        }
                        // face analysis score too low
                        if ((res.face[i].faceScore || 0) < self.human.config.face.detector.minConfidence) {
                            unblockUI();
                            self.notification.add(this.env._t("Face analysis score too low."), {
                                type: "danger",
                            });
                            return;
                        }
                        self.human.tf.dispose(res.tensor);
                        var embedding = res.face[i].embedding;
                        if (embedding) {  
                            var descriptor = self.arrayBufferToBase64(embedding);
                            self.updateDescriptor(descriptor).then(function(){
                                unblockUI();
                            });
                        }else{
                            unblockUI();
                            self.notification.add(this.env._t("Did not get valid results from uploaded photo."), {
                                type: "danger",
                            });
                            return;
                        }                        
                    }
                });
            }else{
                return setTimeout(() => self.getDescriptor(image))
            }
        })
    },
    async updateDescriptor(descriptor){
        var self = this;
        this.record.update({
            'descriptor': descriptor,
            'has_descriptor' : true,
        });
        if (await this.record.checkValidity()) {
            const saved = (await this.props.save(this.record, {})) || this.record;
        } else {
            return false;
        }
        this.props.close();
        return true;
    },
    arrayBufferToBase64(embedding) {
        var binary = '';
        var embedding = new Float32Array(embedding);
        var bytes = new Uint8Array(embedding.buffer);
        var len = bytes.byteLength;
        for (var i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    },
});