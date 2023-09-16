#!/usr/bin/python3
""" Console Module """
import cmd
import re
import sys

import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty() and not stop:
            print('(hbnb) ', end='')
        return stop

    def args_split(self, string):
        """Splits a string into a list of strings based on ", ".

        Splits a string by comma and space but not in between double quotes
        or braces.

        Args:
            string(str): the string to split.
        """

        res = []
        buff = []
        in_quotes = False
        in_braces = 0

        for char in string:
            if char == '"':
                in_quotes = not in_quotes
            elif char == '{':
                in_braces += 1
            elif char == '}':
                in_braces -= 1

            if char in ', ' and not in_quotes and in_braces == 0:
                if buff:
                    res.append(''.join(buff).strip())
                    buff = []
            else:
                buff.append(char)

        if buff:
            res.append(''.join(buff).strip())

        return res

    def default(self, line):
        """Process dot method version of command.

        Args:
            line: the command line to proceess.
        """

        p_line = line.strip()

        pattern = r'(\w+).(\w+)\((.*?)\)'
        mtch = re.match(pattern, p_line)

        if mtch:
            cls_name = mtch.group(1)
            method = mtch.group(2)

            if method in HBNBCommand.dot_cmds:
                args = self.args_split(mtch.group(3))

                args = ' '.join(args)

                line = f"{method} {cls_name} {args}"

                return self.onecmd(line)

        return super().default(line)

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.classes[args]()
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        args = args.split(' ')
        c_name = args[0] if len(args) > 0 else ""
        c_id = args[1] if len(args) > 1 else ""

        key = f"{c_name}.{c_id}"
        objects = models.storage.all()

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        try:
            print(objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        args = args.split(' ')
        c_name = args[0] if len(args) > 0 else ""
        c_id = args[1] if len(args) > 1 else ""

        key = f"{c_name}.{c_id}"
        objects = models.storage.all()

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        try:
            del objects[key]
            models.storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        args = args.strip()
        objects = models.storage.all()

        print_list = []

        if args:
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances."""
        count = 0
        for k, v in models.storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Help information for the count command"""
        print("Usage: <class_name>.count()\n")

    def do_update(self, args):
        """ Updates a certain object with new info """
        args = self.args_split(args)

        c_name = args[0] if len(args) > 0 else ""
        c_id = args[1] if len(args) > 1 else ""
        attr_arg = args[2] if len(args) > 2 else ""

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = f"{c_name}.{c_id}"
        objects = models.storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        obj = objects[key]
        attrs = {}
        if attr_arg:
            if (attr_arg[0] == '{' and attr_arg[-1] == '}' and
                    type(eval(attr_arg)) is dict):
                attrs = eval(attr_arg)
            else:
                if attr_arg[0] == attr_arg[-1] == '"':
                    attr_arg = attr_arg[1:-1]

                attr_val = args[3] if len(args) > 3 else ""
                if attr_val and attr_val[0] == attr_val[-1] == '"':
                    attr_val = attr_val[1:-1]

                attrs[attr_arg] = attr_val

        if not attrs:
            print("** attribute name missing **")
            return

        for att_name, att_val in attrs.items():
            if not att_name:
                print("** attribute name missing **")
                return

            if not att_val:
                print("** value missing **")
                return

            # type cast as necessary
            if att_name in HBNBCommand.types:
                att_val = HBNBCommand.types[att_name](att_val)

            setattr(obj, att_name, att_val)

        obj.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
