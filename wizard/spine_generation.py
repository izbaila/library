import wizard
import time
import netsvc
import osv
import pooler
from osv import fields, osv, orm

change_student_name_form='''<?xml version="1.0"?>
<form title="Spine generation">
    <separator string="Spine eneration" colspan="4"/>
    <field name="catagory"/>
 </form>'''

change_student_name_fields={
     'catagory': {'string':'Catagory','type':'many2one','relation':'lms.categories'},
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