import wizard
import time
import netsvc
import osv
from osv import osv
import pooler
import sys

reservation_form = """<?xml version="1.0"?>
<form title ="History of resources issued by patron">
     <seperator string="Issue resources" colspan="4"/>
     <field name = "borrower"/>
     <newline/>
     <field name = "resource_name"/>
 </form> 
 """
reservation_field = {
    'borrower' :{'string':'Borrower Name','type':'many2one','relation':'lms.patron.registration' },
    'resource_name' :{'string':'Resource Name','type':'many2one','relation':'lms.resource' },
                          }
class wizard_reservation(wizard.interface):
    def reserve(self ,cr ,uid ,data ,context):
        print "borrower name",data['form']['borrower']
        print "resource name",data['form']['resource_name']
        
        catalogue_name = pooler.get_pool(cr.dbname).get('lms.cataloge').search(cr ,uid,[('resource_no.id','=',data['form']['resource_name'])])
        print "catalogued resources=  ",catalogue_name
        i=0
        for check in pooler.get_pool(cr.dbname).get('lms.cataloge').browse(cr ,uid ,catalogue_name):
            if check.state == 'Issued':
                print "catalogue_name[",i,"]= ISSUED",len(catalogue_name),"=length(catalogue_name)"
                if i == len(catalogue_name)-1:
                    print "book is not avilable"
                    pooler.get_pool(cr.dbname).get('lms.reserve.book').create(cr, uid, {'borrower_id': data['form']['borrower'],'cataloge_id':catalogue_name[i],'state':'Reserved'})
            else:
                print "catalogue_name[",i,"]= AVAILBLE"
                raise osv.except_osv(('Reservation Denied'), ('Book cannot be reserved it is availble in library'))
                return None
            i+=1
        return None
    states = {
      'init' : {
         'actions' : [] ,
         'result' : {'type':'form' ,'arch':reservation_form,'fields':reservation_field,
                     'state':[('end','Cancel'),('reserve','Reserve')]}
        
         },
     'reserve': {
        'actions':[],
        'result':{'type':'action', 'action':reserve, 'state':'end'}
        #'result': {'type':'action', 'action':_invoice_cancel, 'state':'end'},#inorder to execute function
        }
      }
wizard_reservation ("wizard_reservation")