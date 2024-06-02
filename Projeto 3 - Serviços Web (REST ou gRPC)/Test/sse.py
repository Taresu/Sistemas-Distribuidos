from flask_sse import sse


def notify(event, data):
    sse.publish(data, type=event)