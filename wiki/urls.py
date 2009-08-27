from django.conf.urls.defaults import *
from wiki.views import wv

urlpatterns = patterns('',
    url('^$',             wv.redirect_to_index,   name='wiki_index'),
    url('^(.*)/edit/$',   wv.page_edit,           name='page_edit'),
    url('^(.*)/submit/$', wv.page_submit,         name='page_submit'),
    url('^(.*)/$',        wv.wiki_page,           name='wiki_page'),
)
