import pooler
import datetime
import datetime
import rml_parse
from datetime import date
from report import report_sxw
import netsvc
from xlrd import formula

class report_return_materail(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_return_materail, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_borrower_detail':self.get_borrower_detail,
                                      'get_return_resource':self.get_return_resource,
                                      'g' :self.g,
                                      'get_month':self.get_month,
                                   })
    def g(self,form):
        patron_info = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr ,self.uid ,form['borrower'])
        image =patron_info.student_id.image 
        return image
    
    def get_month(self,form):
            month = datetime.datetime.now().strftime("%h ,%Y")
            return month
        
    def get_borrower_detail(self,form):
            result = []
            if form['borrower']:
                my_dict = {'name':'' ,'type':''  ,'degree':'' ,'father_name':''}
                rec = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr,self.uid,form['borrower'])
                my_dict['type'] = rec.type
                if my_dict['type'] == 'student':
                    my_dict['name'] = rec.student_id.name
                    my_dict['degree'] = rec.student_id.degree+" , Group : "+str(rec.student_id.group)
                    my_dict['father_name'] = rec.student_id.father_name
                else:
                    my_dict['name'] = rec.employee_id.name
                    my_dict['degree'] = "Department : "+rec.employee_id.department_name
                result.append(my_dict)
                return result
    
    def get_return_resource(self,form):
        res = []
        sno = 0
        iddd = pooler.get_pool(self.cr.dbname).get('lms.return').search(self.cr ,self.uid ,[('borrower_id','=',form['borrower'])])
        rec = pooler.get_pool(self.cr.dbname).get('lms.return').browse(self.cr ,self.uid,iddd)
        for r in rec:
            for c in r.returned_material:
                if form['start_date']: #this if structure is use to default select current date if it is not selected by user 
                    if form['end_date'] == False:
                        end_date = date.today().strftime('%Y-%m-%d')
                    else:
                        end_date = form['end_date']
                    if r.return_date > form['start_date'] and r.return_date < end_date:
                        my_dict = {'sno':'','name':'' ,'return_date':'' ,'state':'' ,'resource_no':'' ,'acc_no':''}
                        sno = sno + 1
                        my_dict['sno'] = sno
                        my_dict['name'] = r.name
                        my_dict['return_date'] = r.return_date
                        my_dict['state'] = r.state
                        my_dict['resource_no'] = c.cataloge_id.resource_no.name
                        my_dict['acc_no'] = c.cataloge_id.accession_no
                        res.append(my_dict)
                else:
                    my_dict = {'sno':'','name':'' ,'return_date':'' ,'state':'' ,'resource_no':'' ,'acc_no':''}
                    sno = sno + 1
                    my_dict['sno'] = sno
                    my_dict['name'] = r.name
                    my_dict['return_date'] = r.return_date
                    my_dict['state'] = r.state
                    my_dict['resource_no'] = c.cataloge_id.resource_no.name
                    my_dict['acc_no'] = c.cataloge_id.accession_no
                    res.append(my_dict)
        return res
    
report_sxw.report_sxw('report.return_materail','lms.return', 
                      '/addons/lms/report/report_return_materail_view.rml',
                      parser=report_return_materail,
                      header=True)