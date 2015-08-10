import pooler
import time
import rml_parse
from report import report_sxw
import netsvc

class report_resource_detail(rml_parse.rml_parse):
    
        def __init__(self, cr, uid, name, context):
            super(report_resource_detail, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_resource':self.get_resource,
                                   })
                       
        def get_resource(self,form):
            result = []
            resource_ids  = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr,self. uid,[('catagory_id','=',form['category'])])
            if resource_ids:
                rec_resource = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,resource_ids)
                for idds in rec_resource:
                    my_dict = {'name':'' ,'subject_id':'' ,'title':'' ,'edition':'' ,'catagory_id':'' ,'barcode':'',
                               'pages':'' ,'dop':'' ,'annual_cost':'' ,'unit_cost':''}
                    my_dict['name'] =idds.name
                    my_dict['unit_cost'] =idds.unit_cost
                    my_dict['annual_cost'] =idds.annual_cost
                    my_dict['dop'] =idds.dop
                    my_dict['pages'] =idds.pages
                    my_dict['barcode'] =idds.barcode
                    my_dict['catagory_id'] =idds.catagory_id.type
                    my_dict['title'] =idds.title
                    my_dict['subject_id'] =idds.subject_id.name
                    my_dict['edition'] =idds.edition.name
                    result.append(my_dict)
            else:
                rec_resource = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr ,self.uid ,[('name','=',self.ids)])
                rec = pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr,self.uid,rec_resource)
                for checker in rec:
                    my_dict = {'name':'' ,'subject_id':'' ,'title':'' ,'edition':'' ,'catagory_id':'' ,'barcode':'',
                              'pages':'' ,'dop':'' ,'annual_cost':'','unit_cost':''}
                    my_dict['name'] = checker.name
                    my_dict['unit_cost'] =idds.unit_cost
                    my_dict['annual_cost'] =checker.annual_cost
                    my_dict['dop'] =checker.dop
                    my_dict['pages'] =checker.pages
                    my_dict['barcode'] =checker.barcode
                    my_dict['catagory_id'] =checker.catagory_id.type
                    my_dict['title'] = checker.title
                    my_dict['edition'] = checker.edition.name
                    my_dict['subject_id'] = checker.subject_id.name 
                    result.append(my_dict)
            return result
        
report_sxw.report_sxw('report.resource_detail',
                      'lms.resource', 
                      '/addons/cms_library/report/resource_info_view.rml',
                      parser=report_resource_detail,
                      header=True)


                      
                     
#report_sxw.report_sxw(report.here you will write the name that you have defined in the report declaration
#(i.e name=student_record) in wizard report defination of xml and then,class name of you actual class in sim module,
#then its path of you rml
# file and it should be in report folder,the name of you class of report,header)
