import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return("Learn About Hawaii Precipitation<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/enter a start date here<start><br/>"
        f"/api/v1.0/enter a start date here <start>/enter an end date here<end><br/>")

@app.route("/api/v1.0/precipitation")

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    all_data = []
    for x in results:
        data_dict = {}
        data_dict["date"] = x.date
        data_dict["precipitation"] = x.prcp
        all_data.append(data_dict)
    
    return jsonify(all_data)


@app.route("/api/v1.0/stations")
def stations():
#Return a JSON list of stations from the dataset. --> do these need to unique stations or all listed
    results = session.query(Measurement.station).all()
    all_names = list(np.ravel(results))
    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    temp_obvs = session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-24').all()
    all_names = list(np.ravel(temp_obvs))
    return jsonify(all_names)

@app.route("/api/v1.0/<start>")
def start_date(start):

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start)
    
    all_dates = []
    dates_dict = {}
    dates_dict["TMIN"] = results[0][0]
    dates_dict["TAVG"] = results[0][1]
    dates_dict["TMAX"] = results[0][2]
    all_dates.append(dates_dict)

    return jsonify(all_dates)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end)
    
    all_dates = []
    dates_dict = {}
    dates_dict["TMIN"] = results[0][0]
    dates_dict["TAVG"] = results[0][1]
    dates_dict["TMAX"] = results[0][2]
    all_dates.append(dates_dict)

    return jsonify(all_dates)

if __name__ == '__main__':
    app.run(debug=True)
