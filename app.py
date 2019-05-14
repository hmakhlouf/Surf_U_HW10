import numpy as np
import pandas as pd
import datetime as dt

from matplotlib import style
import matplotlib.pyplot as plt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



##################
# Database Setup
##################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#########################
# Flask Setup
#########################
app = Flask(__name__)


####################
# Flask Routes
####################

#route 1

@app.route("/")
def Home():
    return(
        f"<h1>List of All Available Routes</h1><br/>"
        f"<h3>/api/precipitation</h3><br/>"
        f"<h3>/api/stations</h3><br/>"
        f"<h3>/api/temperature</h3><br/>"
        f"<h3>/api/<start><br/></h3><br/>"
        f"<h3>/api/<start>/<end></h3>"
    )


#route 2

@app.route("/api/precipitation")
def precipitation():
    last_1yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation_last12 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=last_1yr).all()
    
    # Create a dictionary from the row data and append to a list of all Measurements
    Measurements = []
    for date, prcp in precipitation_last12:
        Measurement_dict = {}
        Measurement_dict["date"] = date
        Measurement_dict["prcp"] = prcp
        Measurements.append(Measurement_dict)
    
    return jsonify(Measurements)


  

# route 3

@app.route("/api/stations")
def station():

    # Query all stations
    stations = session.query(Measurement.station).group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

# route 4

@app.route("/api/temperature")
def temperature():

    last_1yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_last12 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >=last_1yr).all()
    
    Temperatures = []
    for date, tobs in tobs_last12:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        Temperatures.append(temp_dict)
    
    return jsonify(Temperatures)







if __name__ == '__main__':
    app.run(debug=True)
