from lxml.builder import E

from odoo import models, api, _


class BaseModel(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _get_default_org_view(self):
        """ Generates a default org view, based on _rec_name.

        This method is automatically triggered each time the `_fields_view_get()` is called

        :returns: a org view as an lxml document
        :rtype: etree._Element
        """
        return E.org(string=self._description)

    @api.model
    def _get_org_public_data(self, record_data):
        # Allow reading some public information to avoid broken org chart
        data = {}
        for key in ['id', 'year', 'quarter', 'time_frame', 'quarter_full_name', 'mode', 'state', 'company_id', 'parent_id', 'child_ids', 'recursive_child_ids']:
            data[key] = record_data[key]
        data['display_name'] = data['name'] = _('You are not allowed to access')
        return data

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        """
        Override to return data for parent records too
        """
        if self._context.get('org_chart', False) and 'parent_id' in self._fields:
            records = self.search(domain or [], offset, limit, order)
            if records:
                domain = [('id', 'parent_of', records.ids)]

                allowed_ids = [d['id'] for d in super(BaseModel, self).search_read(domain, ['id'], offset, limit, order, **read_kwargs)]

                all_data = super(BaseModel, self.sudo()).search_read(domain, fields, offset, limit, order, **read_kwargs)
                # Delete all private information, only allow reading some public information to avoid broken org chart
                for d in all_data:
                    if d['id'] not in allowed_ids:
                        all_data[all_data.index(d)] = self._get_org_public_data(d)
                return all_data
        return super(BaseModel, self).search_read(domain, fields, offset, limit, order, **read_kwargs)
