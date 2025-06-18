/** @odoo-module **/

import { ActionMenus } from "@web/search/action_menus/action_menus";
import { Layout } from "@web/search/layout";
import { standardViewProps } from "@web/views/standard_view_props";
import { ViewButton } from "@web/views/view_button/view_button";
import { Component } from "@odoo/owl";

import { useModel } from "@web/views/model";
import { useService } from "@web/core/utils/hooks";

export class OrgChartController extends Component {
  setup() {
    this.actionService = useService("action");
    let modelParams = {};
    if (this.props.state) {
      modelParams.data = this.props.state.data;
      modelParams.metaData = this.props.state.metaData;
    } else {
      modelParams = {
        resModel: this.props.resModel,
      };
    }

    this.model = useModel(this.props.Model, modelParams);
    this.setFunChangeDirection = this.setFunChangeDirection.bind(this);
  }
  openRecord(record_id) {
    this.actionService.doAction({
      type: "ir.actions.act_window",
      res_model: this.model.resModel,
      views: [[false, "form"]],
      res_id: record_id,
      view_mode: "form",
    });
  };
  onClickRotateRight() {
    switch (this.props.direction) {
      case 't2b':
        this.props.direction = 'l2r'
        break;
      case 'l2r':
        this.props.direction = 'b2t'
        break;
      case 'b2t':
        this.props.direction = 'r2l'
        break;
      case 'r2l':
        this.props.direction = 't2b'
        break;
    }
    this.funChangeDirection(this.props.direction);
  }
  onClickRotateLeft() {
    switch (this.props.direction) {
      case 't2b':
        this.props.direction = 'r2l'
        break;
      case 'r2l':
        this.props.direction = 'b2t'
        break;
      case 'b2t':
        this.props.direction = 'l2r'
        break;
      case 'l2r':
        this.props.direction = 't2b'
        break;
    }
    this.funChangeDirection(this.props.direction);
  }
  setFunChangeDirection (funChangeDirection) {
    this.funChangeDirection = funChangeDirection;
  }
}
OrgChartController.template = `to_org_chart.OrgChartController`;
OrgChartController.components = { ActionMenus, Layout, ViewButton };

OrgChartController.props = {
  ...standardViewProps,
  direction: String,
  Model: Function,
  Renderer: Function,
  buttonTemplate: String,
};
