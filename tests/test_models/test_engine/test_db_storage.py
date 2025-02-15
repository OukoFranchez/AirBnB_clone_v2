#!/usr/bin/python3

"""
unittests for db_storage module
"""


import unittest
from models.engine.db_storage import DBStorage
from models.engine import db_storage
from models import storage
from os import getenv
from models import City, State
from models import storage
from console import HBNBCommand
import MySQLdb
import pep8

db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', 'file storage not supported')
class test_my_storage(unittest.TestCase):
    """
    Testing my_storage class
    """

    @classmethod
    def setUpClass(cls):
        """ Sets up test environment """
        cls.my_storage = DBStorage()
        cls.command = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """
        Tears down the test environment
        """

        del cls.my_storage

    def setUp(self):
        """ creates a MySQLdb connection """

        uname = getenv("HBNB_MYSQL_USER")
        passw = getenv("HBNB_MYSQL_PWD")
        dbhost = getenv("HBNB_MYSQL_HOST")
        dbname = getenv("HBNB_MYSQL_DB")
        self.test_engine = MySQLdb.connect(
            host=dbhost,
            user=uname, password=passw,
            database=dbname
        )

    def tearDown(self):
        """ close the db connection """

        self.test_engine.close()

    def test_my_storage_methods(self):
        """
            Checks if methods exists
        """

        self.assertTrue(hasattr(self.my_storage, "all"))
        self.assertTrue(hasattr(self.my_storage, "__init__"))
        self.assertTrue(hasattr(self.my_storage, "new"))
        self.assertTrue(hasattr(self.my_storage, "save"))
        self.assertTrue(hasattr(self.my_storage, "delete"))
        self.assertTrue(hasattr(self.my_storage, "reload"))

    def test_model_storage(self):
        """ Tests storage is an instance of DBStorage """

        self.assertTrue(isinstance(storage, DBStorage))

    def test_create(self):
        """ Test adding a new object """

        # initialize sqlalchemy connection
        storage.reload()

        # getting the initial objects
        cur = self.test_engine.cursor()
        cur.execute("SELECT * FROM states;")
        init_objs = cur.fetchall()

        # creating a new object and commit transaction to save the new object
        self.command.onecmd('create State name="California"')
        self.test_engine.commit()

        # Retrieving the data
        cur.execute("SELECT * FROM states;")
        new_objs = cur.fetchall()

        # Confirming the results
        self.assertTrue(len(new_objs) > len(init_objs))

    def test_new_obj(self):
        """ Testing that a new object is created """

        new_obj = State(name="California")
        self.assertTrue(new_obj)
        self.assertTrue(hasattr(new_obj, 'id'))
        self.assertTrue(hasattr(new_obj, 'name'))
        self.assertTrue(hasattr(new_obj, 'updated_at'))
        self.assertTrue(hasattr(new_obj, 'created_at'))

    def test_dbstorage_all(self):
        """ Testing the all method of DBStorage """

        storage.reload()

        # get the initial objects
        result = storage.all()
        cur = self.test_engine.cursor()
        cur.execute("SELECT * FROM states;")
        init_objs = cur.fetchall()
        self.assertTrue(len(result) == len(init_objs))

        # create a new object and commit transaction to save the new object
        self.command.onecmd('create State name="California"')
        self.test_engine.commit()

        # Retrieving the data
        cur.execute("SELECT * FROM states;")
        new_objs = cur.fetchall()
        result = storage.all()

        # Confirm the results
        self.assertTrue(len(result) == len(new_objs))
        self.assertIsInstance(result, dict)

    def test_dbstorage_new(self):
        """ Test the new method of DBStorage """

        storage.all()

        # confirm that no data in the tables
        cur = self.test_engine.cursor()
        cur.execute("SELECT * FROM states;")
        objs = cur.fetchall()
        self.assertTrue(len(objs), 0)

        # create a new object
        new_obj = State(name="California")
        storage.new(new_obj)
        cur.execute("SELECT * FROM states;")
        objs = cur.fetchall()
        self.assertGreater(len(objs), 0)

    def test_dbstorage_delete(self):
        """ Test the delete method of DBStorage """

        storage.all()

        # create new object and update
        state = State(name="California")
        storage.new(state)
        storage.save()

        # confirm object added to the database
        cur = self.test_engine.cursor()
        cur.execute("SELECT * FROM states;")
        objs = cur.fetchall()
        self.assertTrue(len(objs), 1)

        # delete the object and confirm no objects
        storage.delete(state)
        cur.execute("SELECT * FROM states;")
        objs = cur.fetchall()
        self.assertTrue(len(objs), 0)

    def test_pep8_db_storage(self):
        """
        Pep8 compliance in db_storage.py
        """

        style = pep8.StyleGuide(quiet=False)
        errors = 0
        file = (["models/engine/db_storage.py"])
        errors += style.check_files(file).total_errors
        self.assertEqual(errors, 0, 'Need to fix Pep8')

    def test_pep8_test_db_storage(self):
        """
        Pep8 compliance in test_db_storage.py
        """

        style = pep8.StyleGuide(quiet=False)
        errors = 0
        file = (["tests/test_models/test_engine/test_db_storage.py"])
        errors += style.check_files(file).total_errors
        self.assertEqual(errors, 0, 'Need to fix Pep8')

    def test_documentation(self):
        """ Test module documentation """
        self.assertGreater(len(db_storage.__doc__), 3)
        self.assertGreater(len(DBStorage.__doc__), 3)
        self.assertGreater(len(DBStorage.close.__doc__), 3)
        self.assertGreater(len(DBStorage.all.__doc__), 3)
        self.assertGreater(len(DBStorage.delete.__doc__), 3)
        self.assertGreater(len(DBStorage.new.__doc__), 3)
        self.assertGreater(len(DBStorage.reload.__doc__), 3)
        self.assertGreater(len(DBStorage.save.__doc__), 3)
        self.assertGreater(len(DBStorage.__init__.__doc__), 3)
        self.assertGreater(len(self.__doc__), 3)
