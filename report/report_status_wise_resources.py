import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_status_wise_resources(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_status_wise_resources, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_detail':self.get_detail, 
                                      'get_status':self.get_status,
                                   })

    def get_status(self,form):
        
        return form['status']+" Resources"
        
    def get_detail(self,form):
        res =[]
        print "form['status']=",form['status']
        my_dict = {'status':'','title':'' ,'edition':'','author_id':'' ,'subject_id':'' ,'language_id':'' ,'dop':''}
        if form['status'] == 'Issued':
            a_ids =  pooler.get_pool(self.cr.dbname).get('lms.cataloge').search(self.cr, self.uid,[('state','=',form['status'])])
            print a_ids
            for i in pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr ,self.uid ,a_ids):
                print i.resource_no.name
                my_dict['status'] = form['status']
                my_dict['title'] = i.resource_no.title
                my_dict['edition'] = i.resource_no.edition.name
                my_dict['author_id'] = pooler.get_pool(self.cr.dbname).get('lms.author').browse(self.cr ,self.uid,int(i.resource_no.author_id[0])).name
                my_dict['subject_id'] = i.resource_no.subject_id.name
                my_dict['language_id'] = i.resource_no.language_id
                my_dict['dop'] = i.resource_no.dop
                res.append(my_dict)
                for  key,val in my_dict.items():
                    print key, "=>", val
        elif form['status'] == 'Active' or form['status'] == 'Deactive':
            print "active/deactive state"
            if form['status'] ==  'Active':
                ans = True
                a_ids =  pooler.get_pool(self.cr.dbname).get('lms.cataloge').search(self.cr, self.uid,[('active_deactive','=',ans)])
            else:
                ans = False
                a_ids = pooler.get_pool(self.cr.dbname).get('lms.cataloge').search(self.cr, self.uid,[('active_deactive','=',ans)])
            for i in pooler.get_pool(self.cr.dbname).get('lms.cataloge').browse(self.cr ,self.uid ,a_ids):
                print i.resource_no.name
                my_dict['status'] = form['status']
                my_dict['title'] = i.resource_no.title
                my_dict['edition'] = i.resource_no.edition.name
                my_dict['author_id'] = pooler.get_pool(self.cr.dbname).get('lms.author').browse(self.cr ,self.uid,int(i.resource_no.author_id[0])).name
                my_dict['subject_id'] = i.resource_no.subject_id.name
                my_dict['language_id'] = i.resource_no.language_id
                my_dict['dop'] = i.resource_no.dop
                res.append(my_dict)
                for  key,val in my_dict.items():
                    print key, "=>", val 
                             
        elif form['status'] == 'Returned':
            q =  pooler.get_pool(self.cr.dbname).get('lms.return').search(self.cr, self.uid,[('state','=',form['status'])])
            print "return ids =",q
            for check in pooler.get_pool(self.cr.dbname).get('lms.return').browse(self.cr ,self.uid ,q):
                print "name = ",check.returned_material
                for i in check.returned_material:
                    print i.cataloge_id.name
                    my_dict['status'] = form['status']
                    my_dict['title'] = i.resource_no.title
                    my_dict['edition'] = i.resource_no.edition.name
                    my_dict['author_id'] = pooler.get_pool(self.cr.dbname).get('lms.author').browse(self.cr ,self.uid,int(i.resource_no.author_id[0])).name
                    my_dict['subject_id'] = i.resource_no.subject_id.name
                    my_dict['language_id'] = i.resource_no.language_id
                    my_dict['dop'] = i.resource_no.dop
                    res.append(my_dict)
                    for  key,val in my_dict.items():
                        print key, "=>", val
        
        elif form['status'] == 'Reserved':
            print "Reserved"
            q =  pooler.get_pool(self.cr.dbname).get('lms.reserve.book').search(self.cr, self.uid,[('state','=',form['status'])])            
            print "ids=",q
            for i in pooler.get_pool(self.cr.dbname).get('lms.reserve.book').browse(self.cr ,self.uid ,q):
                print "name = ",i.borrower_id.name
              
                
                    
        return res
    
report_sxw.report_sxw('report.status_wise_resources','lms.cataloge', 
                      '/addons/cms_library/report/report_status_wise_resources_view.rml',

                      parser=report_status_wise_resources,
                      header=True)