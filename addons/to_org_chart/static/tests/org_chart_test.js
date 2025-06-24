/** @odoo-module **/

import { getFixture, click, triggerEvent } from "@web/../tests/helpers/utils";
import { makeView, setupViewRegistries } from "@web/../tests/views/helpers";
import { session } from "@web/session";
import { data_q3, data_q3q4 } from "./helpers/sample_data"
import { registry } from "@web/core/registry";

var data = null;
var target = null;
function _preventScroll(ev) {
    ev.stopImmediatePropagation();
}
/*
* recursively loop each tables from top to bottom in org chart and get direct children table
* to count the level of org chart
*/
function getDeepestLevelOrgChart(tables, initLevel) {
    var directCollection = [];
    for (var i = 0; i < tables.length; i++) {
        var directChild = $(tables[i]).find('> .hierarchy > .nodes');
        if (directChild.length > 0) {
            directCollection.push(directChild);
        }
    }
    if (directCollection.length == 0) {
        return initLevel;
    }
    return getDeepestLevelOrgChart(directCollection, initLevel + 1);
}

function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
function getRecordByDomain(records, domain) {
    if (domain.length == 0) {
        return records;
    }
    let listReturns = [];
    let record, key, op, value;
    for (var i = 0; i < records.length; i++) {
        record = records[i];
        for (var j = 0; j < domain.length; j++) {
            key = domain[j][0];
            op = domain[j][1];
            if (op == '=') {
                op = '==';
            }
            value = domain[j][2];
            if (record[key]) {
                if (parseFloat(record[key])) {
                    if (eval(`${record[key]} ${op} ${value}`)) {

                        listReturns.push(record);
                    }
                }
                else {
                    if (eval(`"${record[key]}" ${op} "${value}"`)) {
                        listReturns.push(record);
                    }
                }
            }
        }
    }
    return listReturns;
}
async function makeOrgView(data, searchViewArch = '', context = {}) {
    await makeView({
        type: "org",
        resModel: "okr",
        serverData: { models: data },
        arch: '<tree><field name="name"/></tree>',
        resId: 2,
        searchViewArch: searchViewArch,
        context: context,
        mockRPC(route, args) {
            if (route === "/web/dataset/call_kw/okr/search_read") {
                return Promise.resolve(getRecordByDomain(data.okr.records, args.kwargs.domain));
            }
        },
    })
}

