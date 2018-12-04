from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from readings.abstract_reading import AbstractReading
from datetime import datetime


class TemperatureReading(AbstractReading):
    """ Concrete Implementation of a Temperature Reading """

    __tablename__ = "temperature_reading"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    model = Column(String(250), nullable=False)
    min_reading = Column(Integer, nullable=False)
    avg_reading = Column(Integer, nullable=False)
    max_reading = Column(Integer, nullable=False)
    status = Column(String(250), nullable=False)

    HIGH_TEMP_ERROR = "HIGH_TEMP"
    LOW_TEMP_ERROR = "LOW_TEMP"
    STATUS_OK = "OK"
    DEGREE_SIGN = u'\N{DEGREE SIGN}'

    def get_timestamp(self, date):
        reading_display_datetime = datetime.strftime(date, '%Y-%m-%d %H:%M:%S.%f')
        return reading_display_datetime
