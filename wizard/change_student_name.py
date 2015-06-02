import wizard
import time
import netsvc
import osv
import pooler
from osv import fields, osv, orm

change_student_name_form='''<?xml version="1.0"?>
<form title="Resource detail">
    <seperator string="Resource detail" colspan="4"/>
    <field name="catagory"/>
    <newline/>
    <field name="resource_name"/>
 </form>'''

change_student_name_fields={
     'catagory': {'string':'Catagory','type':'many2one','relation':'lms.categories'},
     'resource_name':{'string':'Resource Name','type':'many2many','relation':'lms.resource'},
     #'resource_name':{'string':'Resource Name','type':'char'},
   }

class wizard_change_student_name(wizard.interface):
    def change_name(self, cr, uid, data, context):
        current_id = data['form']['catagory']
        catagory = pooler.get_pool(cr.dbname).get('lms.categories').browse(cr,uid,current_id).type
        #result = data['form']['resource_name']
        ids = pooler.get_pool(cr.dbname).get('lms.resource').search(cr, uid,[('catagory_id','=',catagory)])
        rec_resources = pooler.get_pool(cr.dbname).get('lms.resource').browse(cr, uid, ids)
        for identities in rec_resources:
            recdict = {'name_resource':'','publication':'','accession_nummber':''}
            recdict['name_resource'] = identities.name
            recdict['publication'] =identities.dop
            acc_ids = pooler.get_pool(cr.dbname).get('lms.cataloge').search(cr, uid,[('resource_no','=',recdict['name_resource'])])
            rec_accession_number = pooler.get_pool(cr.dbname).get('lms.cataloge').browse(cr,uid,acc_ids)
            recdict['accession_number'] = rec_accession_number.accession_no
            print "accession_no=",recdict['accession_number'],"resource name=",recdict['name_resource'],"publication=",recdict['publication']
    states = {
                'init':{    
                 'actions' :[],
                 'result':{'type':'form', 'arch':change_student_name_form, 'fields':change_student_name_fields, 'state':[('end','Cancel','gtk-cancel'), ('change','Change')]}
                },
                'change': {
                   'actions':[],
                   'result':{'type':'print', 'report':'student_record','state':'end'}
                },
            }
wizard_change_student_name("wizard_change_student_name")