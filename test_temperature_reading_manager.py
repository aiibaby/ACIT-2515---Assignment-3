from managers.temperature_reading_manager import TemperatureReadingManager
from readings.temperature_reading import TemperatureReading
from unittest import TestCase
import datetime
import inspect
import os
import sqlite3


class TestTemperatureReadingManager(TestCase):
    """ Unit Tests for the TemperatureReadingManager Class """

    def logPoint(self):
        """ Display test specific information """

        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print('in %s - %s()' % (currentTest, callingFunction))

    def setUp(self):
        """ Creates database tables before each test """
        conn = sqlite3.connect('test_readings.sqlite')

        c = conn.cursor()
        c.execute('''
                          CREATE TABLE temperature_reading
                          (id INTEGER PRIMARY KEY ASC,
                           timestamp DATETIME NOT NULL,
                           model VARCHAR(250) NOT NULL,
                           min_reading NUMBER NOT NULL,
                           avg_reading NUMBER NOT NULL,
                           max_reading NUMBER NOT NULL,
                           status VARCHAR(250) NOT NULL
                          )
                          ''')
        c.execute('''
                          CREATE TABLE pressure_reading
                          (id INTEGER PRIMARY KEY ASC,
                           timestamp DATETIME NOT NULL,
                           model VARCHAR(250) NOT NULL,
                           min_reading NUMBER NOT NULL,
                           avg_reading NUMBER NOT NULL,
                           max_reading NUMBER NOT NULL,
                           status VARCHAR(250) NOT NULL
                          )
                          ''')

        conn.commit()
        conn.close()
        self.logPoint()

    def tearDown(self):
        """ Remove sqlite files after each test method is run """

        os.remove("test_readings.sqlite")

        self.logPoint()

    def test_constructor_success(self):
        """ 010A - Creates a TemperatureReadingManager instance """
        self.reading_manager = TemperatureReadingManager("sqlite:///test_readings.sqlite")
        self.assertIsInstance(self.reading_manager, TemperatureReadingManager,
                              "Must be an instance of PressureReadingManager")

    def test_constructor_fail(self):
        """ 010B - Raises ValueError when database name is empty or None """

        with self.assertRaises(ValueError):
            self.engine = TemperatureReadingManager("")
            self.engine = TemperatureReadingManager(None)

    def test_add_reading_to_database_success(self):
        """ 020A - Adds a TemperatureReading to database """
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.result = self.reading_manager.query_reading_from_database(1)
        self.assertNotEqual(self.result, None, "Cannot be None")

    def test_add_reading_to_database_fail(self):
        """ 020B - Return None if fail to add a TemperatureReading to database with empty input"""
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "")
        self.reading_manager.add_reading_to_database("", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     "", 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, "", 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, "", "GOOD")
        self.result = self.reading_manager.query_reading_from_database(1)
        self.assertEqual(self.result, None, "Must be None")

    def test_update_reading_list_success(self):
        """ 030A - Updates TemperatureReading in a list of readings """
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.update_reading_to_database(1, "2018-10-01 01:01:01.011", "Test Sensor",
                                                        25.1, 22.1, 25.1, "GOOD")
        self.result = self.reading_manager.query_reading_from_database(1)
        self.assertEqual(self.result.max_reading, 25.1, "Must be 25.1.")

    def test_update_reading_list_fail(self):
        """ 030B - Fail to update TemperatureReading to database with a empty input """
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.update_reading_to_database(1, "2018-10-01 01:01:01.011", "Test Sensor",
                                                        25.1, 22.1, "", "GOOD")
        self.result = self.reading_manager.query_reading_from_database(1)
        self.assertEqual(self.result.max_reading, 24.1, "Must be 24.1.")

    def test_query_reading_from_database_success(self):
        """ 040A - Finds a TemperatureReading in database """
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.result = self.reading_manager.query_reading_from_database(1)
        self.assertEqual(self.result.timestamp, datetime.datetime(2018, 10, 1, 1, 1, 1, 11000), "Must be same.")
        self.assertEqual(self.result.model, "Test Sensor", "Must be same.")
        self.assertEqual(self.result.min_reading, 25.1, "Must be same.")
        self.assertEqual(self.result.avg_reading, 22.1, "Must be same.")
        self.assertEqual(self.result.max_reading, 24.1, "Must be same.")
        self.assertEqual(self.result.status, "GOOD", "Must be same.")

    def test_query_reading_from_database_fail(self):
        """ 040B - Return None if fail to find a TemperatureReading in database """
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.result = self.reading_manager.query_reading_from_database(3)
        self.assertEqual(self.result, None, "Must be None.")

    def test_query_readings_from_database_success(self):
        """ 050A - Find all Temperature in database"""
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-02 02:02:01.011", "Test Sensor",
                                                     25.1, 24.1, 26.1, "BAD")
        self.result = self.reading_manager.query_readings_from_database()
        self.assertEqual(len(self.result), 2, "Must be 2.")

    def test_query_readings_from_database_fail(self):
        """ 050B - Fail to find all TemperatureReadings in database and return an empty list """
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.result = self.reading_manager.query_readings_from_database()
        self.assertEqual(len(self.result), 0, "Must be empty list.")

    def delete_reading_in_database_success(self):
        """ 060A - Delete all TemperatureReadings in database"""
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-02 02:02:01.011", "Test Sensor",
                                                     25.1, 24.1, 26.1, "BAD")
        self.reading_manager.delete_reading_in_database(1)
        self.reading_manager.delete_reading_in_database(2)
        self.result = self.reading_manager.query_readings_from_database()
        self.assertEqual(len(self.result), 0, "Must be empty list.")

    def delete_reading_in_database_fail(self):
        """ 060B - Fail to delete TemperatureReading in database with invalid id"""
        self.reading_manager = TemperatureReadingManager('sqlite:///test_readings.sqlite')
        self.reading_manager.add_reading_to_database("2018-10-01 01:01:01.011", "Test Sensor",
                                                     25.1, 22.1, 24.1, "GOOD")
        self.reading_manager.add_reading_to_database("2018-10-02 02:02:01.011", "Test Sensor",
                                                     25.1, 24.1, 26.1, "BAD")
        self.result = self.reading_manager.delete_reading_in_database(4)
        self.assertEqual(self.result, None, "Must be None")
