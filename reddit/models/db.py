# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.settings.extra_fields['auth_user']=[
	Field('Member_type','string',requires=IS_IN_SET(['User','Admin']),default='User',readable=False,writable=False),
	Field('City','string'),
	Field('Profile_Pic','upload'),
	]

auth.define_tables()
## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

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

set1=['World','India','Business','Sports','Entertainment']

db.define_table('cat',
		Field('Name','string')
	       )
db.define_table('Post',
		Field('Heading','string',required=True),
		Field('Category',db.cat,requires=IS_IN_DB(db,'cat.id','cat.Name')),
		Field('Post_details','text'),
		Field('User',default=auth.user_id,readable=False,writable=False),
		Field('Time','datetime',default=request.now,writable=False),
		Field('URL','string',notnull=True,requires=IS_URL()),
		Field('Rating','integer',default=100,required=True),
		Field('Image','upload'),
		Field('Video','string'),
		Field('User_liked','list:integer',readable=False)	
		)

db.define_table('Votes',
		Field('B_User',db.auth_user,default=auth.user_id,requires=IS_IN_DB(db,'auth_user.id','auth_user.id'),required=True,readable=False,writable=False),
		Field('Likes','integer',readable=False),
		Field('Post_id',db.Post,requires=IS_IN_DB(db,'Post.id','Post.id'),required=True)
	       )

db.define_table('Comment',
		Field('Post_no',db.Post,requires=IS_IN_DB(db,'Post.id','Post.id'),required=True),
		Field('Comment','text'),
		Field('By_user',default=auth.user_id,writable=False,readable=False),
		Field('Time','datetime',default=request.now),	       
		)
