# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to web2py!"
    return dict(message=T('Hello World'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
@auth.requires_login()
def index():
	flag=0
	ca=db(db.cat.id>0).select()
	x=db(db.Post.id>0).select(orderby=db.Post.Rating)
	y=db(db.Post.User==db.auth_user.id).select(db.auth_user.first_name,db.auth_user.Profile_Pic,orderby=db.Post.Rating)
	return locals()
@auth.requires_login()
def lall():
	flag=0
	ca=db(db.cat.id>0).select()
	x=db(db.Post.id>0).select(orderby=db.Post.Rating)
	y=db(db.Post.User==db.auth_user.id).select(db.auth_user.first_name,db.auth_user.Profile_Pic,orderby=db.Post.Rating)
#z=db(db.auth_user.id==db.Votes.By_user).select()
#	response.flash= "Like karne ke liye dhanyavaad _^_!"
#	if (len(request.args)!=0):
#		r=request.args[0]
#		p=request.args[1]
#		b=db(db.Post.id==(int(r)+1)).select()	
#	print x
#		response.flash= "Like karne ke liye dhanyavaad _^_!"
#		if (request.args[1]=="like" ):	
#			b=db(db.Post.id==(int(r)+1)).select()
#			print db(db.Post.User_liked.contains(auth.user.id)).select()
#			rec=db(db.Post.User_liked.contains(auth.user.id)).select()
#			if  (len(rec)):
#				print rec[0]['id']
#				print r
#				for j in range (len(rec)):
#					if (rec[j]['id']==int(r)+1):
#						flag=1
#				if (flag==1):
#					redirect(URL("lall"))
#					response.flash= "Kitni baar like karega!!"
				
#				else:			
#					response.flash= "Like karne ke liye dhanyavaad _^_!"
#					a=db(db.Post.id==(int(r)+1)).update(Rating=b[0]['Rating']+5)	
#					db.Post.User_liked.append(auth.user.id)					
#				db(db.Post.id==(int(r)+1)).update(User_liked=auth.user.id)
#					redirect(URL("lall"))
#			else:
#				response.flash= "Like karne ke liye dhanyavaad _^_!"
#				a=db(db.Post.id==(int(r)+1)).update(Rating=b[0]['Rating']+5)	
#				db.Post.User_liked.append(auth.user.id)					
#				db(db.Post.id==(int(r)+1)).update(User_liked=auth.user.id)	
#				redirect(URL("lall"))
#		elif (request.args[1]=="dislike"):	
#			b=db(db.Post.id==int(r)+1).select(db.Post.Rating)
#			a=db(db.Post.id==int(r)+1).update(Rating=b[0]['Rating']-3)
#			redirect(URL("lall"))
	return locals()

@auth.requires_login()
def l():
	r=request.args[0]
	p=request.args[1]
	p=int(p)
	r= int(r)
#	Votes.Post_id=r
	z=db((db.Votes.Post_id==r) & (db.Votes.B_User==auth.user.id)).select()
	if (len(db((db.Votes.Post_id==r) & (db.Votes.B_User==auth.user.id)).select())!=0):
		if (p==5 and z[0]['Likes']==-3):
			pos=db(db.Post.id==r).select(db.Post.Rating)
			db((db.Votes.id==z[0]['id'])).delete()
			db(db.Post.id==r).update(Rating=pos[0]['Rating']+3)
			redirect(URL('lall'))
		elif (p==-3 and z[0]['Likes']==5):
			pos=db(db.Post.id==r).select(db.Post.Rating)
			db((db.Votes.id==z[0]['id'])).delete()
			db(db.Post.id==r).update(Rating=pos[0]['Rating']-5)
			redirect(URL('lall'))
		else :
			session.flash='Kitni baar like karoge?!?!'
			redirect(URL('lall'))

	elif ((len(db((db.Votes.Post_id==r) & (db.Votes.B_User==auth.user.id)).select())==0) or (len(db(db.Votes.id>0).select())==0)):
	 	db.Votes.insert(B_User=auth.user.id,Likes=p,Post_id=r)
		rating=100
		rec=db(db.Votes.Post_id==r).select()
		for i in range (len(rec)):
			print rec[i]['Likes']
			rating=rating+rec[i]['Likes']
			print rating
		db(db.Post.id==r).update(Rating=rating)
		session.flash='Like ya dislike karne ke liye dhanyawaad _^_!'
		redirect(URL('lall'))
	return locals()

@auth.requires_login()
def postnews():
	form=SQLFORM(db.Post)
	if form.process().accepted:
		response.flash= 'News Posted!'
	return locals()

@auth.requires_login()
def listcat():	
	p=db(db.Post.id>0).select()
	y=request.args[0]
	x=db(db.Post.Category==y).select(orderby=db.Post.Rating)
	q=db((db.Post.User==db.auth_user.id) & (db.Post.Category==y)).select(db.auth_user.first_name,db.auth_user.Profile_Pic,orderby=db.Post.Rating)
	cat=db(db.cat.id==y).select()
	print q
	if (len(x)>0):		
		ca=db(db.cat.id>0).select()
		return locals()	
	else :
		ca=db(db.cat.id>0).select()
		return locals()

@auth.requires_login()
def addcomment():
	r=request.args[0]
	r=int(r)
	form=SQLFORM(db.Comment)
	form.vars.Post_no=r
#	form.vars.Post_no.writable=False
	if form.process().accepted :
		session.flash= 'Comment Recorded'
		redirect(URL('addcomment', args=(r)))
	a=db(db.Comment.Post_no==r).select()
	b=db((db.Comment.Post_no==r) & (db.auth_user.id==db.Comment.By_user)).select(db.auth_user.first_name,db.Comment.Time)
	return locals()

@auth.requires_login()
def showcomments():
	r=request.args[0]
	r=int(r)
	a=db(db.Comment.Post_no==r).select()
	b=db((db.Comment.Post_no==r) & (db.auth_user.id==db.Comment.By_user)).select(db.auth_user.first_name,db.Comment.Time)
	return locals()

@auth.requires_login()
def deletepost():
	if (len(request.args)!=0):
		r=request.args[0]
		p=request.args[1]
		r=int(r)
		rec=db(db.Post.id==r).select(db.Post.User)
		print r
		print auth.user.id
		print rec[0]['User']
		if (auth.user.id==rec[0]['User'] or auth.user.Member_type=='Admin'):
			db(db.Post.id==r).delete()
			redirect(URL(p))
		else:
			session.flash='You cannot delete others\' post'
			redirect(URL(p))
	return locals()

@auth.requires_login()
def delaccount():
	if (auth.user.Member_type!='Admin'):
		session.flash='You have no right to do this! :('
		redirect(URL('lall'))
	else:
		acc=db(db.auth_user.Member_type=='User').select()
	return locals()

@auth.requires_login()
def d():
	if (auth.user.Member_type!='Admin'):
		sessiom.flash='You have no right to do this! :('
		redirect(URL('lall'))
	else :
		r=request.args[0]
		db(r==db.auth_user.id).delete()
		db(r==db.Post.User).delete()
		db(r==db.Votes.B_User).delete()
		redirect(URL('delaccount'))
	return locals()

@auth.requires_login()
def addcat():
	if (auth.user.Member_type=='User'):
		form=""
		response.flash= 'Only the Admin can add categories'
	else :
		form=SQLFORM(db.cat)
		if form.process().accepted :
			response.flash= 'Category registered!'
	return locals()

@auth.requires_login()
def updatepost():
	if (len(request.args)!=0):
		r=request.args[0]
		r=int(r)
		rec=db(db.Post.id==r).select(db.Post.User)
		if (auth.user.id==rec[0]['User']):
			form= crud.update(db.Post,r)
			if form.process().accepted :
				response.flash= 'Post Updated'
#			return dict(form=form)
		else:
			session.flash= 'Cant Update Other\'s post!'
			redirect(URL('lall'))
	else :
		session.flash='Sorry please enter through the link for updating a post!'
		redirect(URL('lall'))
	return locals()


