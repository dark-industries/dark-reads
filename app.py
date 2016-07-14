import config
from flask import Flask
from routes import routes


app = Flask(__name__)
app.register_blueprint(routes)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(config.LOGFILE, maxBytes=10000, backupCount=1)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)