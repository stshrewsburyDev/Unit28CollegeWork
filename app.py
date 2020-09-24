import flask, sqlite3, os, json
from datetime import datetime

startup_time = datetime.now()
app = flask.Flask(__name__)

import error_handlers, database_mgr
from cogs import stats, formatting

database = database_mgr.DatabaseManager()
stats.start(startup_time)


@app.route("/")
def main():
    products = database.get_all_records()
    return flask.render_template("home.html", products=products[:5])


@app.route("/browse/")
def browse():
    return flask.render_template("browse.html", products=database.search(flask.request.args))


@app.route("/about/")
def about():
    return flask.render_template("about.html")


@app.route("/product/<product_id>")
def product_page(product_id):
    i = database.get_record(product_id)
    if i:
        return flask.render_template("product.html", info=i, price_fmt="£%.2f" % i[4], pap_fmt="£%.2f" % i[5])
    else:
        return flask.render_template("errors/404.html")


@app.route("/stats/")
def stats_info():
    i = stats.Stats.stats
    return flask.render_template("stats.html", info=i, uptime=formatting.seconds_to_timestamp((datetime.now() - i["STARTED"]).total_seconds()))
