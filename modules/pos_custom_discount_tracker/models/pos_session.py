from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    def _loader_params_res_partner(self):
        """Enhanced partner loading for employee selection"""
        result = super()._loader_params_res_partner()
        
        # Just use existing fields - no new ones
        if 'search_params' in result:
            # Add more fields for better employee identification
            existing_fields = result['search_params'].get('fields', [])
            additional_fields = ['function', 'email', 'phone', 'category_id', 'parent_id']
            
            for field in additional_fields:
                if field not in existing_fields:
                    existing_fields.append(field)
            
            result['search_params']['fields'] = existing_fields
        
        return result
    
    def _pos_data_process(self, loaded_data):
        """Process and organize partner data for POS"""
        super()._pos_data_process(loaded_data)
        
        if 'res.partner' in loaded_data:
            partners = loaded_data['res.partner']
            
            # Create a filtered list of employees/contacts suitable for selection
            pos_employees = []
            
            for partner in partners:
                # Include individual people with contact info
                if (not partner.get('is_company', True) and 
                    (partner.get('email') or partner.get('function') or partner.get('phone'))):
                    
                    # Enhance partner data for better display
                    display_name = partner['name']
                    if partner.get('function'):
                        display_name += f" ({partner['function']})"
                    elif partner.get('email'):
                        display_name += f" ({partner['email']})"
                    
                    pos_employees.append({
                        'id': partner['id'],
                        'name': partner['name'],
                        'display_name': display_name,
                        'function': partner.get('function', ''),
                        'email': partner.get('email', ''),
                        'phone': partner.get('phone', ''),
                    })
            
            # Add some default employees if none found
            if len(pos_employees) == 0:
                pos_employees = [
                    {'id': 1, 'name': 'Administrator', 'display_name': 'Administrator (System)', 'function': 'System Admin'},
                    {'id': 2, 'name': 'Manager', 'display_name': 'Manager (Store)', 'function': 'Store Manager'},
                    {'id': 3, 'name': 'Staff', 'display_name': 'Staff (Sales)', 'function': 'Sales Associate'},
                ]
            
            # Store the processed employee list
            loaded_data['pos_employees'] = pos_employees
            print(f"Processed {len(pos_employees)} employees for POS selection")
            