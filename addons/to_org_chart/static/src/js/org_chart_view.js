/**@odoo-module**/

import { _lt } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { OrgChartController } from "./org_chart_controller";
import { OrgChartModel } from "./org_chart_model";
import { OrgChartRenderer } from './org_chart_renderer'
import { SearchModel } from "@web/search/search_model";

const viewRegistry = registry.category("views");

export const orgChartView = {
    type: "org",
    display_name: _lt("Org Chart"),
    icon: "fa fa-sitemap",
    multiRecord: true,
    Controller: OrgChartController,
    Renderer: OrgChartRenderer,
    Model: OrgChartModel,
    SearchModel: SearchModel,
    searchMenuTypes: ["filter", "groupBy", "comparison", "favorite"],
    buttonTemplate: "to_org_chart.OrgChart.Buttons",

    props: (genericProps, view) => {
        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            buttonTemplate: view.buttonTemplate,
            direction: 't2b',
        };
    },
};

viewRegistry.add("org", orgChartView);
