import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_return_materail(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_return_materail, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_borrower_detail':self.get_borrower_detail,
                                      'get_return_resource':self.get_return_resource,
                                   })
    def get_borrower_detail(self,form):
        
        res = []
        patron_info = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr ,self.uid ,form['borrower'])
        my_dic = {'name':'' ,'type':'' ,'father_name':'' ,'group':'' ,'image':'' ,'degree':'' 
                  }
        my_dic['name'] = patron_info.name
        my_dic['type'] = patron_info.type
        
        if patron_info.type == 'student': 
            my_dic['father_name'] =  patron_info.student_id.father_name
            my_dic['group'] =  patron_info.student_id.group
            my_dic['image'] =  patron_info.student_id.image
            my_dic['degree'] =  patron_info.student_id.degree
            res.append(my_dic)
        else:
            print "department_name=",patron_info.employee_id.department_name
        return res
    
    def get_return_resource(self,form):
        res = []
        iddd = pooler.get_pool(self.cr.dbname).get('lms.return').search(self.cr ,self.uid ,[('borrower_id.name','=',form['borrower'])])
        print "iddd=",iddd,"its length",len(iddd)
        i=0
        while i<len(iddd):
            r = pooler.get_pool(self.cr.dbname).get('lms.return').browse(self.cr ,self.uid,iddd[i])
            for c in r.returned_material:
                my_dict = {'name':'' ,'return_date':'' ,'state':'' ,'resource_no':'' ,'acc_no':''}
                my_dict['name'] = r.name
                my_dict['return_date'] = r.return_date
                my_dict['state'] = r.state
                my_dict['resource_no'] = c.cataloge_id.resource_no.name
                my_dict['acc_no'] = c.cataloge_id.accession_no
                print my_dict.values()
                res.append(my_dict)
                print "res=","******************\n",res
            i=i+1
        return res
    
report_sxw.report_sxw('report.return_materail','lms.return', 
                      '/addons/cms_library/report/report_return_materail_view.rml',

                      parser=report_return_materail,
                      header=True)
