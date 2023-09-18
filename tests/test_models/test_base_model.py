#!/usr/bin/python3
"""Unit tests for models/base_model.py"""
import models
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """Unittests the BaseModel class."""

    def __init__(self, *args, **kwargs):
        """Initialize  instance."""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def tearDown(self):
        """Delete any created files."""
        objects = models.storage.all()
        keys = [k for k in objects.keys()]

        for key in keys:
            del objects[key]

        try:
            os.remove('file.json')
        except OSError:
            pass

    def test_default(self):
        """Test instantiation."""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test initialiazing with **kwargs."""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test updating with **kwargs."""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Test the save method."""
        i = self.value()
        i.save()
        key = f"{self.name}.{i.id}"
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test the string representation."""
        i = self.value()

        res = {}
        res.update(i.__dict__)

        del_key = '_sa_instance_state'
        if del_key in res.keys():
            del res[del_key]

        expected = f'[{self.name}] ({i.id}) {res}'
        self.assertEqual(len(str(i)), len(expected))

    def test_todict(self):
        """Test the to_dict method."""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test instantiating with **kwargs, None argument."""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        "Test instantiating with **kwargs, insufficient arguments."
        n = {'name': 'test'}
        new = self.value(**n)

        self.assertIsInstance(new.id, str)
        self.assertIsInstance(new.created_at, datetime.datetime)
        self.assertIsInstance(new.updated_at, datetime.datetime)
        self.assertEqual(new.name, 'test')

    def test_id(self):
        """Test the id attribute."""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test the created_at attribute."""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Test the updated_at attribute."""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        self.assertGreaterEqual(new.updated_at, new.created_at)
