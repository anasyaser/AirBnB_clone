#!/usr/bin/python3
"""
Entry point

Run AirBnB web application from console
"""

import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Intialize User console commands"""
    prompt = "(hbnb) "

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.objects = storage.all()
        self.classes = {'BaseModel': BaseModel, 'User': User, 'City': City,
                        'Amenity': Amenity, 'Place': Place, 'State': State,
                        'Review': Review}

    def __is_valid_input(self, line, no_args=1):
        """Check validation of users command arguments"""
        args = line.split() if line else []
        msgs = [
            "** class name missing **",
            "** instance id missing **",
            "** attribute name missing **",
            "** value missing **",
            "** attribute name missing **",
            "** value missing **"
                ]
        i = 0
        while (i < no_args):
            if i >= len(args):
                print(msgs[i])
                return False
            if i == 0:
                if args[0] not in self.classes:
                    print("** class doesn't exist **")
                    return False
            if i == 1:
                if ".".join(args[:2]) not in self.objects:
                    print("** no instance found **")
                    return False
            i += 1
        return True

    def do_create(self, line):
        """Create new instance"""
        if self.__is_valid_input(line):
            obj = self.classes[line]()
            storage.save()
            print(obj.id)

    def do_show(self, line):
        """print string representation of instance"""
        # Not that no handling for args more than required and may cause errors
        if self.__is_valid_input(line, 2):
            key = line.replace(" ", ".")
            print(storage.all().get(key))

    def do_destroy(self, line):
        """Delete required instance object"""
        if self.__is_valid_input(line, 2):
            key = line.replace(" ", ".")
            del self.objects[key]
            storage.save()

    def do_all(self, line):
        """print string representation of all objects
        based on valid given class or not"""
        lst = []
        if self.__is_valid_input(line, 1 if line else 0):
            for k, v in self.objects.items():
                if line and line not in k:
                    continue
                lst.append(v.__str__())
            print(lst)

    def do_update(self, line):
        """Update object attribute"""
        if self.__is_valid_input(line, 4):
            def handle_args(text):
                lst = []
                arg = ""
                is_quote = False
                for char in text:
                    if char == "'" or char == '"':
                        is_quote = not is_quote
                    if char == " " and not is_quote:
                        lst.append(arg)
                        arg = ""
                    else:
                        arg += char
                lst.append(arg)
                return lst
            args = handle_args(line)
            obj = self.objects.get(".".join(args[:2]))
            if hasattr(obj, args[2]):
                obj_attr = getattr(obj, args[2])
                setattr(obj, args[2], type(obj_attr)(args[3].replace('"', '')))
            else:
                setattr(obj, args[2], args[3].replace('"', ''))
            storage.save()

    def emptyline(self):
        """handling emptyline command"""
        pass

    def do_quit(self, line):
        """command to exit the programe"""
        return True

    def help_quit(self):
        print("Command to exit the program\n")

    def help_create(self):
        print("Command to create new instances. Usage:create <class type>\n")

    def help_show(self):
        print('Prints the string representation of an instance based on '
              'the class name.\nUsage: show <class name> <instance id>')

    def help_destroy(self):
        print('Deletes an instance based on the class name and id.\n'
              'Usage: destroy <class name> <instance id>')

    def help_all(self):
        print('Prints all string representation of all instances '
              'based or not on the class name.\n'
              'Usage: all <class name>')

    def help_update(self):
        print('Updates an instance based on the class '
              'name and id by adding or updating attribute.\n'
              'Usage: update <class name> <class instance id> <attribute name> '
              '<attribute value>')

    def do_EOF(self, line):
        """Exit the program"""
        print()
        return True

    def do_count(self, line):
        """Count number of objects of class"""
        cnt = 0
        for k, v in self.objects.items():
            if line in k:
                cnt += 1
        print(cnt)

    def precmd(self, line):
        if "." in line:
            class_name = line.split(".")[0]
            cmd = re.findall(r'\.(.*?)\(', line)
            args = re.findall(r'\("([^)]+)"\)', line)
            return " ".join([cmd[0], class_name,
                             args[0].replace(",", "").replace('"', "")
                             if args else ""])
        return line

if __name__ == '__main__':
    HBNBCommand().cmdloop()
