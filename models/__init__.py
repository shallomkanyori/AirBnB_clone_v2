#!/usr/bin/python3
"""This module instantiates a storage object.

    If the environment variable HBNB_TYPE_STORAGE is db, a database storage is
    created. Otherwise, a file storage object is created.
"""
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE', default='')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
    storage.reload()

else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
    storage.reload()
