/**@odoo-module**/

const { Component, useEffect, useRef, onWillUnmount, onWillStart } = owl;
import { _lt } from "@web/core/l10n/translation";
import { qweb } from 'web.core';

const loadScript = (FILE_URL, scriptEle, async = false, type = "text/javascript") => {
    return new Promise((resolve, reject) => {
        try {
            scriptEle.type = type;
            scriptEle.async = async;
            scriptEle.src = FILE_URL;
            scriptEle.addEventListener("load", (ev) => {
                resolve({ status: true });
            });

            scriptEle.addEventListener("error", (ev) => {
                reject({
                    status: false,
                    message: `Failed to load the script ＄{FILE_URL}`,
                });
            });

            document.body.appendChild(scriptEle);
        } catch (error) {
            reject(error);
        }
    });
};


export class OrgChartRenderer extends Component {
    setup() {
        this.model = this.props.model;
        this.chart = null;
        this.update = this.model.update;
        this.to_org_chart = useRef('to_org_chart');
        this._renderOrgChart = this._renderOrgChart.bind(this);
        this.props.setFunChangeDirection(this._renderOrgChart);

        onWillStart(async () => await this._loadscript());
        useEffect(() => this._renderOrgChart('t2b'));
        onWillUnmount(this.onWillUnmount);
    }
    /**
    *
    * @private
    * @param {MouseEvent} ev
    */
    _onNodeClicked(ev) {
        ev.preventDefault();
        var node_body = $(ev.currentTarget).closest('.node_content').find('.node_body');
        var record_id = node_body.data('record-id');
        if (record_id) {
            this.props.openRecord(record_id)
        }
    }

    // Using arrow function to bind this method
    _renderOrgChart(direction) {
        if (!this.to_org_chart || !this.to_org_chart.el || !$(this.to_org_chart.el).orgchart) {
            return;
        }
        var nodeRefs = [];
        var yearNodes = [];
        var childNodes = [];
        var nodeTryTimes = {};
        this.removeChart();
        this.direction = direction;
        // create a clone of records
        var records = this.model.data.slice();
        while (records.length > 0) {
            // get first item in list
            var record = records.shift();
            // create default node
            var children = nodeRefs.find(n => n.record.id == record.id);
            var node = {
                'type': 'record',
                'name': record.name,
                'record': record,
                'className': 'record_node',
                'children': children != undefined ? children.children : []
            }
            // add new year node if not exist
            var yearNode = yearNodes.find(n => n.year == record.year)
            if (yearNode == undefined) {
                yearNode = {
                    'type': 'year',
                    'name': _lt('Year ') + record.year,
                    'year': record.year,
                    'className': 'year_node',
                    'children': []
                };
                yearNodes.push(yearNode);
            }
            // check for where to add current node
            if (!record.parent_id) {
                // if this node set quarter
                if (record.quarter) {
                    // then it should be child of quarter node of this year
                    var foundQNode = false;
                    yearNode.children.forEach(quarterNode => {
                        // find correct quarter node and set it as children
                        if ('quarter' in quarterNode && quarterNode.quarter == record.quarter) {
                            quarterNode.children.push(node);
                            foundQNode = true;
                        }
                    });
                    // create new quarter node if it is not exist
                    if (!foundQNode) {
                        yearNode.children.push({
                            'type': 'quarter',
                            'name': _lt('Quarter ') + (parseInt(record.quarter) + 1),
                            'quarter': record.quarter,
                            'className': 'quarter_node',
                            'children': [node]
                        });
                    }
                } else {
                    // if it is not set quarter then it should be objective of year
                    // and directly added to year
                    yearNode.children.push(node)
                    childNodes.push(node)
                }
            } else {
                // if record have parent then we need to find parent in list
                var parent_node = nodeRefs.find(n => n.record.id == record.parent_id[0])
                if (parent_node != undefined) {
                    // add this node to it's parent node
                    parent_node.children.push(node);
                } else {
                    // in case of parent node not found, there is maybe parent node is not processed in list
                    // so we just push this record back to list
                    if (record.id in nodeTryTimes) {
                        // we continue here as we do not want push it again to nodeRefs
                        // and also we avoid it push it again to records
                        // TODO: what to do with this record ?
                        console.warn(`Record: ${record} parent is not found. What should we do with this record?`)
                        continue;
                    } else {
                        records.push(record);
                        nodeTryTimes[record.id] = 1;
                    }
                }
            }
            // store in nodeRefs for quick reference later when we find for parent
            nodeRefs.push(node)
        }
        // only continue to generate chart in case we have data
        if (yearNodes.length > 0) {
            // create virtual company node
            var data = {
                'type': 'company',
                'name': '',
                'children': record.year ? yearNodes : childNodes,
                'className': 'company_node',
            };
            var checkMultiCompany = this._checkMultiCompany();

            if (checkMultiCompany) {
                data.name = _lt('All companies');
            } else {
                data.name = nodeRefs[0].record.company_id ? nodeRefs[0].record.company_id[1] : _lt('ORG CHART');
            }

            var nodeTemplate = data => { return this._getNodeTemplate(data); };

            this._initOrgChat(data, nodeTemplate);
            $(this.to_org_chart.el).find('.node_content').on('click', this._onNodeClicked.bind(this));
        }
    }

