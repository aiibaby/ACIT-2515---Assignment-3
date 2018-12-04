from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from readings.abstract_reading import AbstractReading


class PressureReading(AbstractReading):
    """ Concrete Implementation of a Pressure Reading """

    __tablename__ = "pressure_reading"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    model = Column(String(250), nullable=False)
    min_reading = Column(Integer, nullable=False)
    avg_reading = Column(Integer, nullable=False)
    max_reading = Column(Integer, nullable=False)
    status = Column(String(250), nullable=False)

    def get_timestamp(self, date):
        reading_display_datetime = datetime.strftime(date, '%Y-%m-%d %H:%M')
        return reading_display_datetime
