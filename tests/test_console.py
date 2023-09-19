#!/usr/bin/python3
"""Unittests for console.py."""
from console import HBNBCommand
from io import StringIO
import models
import os
import sys
import unittest
from unittest.mock import patch
import uuid

from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestConsoleBase(unittest.TestCase):
    """Base class for unittests for the console."""

    error_msgs = ["** class name missing **", "** class doesn't exist **",
                  "** instance id missing **", "** no instance found **",
                  "** attribute name missing **", "** value missing **",
                  "*** Unknown syntax: "]

    # BaseModel is not mapped in db storage, use State instead
    default_cls = 'State' if models.storage_type == 'db' else 'BaseModel'

    def tearDown(self):
        """Delete any created files and clear objects dictionary."""

        objects = models.storage.all()
        keys = [k for k in objects.keys()]
        for key in keys:
            models.storage.delete(objects[key])

        try:
            os.remove("file.json")
        except OSError:
            pass

    def get_output(self, cmd):
        """Returns the output of running a command on the console.

        Args:
            cmd: the command to run.
        """

        res = ""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
            res = f.getvalue().strip()

        return res


class TestConsole_help(TestConsoleBase):
    """Unit tests for the help command of the console."""

    def assert_output_help(self, cmd):
        """Tests the output of the help command.

        Args:
            cmd: the command argument to the help command.
        """

        cmd = f"help {cmd}"
        res = self.get_output(cmd)
        self.assertNotEqual(res, "")

    def test_help(self):
        """Tests the help command."""

        no_arg_res = self.get_output("help")
        self.assertNotEqual(no_arg_res, "")

        self.assert_output_help("help")
        self.assert_output_help("quit")
        self.assert_output_help("EOF")
        self.assert_output_help("create")
        self.assert_output_help("show")
        self.assert_output_help("destroy")
        self.assert_output_help("all")
        self.assert_output_help("update")


class TestConsole_other(TestConsoleBase):
    """Unit tests for miscellaneous commands of the console.

    Unittests for the quit commands and the handling of empty lines.
    """

    def test_quit(self):
        """Tests the quit command."""

        with patch('sys.stdout', new=StringIO()) as f:
            res_val = HBNBCommand().onecmd("quit")
            self.assertTrue(res_val)
            res = f.getvalue().strip()
            self.assertEqual(res, "")

        with patch('sys.stdout', new=StringIO()) as f:
            res_val = HBNBCommand().onecmd("quit other arguments")
            self.assertTrue(res_val)
            res = f.getvalue().strip()
            self.assertEqual(res, "")

    def test_EOF(self):
        """Tests the EOF (^D) command."""

        with patch('sys.stdout', new=StringIO()) as f:
            res_val = HBNBCommand().onecmd("EOF")
            self.assertTrue(res_val)
            res = f.getvalue().strip()
            self.assertEqual(res, "")

        with patch('sys.stdout', new=StringIO()) as f:
            res_val = HBNBCommand().onecmd("EOF other arguments")
            self.assertTrue(res_val)
            res = f.getvalue().strip()
            self.assertEqual(res, "")

    def test_emptyline(self):
        """Tests the handling of empty command lines."""

        res = self.get_output("")
        self.assertEqual(res, "")

        res = self.get_output("     ")
        self.assertEqual(res, "")

        res = self.get_output("\t")
        self.assertEqual(res, "")


