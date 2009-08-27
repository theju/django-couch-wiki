from wiki.models import Page
from datetime import datetime
from wiki.forms import PageForm
from wiki.utils import json_date
from django.conf import settings
from django.utils.functional import curry
from django.template import RequestContext
from couchdb import Server, ResourceNotFound
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, Http404

class WikiViews(object):
    def __init__(self):
        couchdb_host = getattr(settings, 'COUCHDB_HOST')
        server       = Server(couchdb_host)
        try:
            self.db  = server['wiki']
        except ResourceNotFound:
            self.db  = server.create('wiki')
            Page.get_pages.sync(self.db)
        self.wiki_form = curry(PageForm, db = self.db)

    def redirect_to_index(self, request):
        welcome_page_url = getattr(settings, 'WELCOME_PAGE', None)
        if welcome_page_url:
            return HttpResponseRedirect(welcome_page_url)
        return self.wiki_index(request)

    def wiki_index(self, request):
        return render_to_response('wiki/wiki.html', 
                                  context_instance = RequestContext(request, {}))

    def _get_page(self, page_name):
        return Page.get_pages(self.db, key = page_name).rows

    def wiki_page(self, request, page_name):
        page = self._get_page(page_name)
        base_context = {'page_name'   : page_name,
                        'create_page' : False}
        if not page:
            # Create an empty page based on settings.py
            allow_unauth_page_creation = getattr(settings, 'ALLOW_UNAUTH_PAGE_CREATION', True)
            if not allow_unauth_page_creation:
                raise Http404
            form = self.wiki_form(data = {'title': page_name})
            base_context.update({'create_page': True, 'form': form})
        else:
            # Show the page.
            base_context.update({'page': page[0].value})
        request_context = RequestContext(request, base_context)
        return render_to_response('wiki/wiki.html',
                                  context_instance = request_context)

    def page_submit(self, request, page_name):
        # If all's well, save the page and redirect to the page,
        # It it is a preview then redirect to wiki_page with 
        # the preview text
        # If errors, then display them
        if not request.method == "POST":
            return HttpResponseNotAllowed(["POST"])
        page = self._get_page(page_name)
        form = self.wiki_form(data = request.POST)
        base_context = {'page_name'   : page_name, 
                        'create_page' : True,
                        'form'        : form}
        if form.is_valid():
            if 'preview' in request.POST:
                # Preview the page
                base_context.update({'preview': form.cleaned_data['contents']})
                return render_to_response('wiki/wiki.html',
                                          context_instance = RequestContext(request, base_context))
            if page:
                doc_id = page[0].id
            else:
                doc_id = None
            data = form.cleaned_data.copy()
            data['last_edited_date'] = json_date(datetime.now())
            if not request.user.is_anonymous():
                data['user'] = request.user.unwrap()
            if doc_id:
                doc = self.db[doc_id]
                for key in data:
                    doc[key] = data[key]
                self.db[doc_id] = doc
            else:
                data['created_date'] = json_date(datetime.now())
                doc_id = self.db.create(data)
            base_context.update({'page': self.db[doc_id], 'create_page': False})
            base_context.pop('form')
        request_context = RequestContext(request, base_context)
        return render_to_response('wiki/wiki.html', 
                                  context_instance = request_context)

    def page_edit(self, request, page_name):
        # If all's well, save the page and redirect to the page,
        # It it is a preview then redirect to wiki_page with 
        # the preview text
        # If errors, then display them
        page = self._get_page(page_name)
        if not page:
            raise Http404
        if page[0].value['login_to_edit'] and not request.user.is_authenticated():
            return HttpResponseRedirect('%s?next=%s' %(settings.LOGIN_URL, request.path))
        base_context = {'page_name': page_name, 'create_page': True}
        form = self.wiki_form(data = page[0].value)
        base_context.update({'form': form})
        request_context = RequestContext(request, base_context)
        return render_to_response('wiki/wiki.html', 
                                  context_instance = request_context)


wv = WikiViews()
