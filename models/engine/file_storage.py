#!/usr/bin/python3
"""
Module: engine

mange saved and loaded files
"""
import json
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User


class FileStorage:
    """
    storage objects to file and retrieve them
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Get all Current objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Add a new object"""
        FileStorage.__objects[obj.__class__.__name__ + "." + obj.id] = obj

    def save(self):
        """Save current objects to file (Serialization)"""
        objects_dict = {}
        for k, v in FileStorage.__objects.items():
            objects_dict[k] = v.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(objects_dict))

    def reload(self):
        """Load saved objects from file (deserialization)"""
        try:
            with open(FileStorage.__file_path, "r") as f:
                objects_dict = json.loads(f.read())
                for k, v in objects_dict.items():
                    obj = eval(v['__class__'])(**v)
                    self.new(obj)
        except FileNotFoundError:
            pass
