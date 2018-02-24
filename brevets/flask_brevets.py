"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = MongoClient(CONFIG.MONGO_URI)
db = client.get_default_database()
brevet_times_col = db['brevet_times']

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet = request.args.get('brevet', type=int)
    start_info = request.args.get('start_info', type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, brevet, start_info)
    close_time = acp_times.close_time(km, brevet, start_info)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_submit_times_db")
def _submit_times_db():
    brevet_times_col.delete_many({})

    miles = request.args.get("miles", type=str).split("|")
    km = request.args.get("km", type=str).split("|")
    openTime = request.args.get("open", type=str).split("|")
    closeTime = request.args.get("close", type=str).split("|")

    num_controls = len(miles)

    print(miles)
    print(km)
    print(openTime)
    print(closeTime)

    for control in range(num_controls - 1):
        brevet_times_col.insert({
                                "miles": miles[control],
                                "km": km[control],
                                "openTime": openTime[control],
                                "closeTime": closeTime[control]
                                })
    return ""

@app.route("/_display_times_db")
def _display_times_db():
    controls = brevet_times_col.find({})
    print("Controls")
    print(controls)
    parsedControls = ""
    controlNum = 1
    for entries in controls:
        # if len(entries['km']) > 0:
        parsedControls += "<br/>[Control {}<br/> miles: {}<br/>km: {}<br/>openTime: {}<br/>closeTime: {}<br/>]<br/>".format(controlNum, entries['miles'], entries['km'], entries['openTime'], entries['closeTime'])
        controlNum += 1
    return flask.jsonify(result=parsedControls)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
