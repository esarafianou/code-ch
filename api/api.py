import mysql.connector
import redis
from mysql.connector import Error
from flask import Flask, jsonify


app = Flask(__name__)


def check_db():
    try:
        connection = mysql.connector.connect(host='localhost',
                                         port='3306',
                                         user='admin',
                                         password='passwd')
        if connection.is_connected():
            return True
    except Error as e:
        return False


def check_redis():
    try:
        r = redis.Redis(host='localhost',
                        port=6379)

        if r.ping():
            return True
    except redis.ConnectionError:
        return False


@app.route("/status", methods = ['GET', 'POST'])
def check_status():
    resp_db = check_db()
    resp_redis = check_redis()
    status = {'Database':'%s' % resp_db, 'Cache':'%s' % resp_redis, 'Messaging':'bool'}

    return jsonify(status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
