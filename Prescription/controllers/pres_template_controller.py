from odoo import http
from odoo.http import request
import json
import importlib
from datetime import datetime,date
from json import JSONEncoder
import dateutil.parser
from odoo.addons.Prescription.controllers.login_controller import validate_token
 


class PrestemplateController(http.Controller):
    @validate_token
    @http.route('/fetchprestemplate', type='http', method=['GET'])
    def get_pres_template(self):
        try:
            pres_template_rec = http.request.env['prescription.templates'].search([])
            pres_template_list = []
            for prestemplate in pres_template_rec:
                vals ={
                    'id':prestemplate.id,
                    'name':prestemplate.name
                } 
                pres_template_list.append(vals)
            data = {'Code':0,'Message':'Retrieve all prescription template Records' ,'Result': pres_template_list}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"something is wrong"}


    @validate_token
    @http.route('/prestemplate', type='json',method=['POST'],csrf=False)
    def create_pres_template(self, **rec):
        try:
            if request.jsonrequest:
                data = request.jsonrequest
                if data['name']:
                    vals={
                        'name':data['name']
                    }
            new_data = http.request.env['prescription.templates'].sudo().create(vals)
            print("****new_data******",new_data)
            args = {'Code':0, 'Message':'new created record successfully added in prescripion template','Result':new_data.id}
            return args
        except Exception as e:
            return {'Code':1,'Message':"something is wrong"}


    @validate_token
    @http.route('/updateprestemplate',type="http",method=['PUT'],csrf=False)
    def update_pres_tempalte(self, **rec):
        try:
            if request.httprequest:
                if rec['id']:
                    print("**********id*********",rec)
                    update_data = request.env['prescription.templates'].sudo().search([('id','=',rec['id'])])
                    if update_data:
                        update_data.sudo().write(rec)
                        print("********",update_data)
                    data = {'Code':0,'Message':'Successfully record is updated','Result':rec['id']}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}


    @validate_token
    @http.route('/delete_pres_temp/<int:rec_id>',type="http",method=['DELETE'],csrf=False)
    def delete_pres_template(self, rec_id):
        try:
            pres_template_rec = request.env['prescription.templates'].sudo().browse(rec_id)
            id = pres_template_rec.id
            pres_template_rec.unlink()
            data  = {'Code':0,'Message':'Successfully record is deleted','Result':id}
            return json.dumps(data)
        except Exception as e:
            return {'Code':1,'Message':"id is wrong"}
            