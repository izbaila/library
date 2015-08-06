import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_no_of_material(rml_parse.rml_parse):
    def __init__(self, cr, uid, name, context):
            super(report_no_of_material, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({'get_count_detail':self.get_count_detail, 
                                      'get_detail':self.get_detail,
                                   })
    def get_count_detail(self,form):
        res =[]
        print "get_count_detail"
        print " form['resource'] = ",form['resource']
        
        type_catagory = "all of the resources available in library"
        if form['resource']:
            
            type_catagory = pooler.get_pool(self.cr.dbname).get('lms.categories').browse(self.cr ,self.uid,form['resource']).type
            #searching the resords that is in resource with the same catagory_id as in lms.catagory
            wess =pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr ,self.uid ,[('catagory_id.id','=',form['resource'])])
            print "ids of perticular catagory = ",wess
            # calculate total no of resources thats mentioned by user
            total_counts = {'total_resources':'' ,'books':'' ,'magazine':'' ,'journal':'' ,'audio_visual':'' ,'newspaper':''}
            if wess:
                print "full data"
                for i in pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr ,self.uid,wess):
                    sql = """ SELECT COUNT(*) FROM lms_resource
                            WHERE lms_resource.catagory_id = """+str(form['resource'])+"""""" 
                    self.cr.execute(sql)
                    total_no =  self.cr.fetchone()
                    print total_no
                    total_counts['total_resources']  = "Total "+type_catagory +" = "+str(total_no[0])
                    res.append(total_counts)
            else:
                print "selected but no data"
                total_no = [0]
                total_counts['total_resources']  = "Total "+type_catagory +" = "+str(0)
                print "total_no=",total_no[0]
                res.append(total_counts)
        
        else:
            print "nothing is selected empty"
            for i in pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr ,self.uid,self.ids):
                total_counts = {'total_resources':'' ,'books':'' ,'magazine':'' ,'journal':'' ,'audio_visual':'' ,'newspaper':''}
                sql = """ SELECT COUNT(*) FROM lms_resource """ 
                self.cr.execute(sql)
                total_no =  self.cr.fetchone()
                print total_no
                total_counts['total_resources'] = "Total number of resources available in library = "+str(total_no[0])
                
                #total no of books in library
                sql = """ SELECT COUNT(*) FROM lms_resource
                         WHERE lms_resource.catagory_id = """+str(1)+"""""" 
                self.cr.execute(sql)
                total_no_books =  self.cr.fetchone()
                print "books = ",total_no_books
                total_counts['books'] = "Total books = "+str(total_no_books[0])
                
                #total no of magazine in library
                sql = """ SELECT COUNT(*) FROM lms_resource
                         WHERE lms_resource.catagory_id = """+str(2)+"""""" 
                self.cr.execute(sql)
                total_no_magazine =  self.cr.fetchone()
                print "magazine = ",total_no_magazine
                total_counts['magazine'] = "Total magazines = "+str(total_no_magazine[0])
                
                #total no of journal in library
                sql = """ SELECT COUNT(*) FROM lms_resource
                         WHERE lms_resource.catagory_id = """+str(3)+"""""" 
                self.cr.execute(sql)
                total_no_journal =  self.cr.fetchone()
                print "journal = ",total_no_journal
                total_counts['journal'] = "Total journals = "+str(total_no_journal[0])
                
                #total no of audio/visual in library
                sql = """ SELECT COUNT(*) FROM lms_resource
                         WHERE lms_resource.catagory_id = """+str(4)+"""""" 
                self.cr.execute(sql)
                total_no_audio_visual =  self.cr.fetchone()
                print "audio = ",total_no_audio_visual
                total_counts['audio_visual'] = "Total audio/visual = "+str(total_no_audio_visual[0])
                
                #total no of newspaper in library
                sql = """ SELECT COUNT(*) FROM lms_resource
                         WHERE lms_resource.catagory_id = """+str(5)+"""""" 
                self.cr.execute(sql)
                total_no_newspaper =  self.cr.fetchone()
                print "newspaper = ",total_no_newspaper
                total_counts['newspaper'] = "Total newspapers = "+str(total_no_newspaper[0])
                res.append(total_counts)
                
        #return "Total no of "+type_catagory+"s = "+res
        return res

    def get_detail(self,form):
        res = []
        print "form['resource']=",form['resource'],"inside detail"
        if form['resource']:
            wess = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr ,self.uid ,[('catagory_id.id','=',form['resource'])])
            print "wess = ",wess
            for i in pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr ,self.uid,wess):
                print "name = ",i.name,"edition = ",i.edition.name
                my_dict = {'title':'' ,'edition':'','author_id':'' ,'subject_id':'' ,'language_id':'' ,'dop':''} 
                my_dict['title'] = i.title
                my_dict['edition'] = i.edition.name
                my_dict['author_id'] = pooler.get_pool(self.cr.dbname).get('lms.author').browse(self.cr ,self.uid,int(i.author_id[0])).name
                my_dict['subject_id'] = i.subject_id.name
                my_dict['language_id'] = i.language_id
                my_dict['dop'] = i.dop
                res.append(my_dict)
                for  key,val in my_dict.items():
                    print key, "=>", val
        else:
            wess = pooler.get_pool(self.cr.dbname).get('lms.resource').search(self.cr ,self.uid ,[('catagory_id.id','!=',form['resource'])])
            for i in pooler.get_pool(self.cr.dbname).get('lms.resource').browse(self.cr ,self.uid,wess):
                print "name = ",i.name,"edition = ",i.edition.name
                my_dict = {'title':'' ,'edition':'','author_id':'' ,'subject_id':'' ,'language_id':'' ,'dop':''} 
                my_dict['title'] = i.title
                my_dict['edition'] = i.edition.name
                my_dict['author_id'] = pooler.get_pool(self.cr.dbname).get('lms.author').browse(self.cr ,self.uid,int(i.author_id[0])).name
                my_dict['subject_id'] = i.subject_id.name
                my_dict['language_id'] = i.language_id
                my_dict['dop'] = i.dop
                res.append(my_dict)
                for  key,val in my_dict.items():
                    print key, "=>", val
            
        return res

report_sxw.report_sxw('report.no_of_material','lms.categories', 
                      '/addons/cms_library/report/report_no_of_material_view.rml',

                      parser=report_no_of_material,
                      header=True)
