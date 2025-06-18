/* @odoo-module */

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
const { onMounted, onWillDestroy, onWillUnmount, useState } = owl;
import {useService} from '@web/core/utils/hooks';

patch(FormController.prototype, "bpm", {
    setup() {
        this._super();
        this.ormService = useService('orm')
        this.bpm = useState({
            hasprocesses: false,
            processes: [],
        });

        onMounted(() => {
            this.ormService.search('bpm.process', [['model_name','=',this.props.resModel]]).then(async(processes) => {
                if (processes.length){
                    this.bpm.hasprocesses = true;
                    this.bpm.processes= await this.ormService.call('bpm.process','search_read',[] ,{
                        domain: [['id','in', processes] ],
                        fields:['name','id','active_instance_count']
                    });
                }else{
                    this.bpm.hasprocesses = false;
                    this.bpm.processes=[];
                }
            });
        });
    },

    async startProcess(data){
        console.log(data)
        const id= Number(data.target.attributes['data-id'].value);
        this.user.updateContext({resId:this.props.resId, resModel:this.props.resModel})
        const action=this.ormService.call('bpm.process','action_start_process',[id])
        await this.env.services.action.doAction(action)
    },
    debug(){
        console.log(this)
    }
});