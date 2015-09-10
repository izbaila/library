import pooler
import time
import datetime
import rml_parse
from report import report_sxw
import netsvc

class report_resource_detail(rml_parse.rml_parse):
    
        def __init__(self, cr, uid, name, context):
            super(report_resource_detail, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_resource':self.get_resource,
                                       'get_month':self.get_month,
                                   })
            
        def get_month(self,form):
            month = datetime.datetime.now().strftime("%h , %Y")
            return month
        
        def get_resource(self,form):
            
            sno=0
            result = []
            resource_ids  = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr,self. uid,[('catagory_id','=',form['category'])])
            if resource_ids:
                rec_resource = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,resource_ids)
                for idds in rec_resource:
                    my_dict = {'sno':'','name':'' ,'subject_id':'' ,'catagory_id':'' ,'barcode':'', 'dop':'' ,'unit_cost':''}
                    sno =sno+1
                    my_dict['sno']=sno
                    my_dict['name'] =idds.name
                    my_dict['unit_cost'] =idds.unit_cost
                    my_dict['dop'] =idds.dop
                    my_dict['barcode'] =idds.barcode
                    my_dict['catagory_id'] =idds.catagory_id.type
                    my_dict['subject_id'] =idds.subject_id.name
                    result.append(my_dict)
            else:
                rec_resource = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr ,self.uid ,[('name','=',self.ids)])
                rec = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,rec_resource)
                for checker in rec:

                    my_dict = {'sno':'','name':'' ,'subject_id':'' ,'catagory_id':'' ,'barcode':'', 'dop':'' ,'unit_cost':''}
                    sno=sno+1
                    my_dict['sno']=sno
                    my_dict['name'] = checker.name
                    my_dict['unit_cost'] =idds.unit_cost
                    my_dict['dop'] =checker.dop
                    my_dict['barcode'] =checker.barcode
                    my_dict['catagory_id'] =checker.catagory_id.type
                    my_dict['subject_id'] = checker.subject_id.name 
                    result.append(my_dict)
            return result
        
report_sxw.report_sxw('report.resource_detail',
                      'lms.resource', 
                      '/addons/lms/report/resource_detail.rml',
                      parser=report_resource_detail,
                      header=True)
                     
#report_sxw.report_sxw(report.here you will write the name that you have defined in the report declaration
#(i.e name=student_record) in wizard report defination of xml and then,class name of you actual class in sim module,
#then its path of you rml
# file and it should be in report folder,the name of you class of report,header)
