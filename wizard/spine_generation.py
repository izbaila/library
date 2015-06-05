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

class wizard_spine_generation(wizard.interface):
    
    states = {
                'init':{    
                 'actions' :[],
                 'result':{'type':'form', 'arch':change_student_name_form, 'fields':change_student_name_fields, 'state':[('end','Cancel','gtk-cancel'), ('generate','Generate')]}
                },
                'generate': {
                   'actions':[],
                   'result':{'type':'print', 'report':'spine_generation','state':'end'}
                },
            }
wizard_spine_generation("wizard_spine_generation")