class TestConsole_create(TestConsoleBase):
    """Unit tests for the create command of the console."""

    def assert_output_create_gen(self, cls, cmd):
        """Checks and returns the output of a given create command.

        Args:
            cls: the name of the class to create an instance of.
            cmd: the create command.
        """

        res = self.get_output(cmd)
        self.assertIsNotNone(res)
        self.assertIsInstance(uuid.UUID(res), uuid.UUID)
        key = f"{cls}.{res}"
        self.assertIn(key, models.storage.all())

        return key

    def assert_output_create(self, cls):
        """Tests the output of the create command.

        Args:
            cls: the name of the class to create an instance of.
        """
        cmd = f"create {cls}"
        self.assert_output_create_gen(cls, cmd)

    def test_create(self):
        """Tests the create command."""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_create("BaseModel")

        self.assert_output_create("User")
        self.assert_output_create("State")
        self.assert_output_create("City")
        self.assert_output_create("Amenity")
        self.assert_output_create("Place")
        self.assert_output_create("Review")

    def test_create_errors(self):
        """Makes sure the correct errors are displayed for create command."""

        res = self.get_output("create")
        self.assertEqual(res, self.error_msgs[0])

        res = self.get_output("create MyModel")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output('create p_name="p_val"')
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output('create MyModel p_name="p_val"')
        self.assertEqual(res, self.error_msgs[1])

    def assert_output_create_params(self, cls, p_name, p_val, p_exp):
        """Tests the output of the create command with parameters.

        Args:
            cls: the name of the class to create an instance of.
            p_name: the name of the paramter.
            p_val: the value of the parameter.
            p_exp: the expected value of the parameter after creation.
        """

        cmd = f"create {cls} {p_name}={p_val}"

        key = self.assert_output_create_gen(cls, cmd)
        objects = models.storage.all()
        inst = objects[key]

        self.assertEqual(getattr(inst, p_name, None), p_exp)

    def assert_output_create_params_types(self, cls):
        """Test the create command with parameters of different types.

        Args:
            cls: the name of the class to create an instance of.
        """

        p_name = 'string'
        p_val = '"string"'
        p_exp = 'string'
        self.assert_output_create_params(cls, p_name, p_val, p_exp)

        p_name = 'string_with_quotes'
        p_val = r'"string\"quotes"'
        p_exp = 'string"quotes'
        self.assert_output_create_params(cls, p_name, p_val, p_exp)

        p_name = 'string_with_spaces'
        p_val = '"string_with_spaces"'
        p_exp = 'string with spaces'
        self.assert_output_create_params(cls, p_name, p_val, p_exp)

        p_name = 'string_with_quotes_spaces'
        p_val = r'"string_with\"quotes_spaces"'
        p_exp = 'string with"quotes spaces'
        self.assert_output_create_params(cls, p_name, p_val, p_exp)

        p_name = 'float_p'
        p_val = 20.4
        p_exp = 20.4
        self.assert_output_create_params(cls, p_name, p_val, p_exp)

        p_name = 'integer'
        p_val = 3
        p_exp = 3
        self.assert_output_create_params(cls, p_name, p_val, p_exp)

    def test_create_params(self):
        """Test the create command with parameters"""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_create_params_types("BaseModel")

        self.assert_output_create_params_types("User")
        self.assert_output_create_params_types("State")
        self.assert_output_create_params_types("City")
        self.assert_output_create_params_types("Amenity")
        self.assert_output_create_params_types("Place")
        self.assert_output_create_params_types("Review")

    def test_create_params_multi(self):
        """Test the create command with multiple parameters."""

        cmd = f'create {self.default_cls} '
        cmd += r'string="\"My_little_house\"" '
        cmd += r'flt=20.4 integer=9'

        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]

        self.assertEqual(obj.string, '"My little house"')
        self.assertEqual(obj.flt, 20.4)
        self.assertEqual(obj.integer, 9)

    def test_create_params_invalid(self):
        """Ensure the create command skips parameters that don't fit."""

        cmd = f'create {self.default_cls} string1=string'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'string1'))

        cmd = f'create {self.default_cls} string2="s p a c e s"'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'string2'))

        cmd = f'create {self.default_cls} string3="quot"es"'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'string3'))

        cmd = f'create {self.default_cls} flt=20.4.5'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'flt'))

        cmd = f'create {self.default_cls} integer=--20'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'integer'))

        cmd = f'create {self.default_cls} other=["list"]'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'other'))

        cmd = f'create {self.default_cls} other={{dict: "val"}}'
        key = self.assert_output_create_gen(self.default_cls, cmd)
        obj = models.storage.all()[key]
        self.assertFalse(hasattr(obj, 'other'))


class TestConsole_count(TestConsoleBase):
    """Unit tests for the .count() command."""

    def assert_output_count(self, cls):
        """Tests the output of the .count() method.

        Args:
            cls: the name of the cls to test.
        """

        cmd = f'{cls}.count()'
        res = self.get_output(cmd)
        self.assertEqual(res, "0")

        inst1 = eval(cls)()
        inst1.save()
        res = self.get_output(cmd)
        self.assertEqual(res, "1")

        inst2 = eval(cls)()
        inst2.save()
        res = self.get_output(cmd)
        self.assertEqual(res, "2")

    def test_count(self):
        """Tets the .count() method."""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_count("BaseModel")

        self.assert_output_count("User")
        self.assert_output_count("State")
        self.assert_output_count("City")
        self.assert_output_count("Amenity")
        self.assert_output_count("Place")
        self.assert_output_count("Review")

    def test_count_no_cls(self):
        """Tests the .count() method without a class."""

        res = self.get_output(".count()")
        self.assertEqual(res, self.error_msgs[6] + ".count()")


