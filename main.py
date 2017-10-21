#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.api import users
import webapp2
import jinja2
import random
import logging
from dares import Dares
from users import DareUsers
from users import Memories

from google.appengine.ext import ndb

env=jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

def findUser (user):
    user=users.get_current_user()
    find_dare_users=DareUsers.query().filter(DareUsers.email==user.email()).get()
    if find_dare_users==None:
        
        current_user=users.get_current_user()
        find_dare_users=DareUsers(email=current_user.email())
        find_dare_users.put()
    return find_dare_users



class Dares(ndb.Model):
    dare_number=ndb.IntegerProperty(required=False)
    dare=ndb.StringProperty(required=True, indexed=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template("main.html")
        user = users.get_current_user()
        
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
            (user.nickname(), users.create_logout_url('/')))
            d=DareUsers(email=user.email())
            d.put()
            # data["signed_in"]=True
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
            users.create_login_url('/'))
            
            #data["signed_in"]=False

        data = {"LogIn" : greeting}

        
        self.response.write(template.render(data))



# find how to use dare variable again to print dare on mydare page
class DareHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template("dare.html")

            
        dare_query=Dares.query()
        dare_results=dare_query.fetch()
        dare_result=dare_results[random.randint(0,len(dare_results) - 1)]

        

        dare={}
        dare["number"]=dare_result.dare_number #this part isn't necessary but we gonna leave it
        dare["dare"]=dare_result.dare
        self.response.write(template.render(dare))


    def post(self):
        user = users.get_current_user()
        
        m=Memories(writing=self.request.get("textMemories"), pictures=self.request.get("picMemories"), owner=user.email())
        m.put()
        template=env.get_template("dare.html")
        self.response.write(template.render())
        # results_template = env.get_template('results.html')



class ImageHandler(webapp2.RequestHandler):
    def get(self):
        # template=env.get_template("memories.html")
        # user = users.get_current_user()
        # picture_vars={"pictures":self.request.get("memory_id")}
        # d=DareUsers
        # d_key=d.put()
        # m=Memories(writing=self.request.get("textMemories"), pictures=self.request.get("picMemories"), owner=user.email())
        # logging.info(m)
        # key=m.put()
        # logging.info(key)
        # m=Memories.query().filter(Memories.owner==user.email())
        # find_memories=m.fetch()
        # pics=Memories.key.id().pictures
        
        # template=env.get_template("memories.html")
        # memories_query=Memories.query()
        # memories_results=memories_query.fetch()
        # pics=[memories_results[i]] for i in range (0, len(memories_results)-1)
        memory_id=self.request.get("mid")
        m=Memories.get_by_id(int(memory_id))
        self.response.headers['Content-Type'] = 'image/jpg'
        self.response.write(m.pictures)
    
        # self.response.out.write(find_memories[i].pictures)


class UserDare(webapp2.RequestHandler):
    def post(self):
        user_dare=self.request.get("daredare")
        d=Dares(dare=user_dare)
        d.put()
        template=env.get_template("main.html")
        self.response.write(template.render())

# class DareCompleted (webapp2.RequestHandler):
#     def post (self):
#         if (self.request.get("completed_dare"))=="True":
#             user=users.get_current_user()
#             dare_completed_user=findUser(user)
#             dare_completed_user.points+=1
#             dare_completed_user.put()


class MemoryHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template("dare.html")
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        text_memories=self.request.get("textMemories")
        image = self.request.get("picMemories")
        photo = Memories.pictures()
        photo.imageblob = db.Blob(image) 
        m=Memories(writing=text_memories, pictures=photo)
        m.put()
        template=env.get_template("dare.html")
        self.response.write(template.render())


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template=env.get_template("about.html")
        self.response.write(template.render())

# class CurrentHandler(webapp2.RequestHandler):
#     def get(self):
#         template=env.get_template("mydare.html")
    
        # dare_query=Dares.query()
        # dare_results=dare_query.fetch()
        # dare_result=dare_results[random.randint(0,len(dare_results) - 1)]

        # print len(dare_results)

        # dare={}
        # dare["number"]=dare_result.dare_number
        # dare["dare"]=dare_result.dare
        # self.response.write(template.render())




class MemoryHandler(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        template=env.get_template("memories.html")
        memories_query = Memories.query()
        memories=memories_query.filter(Memories.owner==user.email()).fetch()
        data = {"memories" : memories}
        self.response.write(template.render(data))
    
app = webapp2.WSGIApplication([
    ("/userdare", UserDare),
    ("/dare", DareHandler), 
    ("/", MainHandler), 
    # ("/darecompleted", DareCompleted),
    ("/memories", MemoryHandler),
    ("/about", AboutHandler),
    # ("/mydare", CurrentHandler),
    ("/image", ImageHandler)
], debug=True)
