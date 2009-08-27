This is a very simple wiki written with a couchdb backend using
the django stack.

INSTALL
--------

* Fetch the auth and sessions backends for couchdb from here_ and
  add them to the `INSTALLED_APPS` in your project's `settings.py` 
  as per the instructions.
* Place the `wiki` app and reference it too in the `INSTALLED_APPS`.
* Append the `wiki/templates` directory (with the absolute path) in
  the `TEMPLATE_DIRS` attribute of the `settings.py`.
* Add a pointer to the wiki URL and account urls in your `urls.py` 
  like::

    (r'^wiki/', include('wiki.urls'))
    (r'^accounts/', include('django.contrib.auth.urls'))

* Add the following attributes to your `settings.py`.::

    COUCHDB_HOST = 'http://path_to_couchdb_server:port_num/'
    # If you don't want unauthenticated users to create
    # pages, then set the below attribute to False
    ALLOW_UNAUTH_PAGE_CREATION = True
    # The below attribute is optional, if not specified
    # it redirects to an empty page.
    WELCOME_PAGE = '/path/to/default/start/up/page/'

* Your wiki is ready!

Please let me know how you feel about this app.

.. _here: http://github.com/theju/django-couchdb-utils/tree/master