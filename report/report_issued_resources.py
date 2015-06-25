import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_issued_resources(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_issued_resources, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_detail_issued':self.get_detail_issued, 
                                      'get_borrower_detail':self.get_borrower_detail,
                                   })

 
    def get_borrower_detail(self,form):
            result = []
            if form['borrower']:
                my_dict = {'name':'' ,'type':'' ,'group':'' ,'degree':'' ,'image':''}
                rec = pooler.get_pool(self.cr.dbname).get('lms.patron.registration').browse(self.cr,self.uid,form['borrower'])
                my_dict['name'] = rec.name
                my_dict['type'] = rec.type
                my_dict['group'] = rec.student_id.group
                my_dict['degree'] = rec.student_id.degree
                my_dict['image'] = rec.student_id.image
                result.append(my_dict)
                return result
          
        
    def get_detail_issued(self,form):
        result = []

        print "in get_detail",form['borrower']
        issued_resources_id = pooler.get_pool(self.cr.dbname).get('lms.issue').search(self.cr ,self.uid,[('borrower_id.id','=',form['borrower'])])
        print  "issued_resources_id=",issued_resources_id,"\n"

        j=0
        while j< len(issued_resources_id):
            rec = pooler.get_pool(self.cr.dbname).get('lms.issue').browse(self.cr ,self.uid ,issued_resources_id[j])
            ans = rec.resource

            if issued_resources_id:
                for i in ans:
                    my_dict = {'c_name':'' ,'resource_no':'' ,'rack_no':'' ,'accession_no':'' ,'issue_no':'' ,'cataloge_date':''}
                    my_dict['c_name'] =  i.name
                    my_dict['resource_no'] = i.resource_no.name
                    my_dict['rack_no'] = i.rack_no.rack_location
                    my_dict['accession_no'] = i.accession_no
                    my_dict['issue_no'] = rec.name
                    my_dict['cataloge_date'] = rec.issue_date
                 
                    result.append(my_dict)
            j=j+1
        return result
    
   
report_sxw.report_sxw('report.issued_resources','lms.patron.registration', 
                      '/addons/cms_library/report/report_issued_resources_view.rml',

                      parser=report_issued_resources,
                      header=True)
