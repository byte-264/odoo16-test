/** @odoo-module */

import { _lt } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";

const { Component } = owl;

export class PdfOptionsModal extends Component {
}

PdfOptionsModal.components = { Dialog }
PdfOptionsModal.template = "pdf_to_print_options.ButtonOptions";
