from readings.base import Base
from datetime import datetime


class AbstractReading(Base):
    """ Abstract Sensor Reading """
    __abstract__ = True

    SENSOR_TIMESTAMP = "Timestamp"
    SENSOR_MODEL = "Sensor Model"
    READING_SEQ_NUM = "Sequence Number"
    READING_MIN = "Min"
    READING_AVG = "Average"
    READING_MAX = "Max"
    READING_STATUS = "Status"

    def __init__(self, timestamp, model, min_reading, avg_reading, max_reading, status):
        """ Initializes the sensor reading """

        if timestamp is not None:
            self.timestamp = timestamp
        else:
            raise ValueError("Date must be defined")

        AbstractReading._validate_string_input(AbstractReading.SENSOR_MODEL, model)
        self.model = model
        AbstractReading._validate_float(AbstractReading.READING_MIN, min_reading)
        self.min_reading = min_reading
        AbstractReading._validate_float(AbstractReading.READING_AVG, avg_reading)
        self.avg_reading = avg_reading
        AbstractReading._validate_float(AbstractReading.READING_AVG, max_reading)
        self.max_reading = max_reading
        AbstractReading._validate_string_input(AbstractReading.READING_STATUS, status)
        self.status = status

    def get_timestamp(self, date):
        raise NotImplementedError("Must be implemented")

    def to_dict(self):
        dict = {
            "id": self.id,
            "timestamp": self.get_timestamp(self.timestamp),
            "model": self.model,
            "min_reading": self.min_reading,
            "avg_reading": self.avg_reading,
            "max_reading": self.max_reading,
            "status": self.status
        }
        return dict

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
