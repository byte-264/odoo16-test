/** @odoo-module **/

import {registry} from '@web/core/registry';
import {loadJS, loadCSS} from '@web/core/assets';

const {Component, useRef, onWillStart, useState, onMounted} = owl;

export class Bpm extends Component {
    setup() {
        this.bpmn = useRef('bpmn')

        onWillStart(async () => {
            await loadJS('/bpm/static/src/lib/bpmn-js/dist/bpmn-modeler.production.min.js')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/diagram-js.css')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/bpmn-js.css')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/bpmn-font/css/bpmn.css')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/bpmn-font/css/bpmn-codes.css')
            const r=await fetch('/bpm/static/src/bpmn/newDiagram.bpmn')
            this.xml=await r.text()
        })

        onMounted(async() => {

            const diagramXML=this.xml
            this._bpmn = new BpmnJS({ container: this.bpmn.el })
            await this._bpmn.importXML(diagramXML);
            var canvas = this._bpmn.get('canvas');
            canvas.zoom('fit-viewport');
            this._bpmn.get('eventBus').on('element.click', (el) => {
                console.log('element.click:', el)

            })

        })

    }
}

Bpm.template = 'bpm.Bpm';

registry.category('actions').add('bpm', Bpm);