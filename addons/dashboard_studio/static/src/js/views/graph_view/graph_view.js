/** @odoo-module alias=dashboard_studio.GraphView **/

import {useService} from "@web/core/utils/hooks";
import {graphView} from "@web/views/graph/graph_view";
// import {useSetupView} from "@web/views/helpers/view_hook";
import {useSetupView} from "@web/views/view_hook";
import {useModel} from "@web/views/model";
import {registry} from "@web/core/registry";
import {GraphArchParser} from "@web/views/graph/graph_arch_parser";
import {GraphController} from "@web/views/graph/graph_controller";
import DashboardGraphRenderer from "dashboard_studio.GraphRenderer";
import {archParseBoolean} from "@web/views/utils";
import { _lt } from "@web/core/l10n/translation";

const viewRegistry = registry.category("views");


class DashboardGraphArchParser extends GraphArchParser {
    parse(arch, fields = {}) {
        const archInfo = super.parse(...arguments);
        this.visitXML(arch, (node) => {
            switch (node.tagName) {
                case "graph": {
                    if (node.hasAttribute("area")) {
                        archInfo.area = archParseBoolean(node.getAttribute("area"));
                    }
                    if (node.hasAttribute("smooth")) {
                        archInfo.smooth = archParseBoolean(node.getAttribute("smooth"));
                    }
                    const mode = node.getAttribute("type");
                    if (mode && ['polar_area', 'doughnut', 'column'].includes(mode)) {
                        archInfo.mode = mode;
                    }
                }
            }
        });
        return archInfo;
    }
}

export class DashboardGraphController extends GraphController {
    setup() {
        super.setup();
        this.__owl__.parent.parent.controllerInst = this;
        // this.actionService = useService("action");
        // this.model = useModel(this.props.Model, this.props.modelParams);
        //
        // useSetupView({
        //     rootRef: useRef("root"),
        //     getLocalState: () => {
        //         return {metaData: this.model.metaData};
        //     },
        //     getContext: () => this.getContext(),
        // });
    }
}

//
// export default class DashboardGraphView extends GraphView {
//     setup() {
//         this.actionService = useService("action");
//
//         let modelParams;
//         if (this.props.state) {
//             modelParams = this.props.state.metaData;
//         } else {
//             const {arch, fields} = this.props;
//             const parser = new this.constructor.ArchParser();
//             const archInfo = parser.parse(arch, fields);
//             modelParams = {
//                 additionalMeasures: this.props.additionalMeasures,
//                 disableLinking: Boolean(archInfo.disableLinking),
//                 displayScaleLabels: this.props.displayScaleLabels,
//                 fieldAttrs: archInfo.fieldAttrs,
//                 fields: this.props.fields,
//                 groupBy: archInfo.groupBy,
//                 measure: archInfo.measure || "__count",
//                 mode: archInfo.mode || "bar",
//                 order: archInfo.order || null,
//                 resModel: this.props.resModel,
//                 title: archInfo.title || this.env._t("Untitled"),
//
//                 stacked: "stacked" in archInfo ? archInfo.stacked : false,
//                 area: Boolean(archInfo.area),
//                 smooth: Boolean(archInfo.smooth),
//             };
//         }
//
//         this.model = useModel(this.constructor.Model, modelParams);
//
//         useSetupView({
//             getLocalState: () => {
//                 return {metaData: this.model.metaData};
//             },
//             getContext: () => this.getContext(),
//         });
//     }
// }

// DashboardGraphView.Renderer = DashboardGraphRenderer;
// DashboardGraphView.ArchParser = DashboardGraphArchParser;
function props(genericProps, view) {
    let modelParams;
    if (genericProps.state) {
        modelParams = genericProps.state.metaData;
    } else {
        const {arch, fields, resModel} = genericProps;
        const parser = new view.ArchParser();
        const archInfo = parser.parse(arch, fields);
        modelParams = {
            disableLinking: Boolean(archInfo.disableLinking),
            fieldAttrs: archInfo.fieldAttrs,
            fields: fields,
            groupBy: archInfo.groupBy,
            measure: archInfo.measure || "__count",
            mode: archInfo.mode || "bar",
            order: archInfo.order || null,
            resModel: resModel,
            stacked: "stacked" in archInfo ? archInfo.stacked : false,
            cumulated: archInfo.cumulated || false,
            title: archInfo.title || _lt("Untitled"),
            area: Boolean(archInfo.area),
            smooth: Boolean(archInfo.smooth),
        };
    }

    return {
        ...genericProps,
        modelParams,
        Model: view.Model,
        Renderer: view.Renderer,
        buttonTemplate: view.buttonTemplate,
    };
};

viewRegistry.add("dashboard_graph", {
    ...graphView,
    props: props,
    Controller: DashboardGraphController,
    Renderer: DashboardGraphRenderer,
    ArchParser: DashboardGraphArchParser
});
