import wizard
import netsvc
import time
import osv
import pooler


resource_form = '''<?xml version="1.0"?>
<form string="Changing Name">
    <separator string="Name Changing Form" colspan="4"/>
    <field name="student_name"/>
    <newline/>
    <field name="resource_cat"/>
    <newline/>
</form>'''

resource_fields = {
    'resource_name':{'string':'Student Name' ,'type':'char'},              
}

success_message_form = '''<?xml version = "1.0"?>
#<form string="Success Message">
#    <separator string="Success Message State" colspan="4"/>
#</form>'''

success_message_fields = {}

failure_message_form = '''<?xml version = "1.0"?>
#<form string = "Failure Message">
#    <separator string="Failed Message State" colspan="4/>
#</form>'''

failure_message_fields={}

class resource_information(wizard.interface):
    
    def change_name(self,cr,uid,data,context):
        oldname = data['form']['student_name']
        #newname = data['form']['new_name']
        result = pooler.get_pool(cr.dbname).get('resource').browse(cr, uid, [oldname])
        if result:
            return 'success'
        else:
            return 'failure'
    states = {
        'init' : {
            'actions':[],
            'result':{'type':'form', 'arch':resource_form,'fields':resource_fields,'state':[('end','Cancel','gtk-cancel'), ('change','Change','gtk-go-forward')]}
        },
        'change':{
            'actions':[],
            'result':{'type':'state','state':'end'}
        },
        'success':{
            'actions':[],
            'result':{'type':'form', 'arch':success_message_form,'fields':success_message_fields,'state':[('end','Finish')]}
       },
        'failure':{
            'actions':[],
            'result':{'type':'form', 'arch':failure_message_form,'fields':failure_message_fields,'state':[('end','Finish')]}
        },     
    }
resource_information("resource_wizard")