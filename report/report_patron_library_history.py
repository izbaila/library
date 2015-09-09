import pooler
import time
import datetime 
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

import mx.DateTime
from mx.DateTime import RelativeDateTime, now, DateTime, localtime

class report_patron_library_history(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_patron_library_history, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_issued_detail':self.get_issued_detail, 
                                      'get_borrower_detail':self.get_borrower_detail,
                                      'get_image':self.get_image,
                                      'get_month':self.get_month,
                                   })
    def get_month(self,form):
        month = datetime.datetime.now().strftime("%h ,%Y")
        return month

    def get_image(self,form):
        rec = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr,self.uid,form['borrower'])
        image = rec.student_id.image
        return image
    
    def get_borrower_detail(self,form):
            result = []
            if form['borrower']:
                my_dict = {'name':'' ,'type':''  ,'degree':'' ,'father_name':''}
                rec = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr,self.uid,form['borrower'])
                my_dict['type'] = rec.type
                if my_dict['type'] == 'student':
                    my_dict['name'] = rec.student_id.name
                    my_dict['degree'] = "Degree : "+rec.student_id.degree+" , Group : "+str(rec.student_id.group)
                    my_dict['father_name'] = rec.student_id.father_name
                else:
                    my_dict['name'] = rec.employee_id.name
                    my_dict['degree'] = "Department : "+rec.employee_id.department_name
                result.append(my_dict)
                return result
        
    def get_issued_detail(self,form):
        result = []
        issued_resources_id = pooler.get_pool(self.cr.dbname).get('lms.issue').search(self.cr ,self.uid,[('borrower_id.id','=',form['borrower'])])
        j=0
        while j< len(issued_resources_id) :
            rec = pooler.get_pool(self.cr.dbname).get('lms.issue').browse(self.cr ,self.uid ,issued_resources_id[j])
            ans = rec.resource
            if issued_resources_id:
                for i in ans:
                    my_dict = {'resource_no':'' ,'accession_no':'' ,'issue_no':'' ,'cataloge_date':'',
                               'return_date':'' ,'return_name':''}
                    my_dict['resource_no'] = i.resource_no.name
                    my_dict['accession_no'] = i.accession_no
                    my_dict['issue_no'] = rec.name
                    issue_date = mx.DateTime.strptime(rec.issue_date, '%Y-%m-%d').strftime("%h %d, %y ")
                    my_dict['cataloge_date'] = issue_date
                    r_id = pooler.get_pool(self.cr.dbname).get('lms.return').search(self.cr ,self.uid,[('returned_material.cataloge_id.id','=',i.id ),( 'borrower_id.id','=',form['borrower'])])
                    #print "return ids=",r_id
                    for p in pooler.get_pool(self.cr.dbname).get('lms.return').browse(self.cr ,self.uid ,r_id):
                        d = p.return_date
                        return_date = mx.DateTime.strptime(d, '%Y-%m-%d').strftime("%h %d, %y ")
                        #print mx.DateTime.strptime(d, '%Y-%m-%d ')
                       
                        my_dict['return_date'] =return_date
                        my_dict['return_name'] = p.name
                    result.append(my_dict)
            j=j+1
           
        return result
  
report_sxw.report_sxw('report.patron_library_history','lms.patron.registration', 
                      '/addons/cms_library/report/report_patron_library_history_view.rml',
                      parser=report_patron_library_history,
                      header=True)