#!/usr/bin/env python
"""
A simple photo representation for the iOS-based OpenPhoto project.

Kyle Buza (BuzaMoto)
buzamoto.com
2/5/11
"""

import sqlalchemy
from elixir import *

import datetime 

class Photo(Entity):
  
    photo_id = Field(String(length=100), primary_key=True)
    event_id = Field(String(length=100))
    user_id = Field(String(length=100))
    comment = Field(String(length=500))
    photo_latitude = Field(Float())
    photo_longitude = Field(Float())
    photo_width = Field(Integer())
    photo_height = Field(Integer())
    thumb_width = Field(Integer())
    thumb_height = Field(Integer())
    timestamp = Field(DateTime())

    def __init__(self, photo_id, event_id, user_id, photo_width, photo_height, thumb_width, thumb_height, lat, lon, comment):
        self.photo_id = photo_id
        self.event_id = event_id 
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
        return "<Photo ('%s','%s', '%s', Latitude: %d, Longitude: %d, Comment %s)>" % (self.photo_id, self.event_id, self.user_id, self.photo_latitude, self.photo_longitude, self.comment)