class TestConsole_show(TestConsoleBase):
    """Unit tests for the show command of the console."""

    def get_output_show(self, cls, inst_id):
        """Returns the output of the show command.

        Args:
            cls: the name of the class of the the instance to show.
            inst_id: the id of the instance to show.
        """

        cmd = f"show {cls} {inst_id}"
        res = self.get_output(cmd)
        return res

    def assert_output_show(self, cls):
        """Tests the output of the show command.

        Args:
            cls: the name of the class of the instance to show.
        """

        inst = eval(cls)()
        inst.save()
        res = self.get_output_show(cls, inst.id)
        self.assertEqual(res, str(inst))

    def test_show(self):
        """Tests the show command."""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_show("BaseModel")

        self.assert_output_show("User")
        self.assert_output_show("State")
        self.assert_output_show("City")
        self.assert_output_show("Amenity")
        self.assert_output_show("Place")
        self.assert_output_show("Review")

    def test_show_errors(self):
        """Make sure correct errors are displayed for the show command."""

        res = self.get_output("show")
        self.assertEqual(res, self.error_msgs[0])

        res = self.get_output("show MyModel")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"show {self.default_cls}")
        self.assertEqual(res, self.error_msgs[2])

        res = self.get_output(f"show {self.default_cls} 123")
        self.assertEqual(res, self.error_msgs[3])

    def test_show_extra_args(self):
        """Make sure any other arguments to the show command are ignored."""

        b = eval(self.default_cls)()
        b.save()

        cmd = f"show {self.default_cls} {b.id} other arguments"
        res = self.get_output(cmd)
        self.assertEqual(res, str(b))

    def assert_output_show_dot(self, cls):
        """Tests the output of the .show() command.

        Args:
            cls: the name of the class of the instance to show.
        """

        inst = eval(cls)()
        inst.save()
        show_res = self.get_output_show(cls, inst.id)

        cmd = f"{cls}.show({inst.id})"
        res = self.get_output(cmd)
        self.assertEqual(res, show_res)
        self.assertEqual(res, str(inst))

    def test_show_dot(self):
        """Tests the .show() command"""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_show_dot("BaseModel")

        self.assert_output_show_dot("User")
        self.assert_output_show_dot("State")
        self.assert_output_show_dot("City")
        self.assert_output_show_dot("Amenity")
        self.assert_output_show_dot("Place")
        self.assert_output_show_dot("Review")

    def test_show_dot_errors(self):
        """Make sure correct errors are displayed for the .show() command."""

        res = self.get_output(".show()")
        self.assertEqual(res, self.error_msgs[6] + ".show()")

        res = self.get_output("MyModel.show()")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"{self.default_cls}.show()")
        self.assertEqual(res, self.error_msgs[2])

        res = self.get_output(f"{self.default_cls}.show(123)")
        self.assertEqual(res, self.error_msgs[3])

    def test_show_dot_extra_args(self):
        """Make sure any other arguments to the .show() command are ignored."""

        b = eval(self.default_cls)()
        b.save()

        cmd_str = f"{self.default_cls}.show({b.id}, other, arguments)"
        res = self.get_output(cmd_str)
        self.assertEqual(res, str(b))


