from couchdb.schema import *
from couchdb.schema import View

class Page(Document):
    created_date       = DateTimeField()
    last_edited_date   = DateTimeField()
    title              = TextField()
    contents           = TextField()
    auth_user_editable = BooleanField()
    user               = DictField()

    get_pages  = View('pages', 
                      'function (doc) { emit(doc.title, doc);}',
                      name='all')
