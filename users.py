from google.appengine.ext import ndb

class DareUsers(ndb.Model):
	email=ndb.StringProperty()
	points=ndb.IntegerProperty(default=0)
	
class Memories(ndb.Model):
	pictures=ndb.BlobProperty(required=False)
	writing=ndb.StringProperty(required=False)
	owner=ndb.StringProperty() #DareUsers.email

