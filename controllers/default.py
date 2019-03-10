"""# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - presents some ideas on integration of web2py and Vue.js
## - This application was developed using Visual Studio Code and profited
## - of pylint. Some lines and comments are there for convenience for this
## - particular tool. The fake import is to prevent warnings from pylint.
## - As web2py combines model and controller files in a single file,
## - imports are not necessary. However, pylint keeps telling that variables
## - and functions are not declared. To avoid disabling pylint and lose
## - its support, I adopted such tricks.
## - The interest of returning the page through controller is to enable web2py access
## - control, enforcing business rules, like:
## -         @auth.requires_login()
## -         @auth.requires_membership('group')
## -         @auth.requires_permission('read', table_name)
#########################################################################
"""
if 0:#pylint: disable=using-constant-test
    from web2py_vue.models.db import * #pylint: disable=unused-wildcard-import, redefined-builtin, wildcard-import, pointless-string-statement
    from db import *
    
def index():
    """
    Front page of this recipe.
    Present links to each example.
    """
    select_link = A("Vue selector Example", _href=URL("default", "select_page"))
    search_link = A("Vue search example", _href=URL("default", "main"))
    ide_link = A("Vue IDE example", _href=URL("default", "ide_page"))
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'),
                select_link=select_link,
                search_link=search_link,
                ide_link=ide_link,
               )


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to
    allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def main():
    """ Function to allow web2py return the Vue page.
    """
    #response.delimiters = ('{[',']}')
    return dict()


def select_page():
    """
    Exposes a custom list item component along a way to organize the code.
    This component receives data from root Vue object by v-bind directives and returns
    modifications by callback functions. Additionally, this component informs when
    it was selected, allowing root Vue objects to un-select the previous component,
    keeping only one selected component.
    """
    titulo = 'Vue Selector'
    response.flash = T("Loaded!")
    return dict(message=T('Vue'), titulo=titulo)

def ide_page():
    """
    Exposes a simple html editor in browser with a target area.
    Demonstrates the use of v-bind directive with objects and
    subsequent v-model in component. This allows simple two-way
    binding between the root Vue and components.
    Additionally, a simple syntax highlighting library (Prism)
    is used inside a computed property.
    """
    titulo = 'Test of web browser IDE'
    response.flash = T("Loaded!")
    return dict(message=T('Vue'), titulo=titulo)

def json_get_webpages():
    """
    Function to return the webpages in JSON format.
    """

    if len(request.vars.q) > 1:
        ids = db(
            db.webpages.title.contains(request.vars.q) |
            db.webpages.body.contains(request.vars.q)
            ).select(
                db.webpages.id,
                groupby=db.webpages.id,
                limitby=(0, 10)).column()

        rows = db(db.webpages.id.belongs(ids)).select()
    else:
        rows = db(db.webpages.id > 0).select(
            db.webpages.id,
            db.webpages.title,
            db.webpages.body,
            limitby=(0, 10))
    return response.json(rows)

def json_get_systems():
    """
    Function to return the systems in JSON format.
    """
    if len(request.vars.q) > 1:
        ids = db(
                 db.systems.name.contains(request.vars.q)
                 ).select(db.systems.id, groupby=db.systems.id).column()

        rows = db(db.systems.id.belongs(ids)).select()
    else:
        rows = db(db.systems.id>0).select(db.systems.id,
                                         db.systems.name,
                                        limitby=(0, 10))

    return response.json(rows)

def json_search():
    """
    Function to feed the Vue page with query answers.
    """
    if len(request.vars.q) > 0:
        ids = db(
                 db.doc.title.contains(request.vars.q) |
                 db.doc.body.contains(request.vars.q)
                 ).select(db.doc.id, groupby=db.doc.id).column()

        rows = db(db.doc.id.belongs(ids)).select()
    return response.json(rows)

def json_get_source():
    """
    Function to feed the Vue page with all code lines saved.
    """
    rows = db(db.code_lines.id>0).select(
        db.code_lines.vid, 
        db.code_lines.code_text,
        db.code_lines.saved,
        orderby=db.code_lines.vid)
    return response.json(rows)

def json_save_line():
    """
    Function to save in server a single code line.
    """
    ack_message = {'vid': 0, 'msg': 'NACK'}
    if request.vars.vid:
        print ('Request.vars: ' + str(request.vars))
        vid = int(request.vars.vid)
        res = db.code_lines.update_or_insert(
            db.code_lines.vid == vid,
            vid=request.vars.vid,
            vindex=request.vars.vindex,
            code_text=request.vars.code_text,
            saved=True)
        print('Id' + str(res))
        ack_message = {'vid': request.vars.vid, 'msg': 'ACK'}
    return response.json(ack_message)
        