class TestConsole_destroy(TestConsoleBase):
    """Unit tests for the destroy command of the console."""

    def assert_output_destroy(self, cls):
        """Tests the output of the destroy command.

        Args:
            cls: the name of the class of the instance to destroy.
        """

        inst = eval(cls)()
        inst.save()

        cmd = f"destroy {cls} {inst.id}"
        res = self.get_output(cmd)
        self.assertEqual(res, "")
        key = f"{cls}.{inst.id}"
        self.assertNotIn(key, models.storage.all())

    def test_destroy(self):
        """Tests the destroy command."""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_destroy("BaseModel")

        self.assert_output_destroy("User")
        self.assert_output_destroy("State")
        self.assert_output_destroy("City")
        self.assert_output_destroy("Amenity")
        self.assert_output_destroy("Place")
        self.assert_output_destroy("Review")

    def test_destroy_errors(self):
        """Make sure correct errors are displayed for the destroy command."""

        res = self.get_output("destroy")
        self.assertEqual(res, self.error_msgs[0])

        res = self.get_output("destroy MyModel")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"destroy {self.default_cls}")
        self.assertEqual(res, self.error_msgs[2])

        res = self.get_output(f"destroy {self.default_cls} 123")
        self.assertEqual(res, self.error_msgs[3])

    def test_destroy_extra_args(self):
        """Make sure any other arguments to the destroy command are ignored."""

        b = eval(self.default_cls)()
        b.save()

        cmd = f"destroy {self.default_cls} {b.id} other arguments"
        res = self.get_output(cmd)
        self.assertEqual(res, "")
        key = f"{self.default_cls}.{b.id}"
        self.assertNotIn(key, models.storage.all())

    def assert_output_destroy_dot(self, cls):
        """Tests the output of the .destroy() command.

        Args:
            cls: the name of the class of the instance to destroy.
        """

        inst = eval(cls)()
        inst.save()

        cmd = f"{cls}.destroy({inst.id})"
        res = self.get_output(cmd)
        self.assertEqual(res, "")
        key = f"{cls}.{inst.id}"
        self.assertNotIn(key, models.storage.all())

    def test_destroy_dot(self):
        """Tests the .destroy() command"""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_destroy_dot("BaseModel")

        self.assert_output_destroy_dot("User")
        self.assert_output_destroy_dot("State")
        self.assert_output_destroy_dot("City")
        self.assert_output_destroy_dot("Amenity")
        self.assert_output_destroy_dot("Place")
        self.assert_output_destroy_dot("Review")

    def test_destroy_dot_errors(self):
        """Test errors for the .destroy() command.

        Make sure correct errors are displayed for the .destroy() command.
        """

        res = self.get_output(".destroy()")
        self.assertEqual(res, self.error_msgs[6] + ".destroy()")

        res = self.get_output("MyModel.destroy()")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"{self.default_cls}.destroy()")
        self.assertEqual(res, self.error_msgs[2])

        res = self.get_output(f"{self.default_cls}.destroy(123)")
        self.assertEqual(res, self.error_msgs[3])

    def test_destroy_dot_extra_args(self):
        """Test other arguments to the .destroy() command.
        Make sure any other arguments to the .destroy() command are ignored.
        """

        b = eval(self.default_cls)()
        b.save()

        cmd = f"{self.default_cls}.destroy({b.id}, other, arguments)"
        res = self.get_output(cmd)
        self.assertEqual(res, "")
        key = f"{self.default_cls}.{b.id}"
        self.assertNotIn(key, models.storage.all())


class TestConsole_all(TestConsoleBase):
    """Unit tests for the all command of the console."""

    def assert_output_all(self, cls):
        """Tests the output of the all command.

        Args:
            cls: the name of the class to print all instances of.
        """

        objects = models.storage.all(cls)
        obj_ids = [obj.id for obj in objects.values()]

        cmd = f"all {cls}"
        res = self.get_output(cmd)

        for inst_id in obj_ids:
            self.assertIn(inst_id, res)

    def assert_output_all_cls(self, cls):
        """Tests the output of the all command for a class.

        Args:
            cls: the name of the class to print all instances of.
        """

        cmd = f"all {cls}"
        self.assertEqual(self.get_output(cmd), "[]")
        inst1 = eval(cls)()
        inst1.save()
        inst2 = eval(cls)()
        inst2.save()
        self.assert_output_all(cls)

    def test_all(self):
        """Tests the all command."""

        no_arg_res = self.get_output("all")
        self.assertEqual(no_arg_res, "[]")

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_all_cls("BaseModel")

        self.assert_output_all_cls("User")
        self.assert_output_all_cls("State")
        self.assert_output_all_cls("City")
        self.assert_output_all_cls("Amenity")
        self.assert_output_all_cls("Place")
        self.assert_output_all_cls("Review")

        objects = models.storage.all()
        obj_ids = [obj.id for obj in objects.values()]

        no_arg_res = self.get_output("all")

        for inst_id in obj_ids:
            self.assertIn(inst_id, no_arg_res)

    def test_all_errors(self):
        """Make sure correct errors are displayed for the all command."""

        res = self.get_output("all MyModel")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"all {self.default_cls} other arguments")
        self.assertEqual(res, self.error_msgs[1])

    def assert_output_all_dot_one(self, cls):
        """Tests the output of the .all() command with one instance of a class.

        Args:
            cls: the name of the class of the instance to all.
        """

        inst = eval(cls)()
        inst.save()

        res = self.get_output(f"{cls}.all()")
        self.assertIn(inst.id, res)

    def test_all_dot(self):
        """Tests the .all() command"""

        # BaseModel is not mapped in db storage
        if models.storage_type != 'db':
            self.assert_output_all_dot_one("BaseModel")

        self.assert_output_all_dot_one("User")
        self.assert_output_all_dot_one("State")
        self.assert_output_all_dot_one("City")
        self.assert_output_all_dot_one("Amenity")
        self.assert_output_all_dot_one("Place")
        self.assert_output_all_dot_one("Review")

    def test_all_dot_errors(self):
        """Test errors for the .all() command.

        Make sure correct errors are displayed for the .all() command.
        """

        res = self.get_output(".all()")
        self.assertEqual(res, self.error_msgs[6] + ".all()")

        res = self.get_output("MyModel.all()")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"{self.default_cls}.all(other, arguments)")

        self.assertEqual(res, self.error_msgs[1])


