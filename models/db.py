# -*- coding: utf-8 -*-
"""
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
## - This application was developed using Visual Studio Code and profited
## - of pylint. Some lines and comments are there for convenience for this
## - particular tool. The fake import is to prevent warnings from pylint.
## - As web2py combines model and controller files in a single file,
## - imports are not necessary. However, pylint keeps telling that variables
## - and functions are not declared. To avoid disabling pylint and lose
## - its support, I adopted such tricks.
#########################################################################
"""
if 0:#pylint: disable=using-constant-test
    #import sys
    #sys.path.append('C:\\web2py')
    #sys.path.append('C:\\web2py\\applications\\web2py_vue\\models')
    import gluon
    from gluon import * #pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import, pointless-string-statement
    from gluon.compileapp import local_import_aux as local_import #pylint: disable=unused-import
    from gluon.cache import Cache as CacheConstructor
    from gluon.compileapp import LoadFactory as LOAD#pylint: disable=unused-import
    from gluon.html import xmlescape #pylint: disable=unused-import
    from gluon.sql import SQLDB #pylint: disable=unused-import
    from gluon.sql import SQLField #pylint: disable=unused-import
    #from gluon.sqlhtml import SQLFORM #
    #from gluon.sqlhtml import SQLTABLE #
    from gluon.tools import * #pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import, pointless-string-statement

    global request; request = gluon.globals.Request(0)
    global cache; cache = CacheConstructor(request)
    global response; response = gluon.globals.Response()
    global session; session = gluon.globals.Session()
    global db; db = DAL()
    global auth; auth = Auth()
    global crud; crud = Crud(0)
    global mail; mail = Mail()
    global plugins; plugins = PluginManager()
    global service; service = Service()
    global current; current.request = request; current.request.now=request.now
# Web2py Bibliotecas:
#response.optimize_css = "concat,minify,inline"
#response.optimize_js = "concat,minify,inline"


if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.get('db.uri'), 
             pool_size = myconf.get('db.pool_size'),
             migrate_enabled = myconf.get('db.migrate'),
             check_reserved = ['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table(
    'doc',
    Field('title', type='string', requires=IS_LENGTH(80)),
    Field('body', 'text'))

db.define_table(
    'webpages',
    Field('title', type='string', requires=IS_LENGTH(80)),
    Field('body', 'text'))

db.define_table(
    'systems',
    Field('name', type='string', requires=IS_LENGTH(80)),
    Field('body', 'text'))

db.define_table(
    'code_lines',
    Field('vid', type='integer'),
    Field('code_text', type='string'),
    Field('saved', type='boolean'),
    Field('vindex', type='string')
)

## Initial filling of the table
filled_tables = False
if db(db.doc).isempty():
    from gluon.contrib.populate import populate
    populate(db.doc, 100)
    filled_tables = True

if db(db.webpages).isempty():
    from gluon.contrib.populate import populate
    populate(db.webpages, 20)
    filled_tables = True

if db(db.systems).isempty():
    from gluon.contrib.populate import populate
    populate(db.systems, 50)
    filled_tables = True

if filled_tables is True:
    db.commit()