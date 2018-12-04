from managers.abstract_reading_manager import AbstractReadingManager
from readings.pressure_reading import PressureReading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import csv


class PressureReadingManager(AbstractReadingManager):
    """ Pressure Reading Manager """

    def add_reading_to_database(self, timestamp, model, min_reading, avg_reading, max_reading, status):
        """ Add reading to database """
        try:
            session = self.DBSession()
            reading_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
            new_reading = PressureReading(reading_datetime, str(model), float(min_reading), float(avg_reading),
                                          float(max_reading), str(status))
            session.add(new_reading)
            session.commit()
            session.close()
            return True
        except:
            return False

    def update_reading_to_database(self, id, timestamp, model, min_reading, avg_reading, max_reading, status):
        """ Update reading from database """
        try:
            PressureReadingManager._validate_int(PressureReadingManager.DATABASE_ID, int(id))
            PressureReadingManager._validate_string_input(PressureReadingManager.SENSOR_MODEL, str(model))
            PressureReadingManager._validate_float(PressureReadingManager.READING_MIN, float(min_reading))
            PressureReadingManager._validate_float(PressureReadingManager.READING_AVG, float(avg_reading))
            PressureReadingManager._validate_float(PressureReadingManager.READING_MAX, float(max_reading))
            PressureReadingManager._validate_string_input(PressureReadingManager.READING_STATUS, str(status))
            session = self.DBSession()
            updating_reading = session.query(PressureReading).filter(PressureReading.id == id).first()
            if updating_reading is not None:
                updating_reading.timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
                updating_reading.model = model
                updating_reading.min_reading = float(min_reading)
                updating_reading.avg_reading = float(avg_reading)
                updating_reading.max_reading = float(max_reading)
                updating_reading.status = status
                session.commit()
                session.close()
                return True
            else:
                return None
        except:
            return False

    def query_reading_from_database(self, id):
        """ Find one reading from database """
        try:
            PressureReadingManager._validate_int(PressureReadingManager.DATABASE_ID, int(id))
            session = self.DBSession()
            # PressureReading._validate_int(PressureReading.DATABASE, id)
            query_reading = session.query(PressureReading).filter(PressureReading.id == id).first()
            session.close()
            return query_reading
        except:
            return False

    def query_readings_from_database(self):
        """ Find all readings from database """
        try:
            session = self.DBSession()
            query_readings = session.query(PressureReading).all()
            session.close()
            return query_readings
        except:
            return False

    def delete_reading_in_database(self, id):
        """ Delete reading in database """
        try:
            PressureReadingManager._validate_int(PressureReadingManager.DATABASE_ID, int(id))
            session = self.DBSession()
            delete_reading = session.query(PressureReading).filter(PressureReading.id == id).first()
            session.delete(delete_reading)
            session.commit()
            session.close()
            return True
        except:
            return False
