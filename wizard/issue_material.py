import wizard
import time
import netsvc
import osv
import pooler

student_info_form='''<?xml version="1.0"?>
<form title="Student Library History">
    <seperator string="Issued resources" colspan="4"/>
    <field name="borrower"/>
</form>'''

student_info_fields={
    'borrower':{'string':'Borrower Name','type':'many2one','relation':'lms.patron.registration'},
    }

class wizard_issue_material(wizard.interface):
   states = {
    'init': {
        'actions':[],
        'result' : {'type' : 'form','arch':student_info_form,'fields':student_info_fields,'state':[('end','Cancel'),('print','print')]}
        }, 

    'print': {
        'actions':[],
       # 'result':{'type':'state','state':'end'}  #for generating wizard
        'result':{'type':'print','report': 'issued_resources','state':'end'} #for generating report
        }
    }
wizard_issue_material("wizard_issue_material")