#!/usr/bin/env python
"""
A simple photo representation for the iOS-based OpenPhoto project.

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


import sqlalchemy
from elixir import *

import datetime 

class Photo(Entity):
  
    photo_id = Field(String(length=100), primary_key=True)
    user_id = Field(String(length=100))
    comment = Field(String(length=500))
    photo_latitude = Field(Float())
    photo_longitude = Field(Float())
    photo_width = Field(Integer())
    photo_height = Field(Integer())
    thumb_width = Field(Integer())
    thumb_height = Field(Integer())
    timestamp = Field(DateTime())

    def __init__(self, photo_id, user_id, photo_width, photo_height, thumb_width, thumb_height, lat, lon, comment):
        self.photo_id = photo_id
        self.comment = comment
        self.user_id = user_id
        self.photo_latitude = lat
        self.photo_longitude = lon
        self.photo_width = photo_width 
        self.photo_height = photo_height
        self.thumb_width = thumb_width 
        self.thumb_height = thumb_height
        self.timestamp = datetime.datetime.now()
        
    def __repr__(self):
        return "<Photo ('%s','%s', Latitude: %d, Longitude: %d, Comment %s)>" % (self.photo_id, self.user_id, self.photo_latitude, self.photo_longitude, self.comment)
