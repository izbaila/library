import pooler
import time
from datetime import date
import datetime
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula
from werkzeug.testsuite import formparser
from _ast import Num

class report_duedate_resources(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_duedate_resources, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_patron_fine':self.get_patron_fine, 
                                      'get_month' :self.get_month,
                                  })
          
    def serial_number(self,cr,uid,ids,serial_no):
        return serial_no+1
    
    def get_month(self,form):
        month = datetime.datetime.now().strftime("%h ,%Y")
        return month
    def get_patron_fine(self,form):
        res= []
        id_issue_borrower = pooler.get_pool(self.cr.dbname).get('lms.issue').search(self.cr,self.uid,[('borrower_id.id','=',form['borrower'])]) #to grab the id of borrower if he had issued any books
        r = pooler.get_pool(self.cr.dbname).get('lms.issue').browse(self.cr ,self.uid ,id_issue_borrower)
        d2 = datetime.datetime.strptime( date.today().strftime('%Y-%m-%d'), "%Y-%m-%d").date() #current date
        serial_no = 0
        for i in r:
            d1 = datetime.datetime.strptime(i.issue_date, "%Y-%m-%d").date() #date on which the book was issued
            days_past_duedate = abs((d2 - d1).days)
            for c in i.resource:
                if days_past_duedate > 10:
                    fine_id = pooler.get_pool(self.cr.dbname).get('lms.fine.dues').search(self.cr,self.uid,[('catagory.type','=',c.resource_no.catagory_id.type)])
                    for fine in self.pool.get('lms.fine.dues').browse(self.cr ,self.uid ,fine_id): #to calculate fine
                        my_dict = {'s_no':'','borrower':'','resource':'','issue_date':'','due_date':'','fine':''}
                        my_dict['due_date'] = d1 + datetime.timedelta(days=10) #to find what the due date should be according to issue date
                        my_dict['borrower'] = i.borrower_id.name 
                        my_dict['issue_date'] = i.issue_date
                        my_dict['resource'] = c.resource_no.name
                        rupee= fine.fine_amount
                        print "fine per day=",rupee,".book has been issued from= ",days_past_duedate,".overdue days= ",days_past_duedate-9,"total fine= ",(days_past_duedate-9)*rupee
                        my_dict['fine'] = (days_past_duedate-9)*rupee
                        #to calculate serial number
                        sum_num = self.serial_number(self.cr,self.uid,self.ids,serial_no)
                        serial_no = sum_num
                        my_dict['s_no'] = sum_num
                        res.append(my_dict)
        return res
    
report_sxw.report_sxw('report.duedate_resources','lms.issue', 
                      '/addons/cms_library/report/report_duedate_resources_view.rml',
                      parser=report_duedate_resources,
                      header=True)