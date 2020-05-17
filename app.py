import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Getting precipitation data")
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close
    return jsonify(results1)
    
@app.route("/api/v1.0/stations")
def stations():
    print("Getting station Data")
    session = Session(engine)
    results = session.query(Station.id, Station.name).all()
    session.close
    return jsonify(results2)
    
@app.route("/api/v1.0/tobs")
def tobs():
    print("Getting temperatures")
    session = Session(engine)
    results_new = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station== 'USC00519281').all()
    session.close

    return jsonify(results_new)

@app.route("/api/v1.0/<start>")
def start_date(start):
    print("Getting Data for date provided")
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close
    return jsonify(results[0])
@app.route("/api/v1.0/<start>/<end>")
def date_period(start,end):
    print("Getting Data for dates provided")
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close
    return jsonify(results[0])
    
if __name__== '__main__':
    app.run(debug=True)