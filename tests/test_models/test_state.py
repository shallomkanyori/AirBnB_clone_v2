#!/usr/bin/python3
"""Unit tests for models/state.py."""
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """Unittest the State class."""

    def __init__(self, *args, **kwargs):
        """Initialize instance."""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Test the name attribute."""
        new = self.value()
        self.assertEqual(type(new.name), str)
