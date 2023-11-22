#!/usr/bin/python3
"""
Module_name: model

Create base class
it will define all common attributes/methods for other classes
it will be useful to be used as superclass
"""

import datetime as dt
import uuid
import models


class BaseModel:
    """
    Base class to be inherited

    Attr:
       id: uniq identifier for all instances
       created_at: datetime(ISO format) of instance created time
       updated_at: datetime(ISO format) of any object change
    """

    def __init__(self, *arg, **kwarg):
        if kwarg:
            self.__from_dict(kwarg)
        else:
            self.__new()

    def __new(self):
        """Set new Instance attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = dt.datetime.now()
        self.updated_at = dt.datetime.now()
        models.storage.new(self)

    def __from_dict(self, kwarg):
        """create an instace from object dictionary representation"""
        for attr, value in kwarg.items():
            if attr != "__class__":
                setattr(self, attr, value)
        self.created_at = dt.datetime.strptime(self.created_at,
                                               "%Y-%m-%dT%H:%M:%S.%f")
        self.updated_at = dt.datetime.strptime(self.updated_at,
                                               "%Y-%m-%dT%H:%M:%S.%f")

    def save(self):
        """save object to file (Note:update object attributes (updated_at))"""
        self.updated_at = dt.datetime.now()
        models.storage.save()

    def to_dict(self):
        """Create a dictionary representation of instance attributes"""
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = obj_dict["created_at"].isoformat()
        obj_dict["updated_at"] = obj_dict["updated_at"].isoformat()
        return obj_dict

    def __str__(self):
        """Instance string repr"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
