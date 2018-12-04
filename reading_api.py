from flask import Flask
from flask import request
from flask import Response
import json
from managers.temperature_reading_manager import TemperatureReadingManager
from managers.pressure_reading_manager import PressureReadingManager

app = Flask(__name__)

DB_NAME = 'sqlite:///readings.sqlite'


@app.route("/sensor/<string:sensor_type>/reading", methods=["POST"])
def add_reading(sensor_type):
    """ Add a sensor reading to database """
    try:
        database = create_reading_manager(sensor_type)
        user_input = request.get_json()
        result = database.add_reading_to_database(user_input["timestamp"], user_input["model"],
                                                  user_input["min_reading"],
                                                  user_input["avg_reading"], user_input["max_reading"],
                                                  user_input["status"])
        if result:
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=400)


@app.route("/sensor/<string:sensor_type>/reading/<int:id>", methods=["PUT"])
def update_reading(sensor_type, id):
    """ Updates a reading based on ID """
    try:
        database = create_reading_manager(sensor_type)
        user_input = request.get_json()
        result = database.update_reading_to_database(id, user_input["timestamp"], user_input["model"],
                                                     user_input["min_reading"],
                                                     user_input["avg_reading"], user_input["max_reading"],
                                                     user_input["status"])

        if result:
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=400)


@app.route("/sensor/<string:sensor_type>/reading/<int:id>", methods=["DELETE"])
def delete_reading(sensor_type, id):
    """ Delete a reading from database based on ID """
    try:
        database = create_reading_manager(sensor_type)
        result = database.delete_reading_in_database(id)

        if result:
            return Response(status=200)
        else:
            return Response(status=404)
    except:
        return Response(status=400)


@app.route("/sensor/<string:sensor_type>/reading/<int:id>", methods=["GET"])
def get_reading(sensor_type, id):
    """ Get a reading from database based on ID """

    try:
        database = create_reading_manager(sensor_type)
        find_reading = database.query_reading_from_database(id)
        reading_in_json = json.dumps(find_reading.to_dict(), indent=4)
        if find_reading:
            return Response(response=reading_in_json, status=200, mimetype="application/json")
        else:
            return Response(response=None, status=404, mimetype="application/json")

    except:
        return Response(response=None, status=400, mimetype="application/json")


@app.route("/sensor/<string:sensor_type>/reading/all", methods=["GET"])
def get_all_readings(sensor_type):
    """ Get all reading from database based on ID """

    try:
        database = create_reading_manager(sensor_type)
        readings = database.query_readings_from_database()

        readings = [item.to_dict() for item in readings]
        readings_in_json = json.dumps(readings, indent=4)
        if readings_in_json:
            return Response(response=readings_in_json, status=200, mimetype="application/json")
        else:
            return Response(response=None, status=404, mimetype="application/json")

    except:
        return Response(response=None, status=400, mimetype="application/json")


def create_reading_manager(sensor_type):
    """ Returns reading manager if valid input, None otherwise """

    if sensor_type == "temperature":
        reading_manager = TemperatureReadingManager(DB_NAME)
    elif sensor_type == "pressure":
        reading_manager = PressureReadingManager(DB_NAME)
    else:
        reading_manager = None

    return reading_manager


if __name__ == "__main__":
    app.run()
