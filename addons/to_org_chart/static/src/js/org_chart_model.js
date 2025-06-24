/** @odoo-module **/

import { Model } from "@web/views/model";

export class OrgChartModel extends Model {
    /**
     * @override
     * @param {Widget} parent
     */
    setup(params) {
        this.data = null;
        this.metaData = params;
        this.searchParams = null;
    }

    async load(searchParams) {
        this.searchParams = searchParams;
        const metaData = this._buildMetaData();
        this.data = await this._loadDataNode(metaData);
    }

    /**
     * @protected
     * @param {Object} [params={}]
     * @returns {Object}
     */
    _buildMetaData(params) {
        const { domain, context, groupBy } = this.searchParams;
        const metaData = Object.assign({}, this.metaData, { context });
        metaData.domain = domain;
        metaData.groupBy = groupBy.length ? groupBy : [];
        return Object.assign(metaData, params);
    }

    async _loadDataNode(params) {
        this.domain = params.domain || this.domain || [];
        var context = params.context || {};
        if (this.domain) {
            context.org_chart = true;
        }
        this.resModel = params.resModel || this.resModel || "";
        return await this.orm.call(this.resModel, "search_read", [], {
            fields: [],
            domain: this.domain,
            context: context
        })
    }
}

