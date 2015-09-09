import wizard
import time
import netsvc
import osv
import pooler

_change_student_name_form='''<?xml version="1.0"?>
<form title="changing student name">
    <seperator string="change student name" colspan="4"/>
    <field name="category"/>
</form>'''

_change_student_name_fields={
     'category': {'string':'Category','type':'many2one','relation':'lms.categories','required':True},
    }

class wizard_resource_detail(wizard.interface):
    states = {
    'init': {
        'actions':[],
        'result' : {'type' : 'form','arch':_change_student_name_form,'fields':_change_student_name_fields,'state':[('end','Cancel'),('print','print')]}
        }, 

    'print': {
        'actions':[],
        #'result':{'type':'state','state':'end'}  #for generating wizard
        'result':{'type':'print','report': 'resource_detail','state':'end'} #for generating report
        }
    }
wizard_resource_detail("wizard_resource_detail")