function zoomThenCompare(assert) {
    var transform_befor_wheel = document.querySelector('.to_org_chart').style.transform;
    document.querySelector('.to_org_chart').dispatchEvent(new Event('wheel', { "bubbles": true, "cancelable": false }));
    var transform_after_wheel = document.querySelector('.to_org_chart').style.transform;
    assert.notEqual(transform_befor_wheel, transform_after_wheel,
        'The transform of before should be different from transform of after when trigger wheel event');
}
QUnit.module('to_org_chart', (hooks) => {
    hooks.beforeEach(() => {
        target = getFixture();
        window.addEventListener('scroll', _preventScroll, true);
        session.uid = -1;
        data = {
            'okr': {
                fields: {
                    id: { string: "ID", type: "integer" },
                    name: { string: "name", type: "char" },
                    display_name: { string: "display name", type: "char" },
                    year: { string: "year", type: "char" },
                    quarter: {
                        string: "quarter", type: "selection", selection: [
                            ['0', 'Q1'],
                            ['1', 'Q2'],
                            ['2', 'Q3'],
                            ['3', 'Q4'],
                        ]
                    },
                    time_frame: { string: "time frame", type: "char" },
                    quarter_full_name: { string: "quarter full name", type: "char" },
                    description: { string: "description", type: "text" },
                    mode: {
                        string: "mode", type: "selection", selection: [
                            ['company', 'Company'],
                            ['department', 'Department'],
                            ['employee', 'Employee'],
                        ]
                    },
                    type: {
                        string: "type", type: "selection", selection: [
                            ['committed', 'Committed'],
                            ['aspirational', 'Aspirational'],
                        ]
                    },
                    state: {
                        string: "state", type: "selection", selection: [
                            ['draft', 'Draft'],
                            ['confirmed', 'Confirmed'],
                            ['cancelled', 'Cancelled'],
                        ]
                    },
                    result: {
                        string: "result", type: "selection", selection: [
                            ['successful', 'Successful'],
                            ['failed', 'Failed'],
                        ]
                    },
                    company_id: { string: "company id", type: "many2one", relation: 'company' },
                    department_id: { string: "department id", type: "many2one", relation: 'department' },
                    employee_id: { string: "employee id", type: "many2one", relation: 'employee' },
                    owner: { string: "owner", type: "char" },
                    user_id: { string: "user id", type: "many2one", relation: 'user' },
                    parent_id: { string: "parent id", type: "many2one", relation: 'okr' },
                    child_ids: { string: "child ids", type: "one2many", relation: 'okr' },
                    key_results_count: { string: "key results count", type: "integer" },
                    recursive_child_ids: { string: "key results count", type: "many2many", relation: 'okr' },
                    points: { string: "points", type: "float" },
                    progress: { string: "progress", type: "float" },
                    weight: { string: "weight", type: "float" },
                    okr_success_points_threshold: { string: "okr coefficient", type: "float" },
                    create_uid: { string: "create uid", type: "many2one", relation: 'user' },
                    create_date: { string: 'create date', type: 'datetime' },
                    write_uid: { string: 'write uid', type: 'datetime' },
                    write_date: { string: 'write date', type: 'datetime' },
                    __last_update: { string: 'last update', type: 'datetime' },
                },
                records: data_q3,
            },
            'company': {
                fields: {
                    id: { string: "ID", type: "integer" },
                    name: { string: "name", type: "char" },
                },
                records: [
                    { id: 4, name: 'Example Company for OKR' }
                ]
            },
            'department': {
                fields: {
                    id: { string: "ID", type: "integer" },
                    name: { string: "name", type: "char" },
                },
                records: []
            },
            'employee': {
                fields: {
                    id: { string: "ID", type: "integer" },
                    name: { string: "name", type: "char" },
                },
                records: [
                    { id: 3572, name: 'Owner Example Company' },
                ]
            },
            'user': {
                fields: {
                    id: { string: "ID", type: "integer" },
                    name: { string: "name", type: "char" },
                },
                records: [
                    { id: 2, name: 'Mitchell Admin' },
                ]
            }
        };
        setupViewRegistries();
    })
    hooks.afterEach(() => {
        window.removeEventListener('scroll', _preventScroll, true);
    })
    QUnit.module('OrgChartView');

    odoo.session_info = {};
    odoo.session_info.user_context = {};

    QUnit.test('TC01: Q3 rendering test', async function (assert) {
        assert.expect(2);
        await makeOrgView(data);

        assert.equal(target.getElementsByClassName('node').length, 16, 'Number of okr node should be 16');
        var superParentTable = $('.to_org_chart > .nodes');
        var depestLevel = getDeepestLevelOrgChart(superParentTable, 1);
        assert.equal(depestLevel, 7, 'The whole level should be 7');
    });
    QUnit.test('TC02:Q3, Q4 rendering test', async function (assert) {
        assert.expect(2);
        data.okr.records = data_q3q4;
        await makeOrgView(data);

        assert.equal(target.getElementsByClassName('node').length, 20, 'Number of okr node should be 20');
        var superParentTable = $('.to_org_chart > .nodes');
        var depestLevel = getDeepestLevelOrgChart(superParentTable, 1);
        assert.equal(depestLevel, 7, 'The whole level should be 7');
    });

    QUnit.test('TC03: Q3, Q4 filter for Q4', async function (assert) {
        assert.expect(2);
        data.okr.records = data_q3q4;
        const searchViewArch = `
        <search>
        <filter name="q4_okr" string="Q4"  domain="[('quarter', '=', '3')]"/>
        </search>`;
        const context = {
            search_default_q4_okr: true
        }
        await makeOrgView(data, searchViewArch, context);

        assert.equal(target.getElementsByClassName('node').length, 6, 'Number of okr node should be 6');
        var superParentTable = $('.to_org_chart > .nodes');
        var depestLevel = getDeepestLevelOrgChart(superParentTable, 1);
        assert.equal(depestLevel, 5, 'The whole level should be 5');
    });
    QUnit.test('TC04: Q3, Q4 filter for successfull result', async function (assert) {
        assert.expect(2);
        data.okr.records = data_q3q4;
        const searchViewArch = `
        <search>
        <filter name="result_okr" string="Successfull" domain="[('result', '=', 'successful')]"/>
        <filter name="q4_okr" string="Q4" domain="[('quarter', '=', '3')]"/>
        </search>`;
        const context = {
            search_default_result_okr: true
        }
        await makeOrgView(data, searchViewArch, context);

        assert.equal(target.getElementsByClassName('node').length, 2, 'Number of okr node should be 2');
        var superParentTable = $('.to_org_chart > .nodes');
        var depestLevel = getDeepestLevelOrgChart(superParentTable, 1);
        assert.equal(depestLevel, 2, 'The whole level should be 2');
    });
    QUnit.test('TC05: Q3 rendering and click the node', async function (assert) {
        assert.expect(3);
        data.okr.records = data_q3;
        const orgChartView = registry.category("views").get("org");
        class OrgViewCustom extends orgChartView.Controller {
            openRecord(record_id) {
                assert.step("openRecord");
                assert.strictEqual(record_id, 1);
            }
        }
        registry.category("views").add(
            "org",
            {
                ...orgChartView,
                Controller: OrgViewCustom,
            },
            { force: true }
        );

        await makeOrgView(data);
        await click(target.querySelector('.node.record_node>.node_content '))
        assert.verifySteps(["openRecord"]);
    });
    QUnit.test('TC07: Q3 rendering and test wheel event to scale chart', async function (assert) {
        assert.expect(1);
        data.okr.records = data_q3;
        await makeOrgView(data);
        zoomThenCompare(assert);
    });
    QUnit.test('TC08: Q3 Q4 test with button arrow in the node of org chart', async function (assert) {
        assert.expect(5);
        data.okr.records = data_q3q4;
        await makeOrgView(data);

        assert.ok("Testing with node have record id = 7 in sample data");
        // test with the node have record id = 7
        const node = document.querySelector("[data-record-id='7']");
        await triggerEvent(node, null, "mouseover");
        // b1
        await click(target.querySelector('.rightEdge.oci-chevron-left'));
        await timeout(500);
        assert.equal($('.node:not(.slide-left)').length, 17, 'Total should be 17 slide in left node');
        // b2
        await triggerEvent(node, null, "mouseover");
        await click(target.querySelector('.rightEdge.oci.oci-chevron-right'))
        await timeout(500);
        assert.equal($('.node:not(.slide-left)').length, 20, 'Total should be 20 slide out left node');
        //b3
        await triggerEvent(node, null, "mouseover");
        await click(target.querySelector('.topEdge.oci.oci-chevron-down'));
        await timeout(500);
        assert.equal($('.node.slide-up, .node.slide-left, .node.slide-down, .node.slide-right').length, 16,
            'Total should be 16 slide in all around node except children');
        // b4
        await triggerEvent(node, null, "mouseover");
        await click(target.querySelector('.topEdge.oci-chevron-up'));
        await timeout(500);
        assert.equal($('.node.slide-up, .node.slide-left, .node.slide-down, .node.slide-right').length, 15,
            'Total should be 15 slide in all around node except children');
    });
    QUnit.test('TC09: Q3, Q4 rendering and test progress', async function (assert) {
        assert.expect(1);
        data.okr.records = data_q3q4;
        await makeOrgView(data);

        // test with the node have record id = 4
        const node = $(document.querySelector("[data-record-id='4']")).parents('.node');
        var progress = node.find('.progress .progress-bar');
        assert.equal(progress.hasClass('bg-danger'), true,
            'Progress bar should have bg-danger class');
    });
    QUnit.test('TC12: Q3, Q4 rendering and change node with id 1 to Q4', async function (assert) {
        assert.expect(4);
        data.okr.records = data_q3q4;
        for (var i = 0; i < data.okr.records.length; i++) {
            var r = data.okr.records[i];
            if (r.id == 1) {
                assert.equal(r.quarter, "2", "The node 'Hoàn thiện hệ thống SaaS Website Sales' should be 2 at first");
                assert.notOk($(".quarter_node:contains('4')").closest('table').find('[data-record-id=1]').length,
                    "The node 'Hoàn thiện hệ thống SaaS Website Sales' should not exist in Quarter 4 ");
                data.okr.records[i].quarter = "3";
                assert.ok(data.okr.records[i].quarter == "3", "Change 'Hoàn thiện hệ thống SaaS Website Sales' to Q4");
                break;
            }
        }
        await makeOrgView(data);
        assert.ok($(".quarter_node:contains('4')").parents('.nodes').find('[data-record-id=1]').length,
            "The node 'Hoàn thiện hệ thống SaaS Website Sales' should exist in Quarter 4");
    });
    QUnit.test('TC13: Q3 rotate then zoom', async function (assert) {
        assert.expect(2);
        data.okr.records = data_q3;
        await makeOrgView(data);

        await click(target.querySelector('.fa-rotate-right'));
        await timeout(500);
        zoomThenCompare(assert);

        await click(target.querySelector('.fa-rotate-left'));
        await timeout(500);
        zoomThenCompare(assert);
    });

});
