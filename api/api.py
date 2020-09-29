import mysql.connector
import redis
from pykafka import KafkaClient
from pykafka.exceptions import KafkaException
from mysql.connector import Error
from flask import Flask, jsonify


app = Flask("Status_check_API")


def check_db():
    """ Function to request status of MySQL database.
        Gets response by connecting as a user to DB container.
    """
    try:

        connection = mysql.connector.connect(host='mysql',
                                             port='3306',
                                             user='root',
                                             password='password')
        if connection.is_connected():
            return True
    except Error:
        return False


def check_redis():
    """ Function to request status of Redis Server.
        Works by pinging the server through the redis python module.
    """
    try:
        r = redis.Redis(host='redis',
                        port=6379)

        if r.ping():
            return True
    except redis.ConnectionError:
        return False


def check_kafka():
    """ Function to request the status of Kafka Cluster.
    """
    try:
        client = KafkaClient("kafka:9092")

        if client:
            return True
    except KafkaException:
        return False


@app.route("/status", methods=['GET'])
def check_status():
    """ Basic API operation, checks statuses from services running
        on containers within the same network.
    """
    resp_db = check_db()
    resp_redis = check_redis()
    resp_kafka = check_kafka()
    # Response in JSON format
    status = {'Database': '%s' % resp_db,
              'Cache': '%s' % resp_redis,
              'Messaging': '%s' % resp_kafka}

    resp = jsonify(status)
    resp.status_code = 200

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
