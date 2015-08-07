import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_librarycard(rml_parse.rml_parse):
    
    def __init__(self, cr, uid, name, context):
            super(report_librarycard, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_status_resources':self.get_status_resources,
                                      'get_image':self.get_image,
                                   })
 

    def get_image(self,form):
        obj = self.pool.get('lms.patron.registration').browse(self.cr, self.uid,form['borrower_id'])
        if obj.type =='student':
            image = obj.student_id.image
            return image
        else:
            print "end of get image"
            return None

    def get_status_resources(self,form):
        res = []
        print form['borrower_id']
        obj = self.pool.get('lms.patron.registration').browse(self.cr, self.uid,form['borrower_id'])
        print obj.name,obj.type
    #    for check in obj: 
        my_dict = {'name':'' ,'type':'' ,'department':'' ,'father_name':'','joining_date':'','expiration_date':''}
        my_dict['name'] = obj.name
        my_dict['type'] = obj.type
        my_dict['joining_date'] = obj.dor
        my_dict['expiration_date'] = obj.expiry_date
        if obj.type == 'employee':
            print obj.employee_id.department_name
            my_dict['department'] = "Department : "+obj.employee_id.department_name
            my_dict['father_name'] = " "
        else:
            print obj.student_id.degree
            my_dict['department'] = "Degree : "+obj.student_id.degree
            my_dict['father_name'] = obj.student_id.father_name
            res.append(my_dict)
        for keys,val in my_dict.items():
            print keys ,"->",val
        print "end of get_status_resources"
        return res

report_sxw.report_sxw('report.librarycard',
                      'lms.library.card',
                      '/addons/cms_library/report/report_librarycard.rml',
                      parser=report_librarycard,
                      header=True)