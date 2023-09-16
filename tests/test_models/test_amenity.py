#!/usr/bin/python3
"""Unit tests for models/amenity.py."""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity


class test_Amenity(test_basemodel):
    """Unittest the Amenity class."""

    def __init__(self, *args, **kwargs):
        """Initialize instance."""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test the name attribute."""
        new = self.value()
        self.assertEqual(type(new.name), str)