    _checkMultiCompany() {
        var company_ids = [];
        this.model.data.forEach(function (record) {
            if (record.company_id && !company_ids.includes(record.company_id[0])) {
                company_ids.push(record.company_id[0]);
            }
        });
        return company_ids.length > 1;
    }

    /**
    * initialize org chart
    *
    * @private
    */
    _initOrgChat(data, nodeTemplate) {
        if (this.to_org_chart.el) {
            this.chart = $(this.to_org_chart.el).orgchart({
                'data': data,
                'pan': true,
                'zoom': true,
                'zoomoutLimit': -0.1,
                'chartClass': 'to_org_chart',
                'toggleSiblingsResp': false,
                'direction': this.direction,
                'nodeTemplate': nodeTemplate,
                'className': '',
                'initCompleted': () => {
                    $('[data-toggle="popover"]').popover();
                }
            });
        }
    }

    /**
    * get node template for rendering
    *
    * @private
    */
    _getNodeTemplate(node) {
        var nodeClass = 'node_content ';

        if (node.type == 'company') {
            nodeClass += 'company_node_content';
        } else if (node.type == 'year') {
            nodeClass += 'year_node_content';
        } else if (node.type == 'quarter') {
            nodeClass += 'quarter_node_content';
        }
        var progress = 0;
        var progressColor = 'bg-danger';
        if (node.type == 'record') {
            progress = Math.max(0, Math.min(100, Math.floor(node.record.points * 100)))
            if (node.record.result == 'successful') {
                progressColor = 'bg-success';
            }
        }
        var departmentName = '';
        if (node.type == 'record') {
            if (node.record.mode == 'department') {
				departmentName = node.record.department_id ? node.record.department_id[1] : false;
            } else if (node.record.mode == 'employee') {
				departmentName = node.record.user_id ? node.record.user_id[1] : false;
            } else if (node.record.mode == 'company') {
                departmentName = _lt('Company Objective');
            }
        }
        var node = qweb.render('to_org_chart.OrgChartNodeTemplate', {
            node: node,
            nodeClass: nodeClass,
            progress: progress,
            progressClass: `progress-bar ${progressColor}`,
            departmentName: departmentName,
        })
        return node;
    }
    async _loadscript() {
        if (window.Chart) {
            this.originChart = window.Chart;
        }
        this.scriptHtml2canvas = document.createElement("script");
        this.scriptChartjsOrg = document.createElement("script");
        await loadScript("/to_org_chart/static/lib/html2canvas/html2canvas.min.js", this.scriptHtml2canvas);
        await loadScript("/to_org_chart/static/lib/orgchart/jquery.orgchart.js", this.scriptChartjsOrg);
        this._renderOrgChart('t2b');
    }
    removeChart() {
        // Delete old element
        $(this.to_org_chart.el).empty();
        // When the user clicks the rotate button, the system will clear the org chart. 
        // This is because the events of the old chart are not automatically unbound. 
        // Therefore, we need to unbind the events of the chart.
        if (!this.chart || !this.chart.$chart) {
            return;
        }
        this.chart.unbindZoom();
        this.chart = null;
    }
    onWillUnmount() {
        this.scriptHtml2canvas.remove();
        this.scriptChartjsOrg.remove();
        if (this.originChart) {
            window.Chart = this.originChart;
        }
    }
}
OrgChartRenderer.template = "to_org_chart.OrgChartRender";
