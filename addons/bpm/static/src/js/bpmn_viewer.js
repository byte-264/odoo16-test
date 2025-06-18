/** @odoo-module **/

import {registry} from '@web/core/registry';
import {loadJS, loadCSS} from '@web/core/assets';

const {Component, useRef, onWillStart, onMounted, useState} = owl;
import {useService} from '@web/core/utils/hooks';

const BPMN_ELEMENTS = [
    'bpmn:Task', 'bpmn:UserTask', 'bpmn:ScriptTask',
    'bpmn:SequenceFlow', 'bpmn:CallActivity',
]

const FUTURE_ELEMENTS = [
    'bpmn:Process', 'bpmn:SubProcess', 'bpmn:Participant',
    'bpmn:StartEvent', 'bpmn:EndEvent',
    'bpmn:ServiceTask',
    'bpmn:BusinessRuleTask', 'bpmn:SendTask', 'bpmn:ReceiveTask', 'bpmn:ManualTask',
    'bpmn:ExclusiveGateway', 'bpmn:ParallelGateway', 'bpmn:InclusiveGateway', 'bpmn:ComplexGateway',
    'bpmn:EventBasedGateway', 'bpmn:IntermediateCatchEvent', 'bpmn:IntermediateThrowEvent',
    'bpmn:BoundaryEvent', 'bpmn:MessageFlow',
    'bpmn:Message', 'bpmn:Signal'
]

export class BpmnViewer extends Component {
    setup() {
        this.bpmn = useRef('bpmn_viewer')
        this.userService = useService('user')
        this.lastUpdate = Date.now()
        this.state=useState({
            hasManagerGroup: false
        })

        onWillStart(async () => {
            this.state.hasManagerGroup = await this.userService.hasGroup('bpm.group_manager')
            if (this.state.hasManagerGroup) {
                await loadJS('/bpm/static/src/lib/bpmn-js/dist/bpmn-modeler.production.min.js')
            } else {
                await loadJS('/bpm/static/src/lib/bpmn-js/dist/bpmn-viewer.production.min.js')
            }
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/diagram-js.css')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/bpmn-js.css')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/bpmn-font/css/bpmn.css')
            await loadCSS('/bpm/static/src/lib/bpmn-js/dist/assets/bpmn-font/css/bpmn-codes.css')
            window.test = this
        })

        onMounted(async () => {
            this._bpmn = new BpmnJS({container: this.bpmn.el})
            if (this.props.record.data.xml) {
                await this._bpmn.importXML(this.props.record.data.xml);
            } else {
                await this._bpmn.createDiagram()
            }

            this._bpmn.get('eventBus').on('element.changed', (e) => {
                const now = Date.now()
                if (now - this.lastUpdate > 30000) {
                    this.lastUpdate = now
                    this.check_diagram()
                }
            })

            this._bpmn.get('eventBus').on('element.dblclick', async (event) => {
                    const element = event.element;
                    if (element) {
                        if (BPMN_ELEMENTS.includes(element.type)) {
                            const filtered = this.props.record.data.element_ids.records.filter(x => x.data.bpmn_id == element.id)
                            let element_id = null
                            if (filtered.length == 0) {
                                element_id = await this.env.services.orm.create('bpm.process.element', [{
                                    'bpmn_id': element.id,
                                    'process_id': this.props.record.data.id,
                                    'name': element.businessObject.name,
                                    'type': element.type.replace('bpmn:', ''),
                                }])

                            } else {
                                element_id = filtered[0].data
                            }
                            await this.env.services.action.doAction({
                                type: 'ir.actions.act_window',
                                res_model: 'bpm.process.element',
                                views: [[false, 'form']],
                                target: 'new',
                                res_id: element_id.id,
                            })
                            event.preventDefault();
                        }
                    }
                }
            )
        })
    }


    async check_diagram() {
        if (!this.state.hasManagerGroup) return;
        await this.props.record.save()
        const data = await this._bpmn.saveXML()
        const svg_data = await this._bpmn.saveSVG()
        await this.env.services.orm.write('bpm.process', [this.props.record.resId], {
            xml: data.xml,
            screenshot: btoa(svg_data.svg)
        })
        await this.props.record.load()
        await this.props.record.update()
        const modeling = this._bpmn.get('modeling')
        this.props.record.data.element_ids.records.forEach(async x => {
            const e = this._bpmn.get('elementRegistry').get(x.data.bpmn_id)
            if (e && e.name != x.data.name) {
                modeling.updateProperties(e, {name: x.data.name})
            }
        })
    }
}

BpmnViewer.template = 'bpm.BpmnViewer';
registry.category('fields').add('bpmn_viewer',BpmnViewer);