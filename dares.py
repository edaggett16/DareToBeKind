from google.appengine.ext import ndb

class Dares(ndb.Model):
	# dare_number=ndb.IntegerProperty(required=False)
	dare=ndb.StringProperty(required=True, indexed=True)

