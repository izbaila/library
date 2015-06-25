import wizard
import time
import netsvc
import osv
import pooler

return_materail_form='''<?xml version="1.0"?>
<form title="Student Library History">
    <seperator string="Return resources" colspan="4"/>
    <field name="borrower"/>
</form>'''

return_materail_fields={
    'borrower':{'string':'Borrower Name','type':'many2one','relation':'lms.patron.registration'},
    }

class wizard_return_material(wizard.interface):
    states = {
              'init' : {
                        'action' : [] , 
                        'result' : {'type' : 'form','arch':return_materail_form,'fields':return_materail_fields,'state':[('end','Cancel'),('print','print')]}
                        },
              
          'print': {
            'actions':[],
           # 'result':{'type':'state','state':'end'}  #for generating wizard
            'result':{'type':'print','report': 'return_materail','state':'end'} #for generating report
            }
    }
wizard_return_material("wizard_return_material")