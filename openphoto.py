#!/usr/bin/env python

"""
A simple web server that can handle photo uploads from the OpenPhoto iOS application.
Uses the Tornado web server:  http://www.tornadoweb.org

Created by Kyle Buza on 2/5/11.
Copyright 2010 BuzaMoto. All rights reserved.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import json
import base64

import tornado.web
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from sqlalchemy import desc
from sqlalchemy import create_engine

from elixir import *
from photo import *

define("port", default=25006, help="Port to run the server on.", type=int)

#Change this to a location that you'd like your photos stored on your filesystem.
PHOTO_DIR_PREFIX = 'static/data/'

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/hello", HelloHandler),
            (r"/upload", UploadHandlerLocal),
            (r"/comment", CommentHandler)
        ]
        settings = dict(
            static_path= os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class HelloHandler(tornado.web.RequestHandler):

    def get(self):
    	res = { 'code' : 200, 'status' : 'success', 'title' : 'My OpenPhoto Test Server'}
    	self.write(tornado.escape.json_encode(res))

class CommentHandler(tornado.web.RequestHandler):
  
    def post(self):
      photo_id = self.get_argument("photo_id", None)
      comment = self.get_argument("comment", None)
      if photo_id == None or comment == None:
        res = { 'status' : 'failure'}
        self.write(tornado.escape.json_encode(res))
        return
        	
      _photo = Photo.get_by(photo_id=photo_id)
 
      if not _photo:
        res = { 'status' : 'nonexistent'}
        self.write(tornado.escape.json_encode(res))
        return
        
      _photo.comment = comment
      session.commit()
        
      res = { 'status' : 'success'}
      self.write(tornado.escape.json_encode(res))

class UploadHandlerLocal(tornado.web.RequestHandler):

    def post(self):

      photo_id = self.get_argument("photo_id", None)
      user_id = self.get_argument("user_id", None)
      comment = self.get_argument("comment", "")
      photo_width = self.get_argument("photo_width", None)
      photo_height = self.get_argument("photo_height", None)
      thumb_width = self.get_argument("thumb_width", None)
      thumb_height = self.get_argument("thumb_height", None)
      imgdata_b64 = self.get_argument("photo_b64", None)
      imgdata_thumb_b64 = self.get_argument("photo_thumb_b64", None)
      
      latitude = self.get_argument("latitude", 0)
      longitude = self.get_argument("longitude", 0)

      if photo_id == None or \
         user_id == None or \
         imgdata_b64 == None or \
         imgdata_thumb_b64 == None or \
         photo_width == None or \
         photo_height == None or \
         thumb_height == None or \
         thumb_width == None:
        res = { 'status' : 'failure'}
        self.write(tornado.escape.json_encode(res))
        return
        	
      _photo = Photo.get_by(photo_id=photo_id)
      if _photo == None:
        imgbytes = base64.decodestring(imgdata_b64)
        thumbbytes = base64.decodestring(imgdata_thumb_b64)
        try:
          f = open(PHOTO_DIR_PREFIX+photo_id+'.png', "w")
          f.write(imgbytes)
          f.close()
          f = open(PHOTO_DIR_PREFIX+photo_id+'_thumb.png', "w")
          f.write(thumbbytes)
          f.close()
        except Exception, e:
          res = { 'status' : 'failure'}
          self.write(tornado.escape.json_encode(res))
          return

      else:
        res = { 'status' : 'exists'}
        self.write(tornado.escape.json_encode(res))
        return
      try:
        _photo = Photo(photo_id, user_id, photo_width, photo_height, thumb_width, thumb_height, latitude, longitude, comment)
        session.commit()
      except Exception, e:
        res = { 'status' : 'failure'}
        self.write(tornado.escape.json_encode(res))
        return

      res = { 'status' : 'success'}
      self.write(tornado.escape.json_encode(res))

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

def init_db():
  metadata.bind = create_engine("sqlite:///openphoto.sqlite", pool_recycle=3600)
  setup_all()
  create_all()

if __name__ == "__main__":
  init_db()
  main()
