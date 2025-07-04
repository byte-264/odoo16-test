from odoo import http
from odoo.http import request
import base64

class HrAttendanceFaceRecognition(http.Controller):
    
    @http.route('/hr_attendance_controls_pro/loadLabeledImages/', type='json', auth="user")
    def load_labeled_images(self):
        import logging
        _logger = logging.getLogger(__name__)
        
        descriptions = []
        employees = request.env['hr.employee'].sudo().search([])
        _logger.info(f"Found {len(employees)} employees")
        
        for employee in employees:
            descriptors = []
            _logger.info(f"Processing employee: {employee.name} (ID: {employee.id})")
            _logger.info(f"Employee has {len(employee.user_faces)} faces")
            
            for faces in employee.user_faces:
                _logger.info(f"Face ID: {faces.id}, has descriptor: {bool(faces.descriptor)}, descriptor length: {len(faces.descriptor) if faces.descriptor else 0}")
                if faces.descriptor and faces.descriptor != 'false':
                    descriptors.append(faces.descriptor)
                    
            if descriptors:
                vals = {
                    "label": employee.id,
                    "descriptors": descriptors,
                    "name": employee.name,
                }
                descriptions.append(vals)
                _logger.info(f"Added employee {employee.name} with {len(descriptors)} descriptors")
            else:
                _logger.info(f"No valid descriptors for employee {employee.name}")
                
        _logger.info(f"Returning {len(descriptions)} employees with descriptors")
        return descriptions
    
    @http.route('/hr_attendance_controls_pro/getName/<int:employee_id>/', type='json', auth="user")
    def get_name(self,employee_id):
        name = False
        if employee_id:
            employee = request.env['hr.employee'].sudo().search([('id', '=', int(employee_id))])
            name =  employee.name
        return name
