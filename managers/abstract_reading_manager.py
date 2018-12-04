from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class AbstractReadingManager:
    """ Abstract Reading Manager """

    FILENAME = "File Name"
    DATABASE_ID = "ID"
    SENSOR_TIMESTAMP = "Timestamp"
    SENSOR_MODEL = "Sensor Model"
    READING_MIN = "Min"
    READING_AVG = "Average"
    READING_MAX = "Max"
    READING_STATUS = "Status"

    def __init__(self, db_name):
        """ Initializes the reading manager """
        if db_name == "":
            raise ValueError
        elif db_name == None:
            raise ValueError
        else:
            self.engine = create_engine(db_name)
            self.DBSession = sessionmaker(bind=self.engine)

    def add_reading_to_database(self, timestamp, model, min_reading, avg_reading, max_reading, status):
        """ Add reading to database """
        raise NotImplementedError("Must be implemented")

    def update_reading_to_database(self, id, timestamp, model, min_reading, avg_reading, max_reading, status):
        """ Update reading from database """
        raise NotImplementedError("Must be implemented")

    def query_reading_from_database(self, id):
        """ Find one reading from database """
        raise NotImplementedError("Must be implemented")

    def query_readings_from_database(self):
        """ Find all readings from database """
        raise NotImplementedError("Must be implemented")

    def delete_reading_in_database(self, id):
        """ Delete reading in database """
        raise NotImplementedError("Must be implemented")

    @staticmethod
    def _validate_string_input(display_name, input_value):
        """ Private helper to validate input values as not None or an empty string """

        if input_value is None:
            raise ValueError(display_name + " cannot be undefined.")

        if input_value == "":
            raise ValueError(display_name + " cannot be empty.")

    @staticmethod
    def _validate_int(display_name, input_value):
        """ Private method to validate the input value is an integer type """

        if type(input_value) != int:
            raise ValueError(display_name, " must be an integer type")

    @staticmethod
    def _validate_float(display_name, input_value):
        """ Private method to validate the input value is a float type """

        if type(input_value) != float:
            raise ValueError(display_name, " must be a float type")
