# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    '''List of all api routes. '''
    return (
        f'Welcome to My Assignment 10-Advanced-Data-Storage-and-Retrieval Results <br/><br/>'
        f'Here are a list of results from my calculations via routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
    )

        
@app.route("/api/v1.0/precipitation")
def precipitation():
    '''PRECIPITATION LIST'''
    last12months = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date.between('2016-09-01','2017-08-31')).order_by(Measurement.date.asc()).all()
    
    all_precip = []
    for date, prcp in last12months:
        precip_dict = {}
        precip_dict['Date'] = date
        precip_dict['Precip'] = prcp
        all_precip.append(precip_dict)
        
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    activeStations = session.query(Measurement.station).order_by(Measurement.station.desc()).all()
    
    all_stations = []
    for station in activeStations:
        station_dict = {}
        station_dict['Station'] = station
        all_stations.append(station_dict)
        
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last12monthsTemp = session.query(Measurement.station).filter(Measurement.date.between('2016-09-01','2017-08-31')).order_by(Measurement.date.desc()).all()

    prevYrTemp = []
    for date, tobs in last12monthsTemp:
        temp_dict = {}
        precip_dict['Date'] = date
        temp_dict['Temp'] = tobs
        prevYrTemp.append(temp_dict)
        
    return jsonify(prevYrTemp)
    
@app.route("/api/v1.0/<start>")
def start(start):
    peaksTemp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    startFrom = start.replace(" ", "")
    for dateinput in peaksTemp:
        search_date = dateinput["startdate"].replace(" ", "")

        if search_date == startFrom:
            return jsonify(peaksTemp)
    return jsonify({"error": "Character not found."}), 404

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    peaksTemp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measure.date <= end).all()

    startFrom = start.replace(" ", "")
    for dateinput in peaksTemp:
        search_date = dateinput["startdate"].replace(" ", "")

        if search_date == startFrom:
            return jsonify(peaksTemp)
    return jsonify({"error": "Character not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
