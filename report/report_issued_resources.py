import pooler
import time
import rml_parse
from report import report_sxw
import netsvc

class report_issued_resources(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_issued_resources, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_borrower_detail':self.get_borrower_detail,
                                   })
    def get_borrower_detail(self,form):
        result = []
        print "form['borrower']=",form['borrower']
        
        #borrower_id_issue = pooler.get_pool(self.cr.dbname).get('lms.issue').search(self.cr,self. uid,[('borrower_id.name','=',form['borrower'])]) 
        #print   "borrower_id=",borrower_id_issue
        
        my_dict = {'name':'' ,'type':'' ,'group':'' ,'degree':'' ,'image':'' }
        
        rec_users = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr ,self.uid ,form['borrower'])
        my_dict['name'] = rec_users.name
        my_dict['type'] = rec_users.type
        if rec_users.type == 'student':
            my_dict['group'] = rec_users.student_id.group
            my_dict['degree'] = rec_users.student_id.degree
            my_dict['image'] = rec_users.student_id.image
            print my_dict['name']
      #  i=0
       # while i< len(my_dict):
        #    result.append(my_dict)
        
        #print result[0]
        return result

report_sxw.report_sxw('report.issued_resources','lms.patron.registration', 
                      '/addons/cms_library/report/report_issued_resources_view.rml',
                      parser=report_issued_resources,
                      header=True)
