import pooler
import time
import rml_parse
from report import report_sxw
import netsvc
from xlrd import formula

class report_librarycard(rml_parse.rml_parse):
    
    def __init__(self, cr, uid, name, context):
            super(report_librarycard, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({ 'get_patron_for_cards':self.get_patron_for_cards,
                                   })

    def get_patron_for_cards(self,form):
        result = []
        obj = self.pool.get('lms.library.card').browse(self.cr, self.uid,form['borrower_id'])
        print "Patron_id",obj.borrower_id.type
        return None

report_sxw.report_sxw('report.librarycard',
                      'lms.library.card',
                      '/addons/cms_library/report/report_librarycard.rml',
                      parser=report_librarycard,
                      header=True)