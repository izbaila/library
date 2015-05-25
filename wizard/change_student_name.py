import wizard
import time
import netsvc
import osv
import pooler

_change_student_name_form='''<?xml version="1.0"?>
<form title="changing student name">
    <seperator string="change student name" colspan="4"/>
    <field name="catagory"/>
    <newline/>
    <field name="title"/>
 </form>'''

_change_student_name_fields={
     'catagory': {'string':'Catagory','type':'many2one','relation':'lms.categories'},
     'title':{'string':'Title','type':'char'},
   }


def change_name(self, cr, uid, data, context):
    current_id = data['form']['catagory']
    title_fetch = data['form']['title']
    print "current_id=",current_id
    
   # pooler.get_pool(cr.dbname).get('student').write(cr,uid,current_id,{'name':first_name,'father_name':last_name})
    return None
    

class wizard_change_student_name(wizard.interface):
    states = {
    'init': {
        'actions':[],
        'result' : {'type' : 'form','arch':_change_student_name_form,'fields':_change_student_name_fields,'state':[('print','print'),('end','Cancel')]}
        }, 

    'print': {
        'actions':[],
        'result':{'type':'state','state':'end'}
        }
    }
wizard_change_student_name("wizard_change_student_name")