class TestConsole_update(TestConsoleBase):
    """Unit tests for the update command of the console."""

    def assert_output_update(self, cmd, cls, inst_id, attr_name, attr_val):
        """Assert that an instance is updated.

        Args:
            cmd: the update command used
            cls: the name of the class of the instance to update
            inst_id: the id of the instance to update
            attr_name: the name of the attribute to add or update.
            attr_val: the new value of the attribute.
        """
        res = self.get_output(cmd)
        self.assertEqual(res, "")

        key = f"{cls}.{inst_id}"
        objects = models.storage.all()
        self.assertIn(key, objects)

        obj = objects[key]
        self.assertTrue(hasattr(obj, attr_name))
        obj_attr = getattr(obj, attr_name)

        try:
            attr_val = eval(str(attr_val))
        except Exception:
            pass

        self.assertTrue(obj_attr == attr_val)

    def assert_output_update_cmds(self, cls, inst_id, attr_name, attr_val):
        """Tests the output of all version of the update command.

        Args:
            cls: the name of the class of the instance to update
            inst_id: the id of the instance to update
            attr_name: the name of the attribute to add or update.
            attr_val: the new value of the attribute.
        """

        # update cls inst_id attr_name attr_val
        cmd = f'update {cls} {inst_id} {attr_name} '
        cmd += f'"{attr_val}"' if type(attr_val) is str else f'{attr_val}'
        self.assert_output_update(cmd, cls, inst_id, attr_name, attr_val)

        # cls.update(inst_id, "attr_name", attr_val)
        cmd = f'{cls}.update({inst_id}, "{attr_name}_dot", '
        cmd += f'"{attr_val}")' if type(attr_val) is str else f'{attr_val})'
        self.assert_output_update(cmd, cls, inst_id, attr_name, attr_val)

        # cls.update(inst_id, {'attr_name': atrr_val}
        cmd = f"{cls}.update({inst_id}, {{'{attr_name}_dot_dict1': "
        if type(attr_val) is str:
            cmd += f'"{attr_val}"}})'
        else:
            cmd += f'{attr_val}}})'
        self.assert_output_update(cmd, cls, inst_id, attr_name, attr_val)

        # cls.update(inst_id, {"attr_name": atrr_val}
        cmd = f'{cls}.update({inst_id}, {{"{attr_name}_dot_dict2": '
        if type(attr_val) is str:
            cmd += f'"{attr_val}"}})'
        else:
            cmd += f'{attr_val}}})'
        self.assert_output_update(cmd, cls, inst_id, attr_name, attr_val)

    def assert_output_update_types(self, cls):
        """Tests the output of the update command with different types.

        Args:
            cls: the name of the class of the the instance to update
        """
        inst = eval(cls)()
        inst.save()

        attr_name = "string_arg"
        attr_val = "string"
        self.assert_output_update_cmds(cls, inst.id, attr_name, attr_val)

        attr_name = "int_arg"
        attr_val = 89
        self.assert_output_update_cmds(cls, inst.id, attr_name, attr_val)

        attr_name = "float_arg"
        attr_val = 12.7
        self.assert_output_update_cmds(cls, inst.id, attr_name, attr_val)

        attr_name = "space_string_arg"
        attr_val = "one two"
        self.assert_output_update_cmds(cls, inst.id, attr_name, attr_val)

        attr_name = "string_int_arg"
        attr_val = "90"
        self.assert_output_update_cmds(cls, inst.id, attr_name, attr_val)

        attr_name = "string_float_arg"
        attr_val = "5.4"
        self.assert_output_update_cmds(cls, inst.id, attr_name, attr_val)

    def test_update(self):
        """Tests the update command."""

        # BaseModel is not mapped in db storage
        if models.storage_type == 'db':
            self.assert_output_update_types("BaseModel")

        self.assert_output_update_types("User")
        self.assert_output_update_types("State")
        self.assert_output_update_types("City")
        self.assert_output_update_types("Amenity")
        self.assert_output_update_types("Place")
        self.assert_output_update_types("Review")

    def test_update_errors(self):
        """Make sure correct errors are displayed for the update command."""

        res = self.get_output("update")
        self.assertEqual(res, self.error_msgs[0])

        res = self.get_output("update MyModel")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"update {self.default_cls}")
        self.assertEqual(res, self.error_msgs[2])

        res = self.get_output(f"update {self.default_cls} 123")
        self.assertEqual(res, self.error_msgs[3])

        b = eval(self.default_cls)()
        b.save()
        cmd = f"update {self.default_cls} {b.id}"
        res = self.get_output(cmd)
        self.assertEqual(res, self.error_msgs[4])

        cmd = f"update {self.default_cls} {b.id} attr"
        res = self.get_output(cmd)
        self.assertEqual(res, self.error_msgs[5])

    def test_update_extra_args(self):
        """Make sure any other arguments to the update command are ignored."""

        b = eval(self.default_cls)()
        b.save()

        attr = "attr"
        attr_val = 89

        cmd = (f"update {self.default_cls} {b.id} {attr} {attr_val}"
               + " other arguments")
        res = self.get_output(cmd)
        self.assertEqual(res, "")

        key = f"{self.default_cls}.{b.id}"
        objects = models.storage.all()
        self.assertIn(key, models.storage.all())

        obj = objects[key]
        self.assertTrue(hasattr(obj, attr))
        self.assertTrue(getattr(obj, attr) == attr_val)

    def test_update_dot_errors(self):
        """Make sure correct errors are displayed for the .update() command."""

        res = self.get_output(".update()")
        self.assertEqual(res, self.error_msgs[6] + ".update()")

        res = self.get_output("MyModel.update()")
        self.assertEqual(res, self.error_msgs[1])

        res = self.get_output(f"{self.default_cls}.update()")
        self.assertEqual(res, self.error_msgs[2])

        res = self.get_output(f"{self.default_cls}.update(123)")
        self.assertEqual(res, self.error_msgs[3])

        b = eval(self.default_cls)()
        b.save()
        cmd = f"{self.default_cls}.update({b.id})"
        res = self.get_output(cmd)
        self.assertEqual(res, self.error_msgs[4])

        cmd = f'{self.default_cls}.update({b.id}, "attr")'
        res = self.get_output(cmd)
        self.assertEqual(res, self.error_msgs[5])

        cmd = f"{self.default_cls}.update({b.id}, {{}})"
        res = self.get_output(cmd)
        self.assertEqual(res, self.error_msgs[4])

        cmd = f'{self.default_cls}.update({b.id}, {{"attr": ""}})'
        res = self.get_output(cmd)
        self.assertEqual(res, self.error_msgs[5])

    def test_update_dot_extra_args(self):
        """Make sure any other arguments to the .update() command are ignored.
        """

        b = eval(self.default_cls)()
        b.save()

        attr = "attr"
        attr_val = 89

        cmd = (f"{self.default_cls}.update({b.id}, {attr}, {attr_val},"
               + " other, arguments)")
        res = self.get_output(cmd)
        self.assertEqual(res, "")

        key = f"{self.default_cls}.{b.id}"
        objects = models.storage.all()
        self.assertIn(key, models.storage.all())

        obj = objects[key]
        self.assertTrue(hasattr(obj, attr))
        self.assertTrue(getattr(obj, attr) == attr_val)


if __name__ == "__main__":
    unittest.main()
