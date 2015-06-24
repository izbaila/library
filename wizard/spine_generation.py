import wizard
import time
import netsvc
import osv
import pooler
from osv import fields, osv, orm

change_student_name_form = '''<?xml version="1.0"?>
<form string="Changing Name">
    <separator string="Name Changing Form" colspan="4"/>
    <field name="catagory"/>
    <newline/>
    <field name="check_box"/>
    <newline/>
</form>'''
    
success_message_form = '''<?xml version="1.0"?>
<form string="Changing Name">
    <separator string="Catalogued REsources" colspan="4"/>
    <field name="resource"/>
   </form>'''

success_message_fields = {
    'resource': {'string':'Catalogued Resource','type':'many2many','relation':'lms.resource'},
    }
    
change_student_name_fields = {
                               
   'catagory': {'string':'Catagory','type':'many2one','relation':'lms.categories'},
   'check_box' : {'string':'Proceed' , 'type':'boolean'},
}

failure_message_form = '''<?xml version = "1.0"?>
<form string="Failure Message">
    <separator string="Failure" colspan="4"/>
</form>'''

failure_message_fields = {}     

class wizard_spine_generation(wizard.interface):
    
    def change_name(self,cr,uid,data,context):
        cata = data['form']['catagory']
        ck_box = data['form']['check_box']
        if ck_box:
            return 'success'
        else:
            return 'failure'
 
    def spine(self,cr,uid,data,context):
        
        cata = data['form']['resource']
        print "resources that are selected from the resource table in next step are=",cata
        if cata:
            return 'failure'
       
    states = {
                'init':{    
                 'actions' :[],
                 'result':{'type':'form', 'arch':change_student_name_form, 'fields':change_student_name_fields, 'state':[('end','Cancel','gtk-cancel'), ('Next','Next')]}
                },
                'Next': {
                   'actions':[],
                   'result':{'type':'choice' , 'next_state':change_name}
                },
                'success':{
                    'actions':[],
                    'result':{'type':'form', 'arch':success_message_form, 'fields':success_message_fields, 'state':[('end','Cancel','gtk-cancel'), ('Generate','Generate')]}
                },
                'failure':{
                    'actions':[],
                    'result':{'type':'form', 'arch':failure_message_form, 'fields':failure_message_fields, 'state':[('end','Cancel')]}
                },
                'Generate':{
                    'actions':[],
                   # 'result':{'type':'choice' , 'next_state':spine}
                    'result' :{'type':'print','report': 'spine_generation','state':'end'} #for generating report
                },
            }
wizard_spine_generation("wizard_spine_generation")