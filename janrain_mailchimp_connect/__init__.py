"""Flask application setup."""
import flask
import logging
import logging.handlers
from janrain_mailchimp_connect._version import __version__
from janrain_mailchimp_connect.actions.sync import sync

def create_app(config, JobModel, executor):
    app = flask.Flask(__name__)
    app.config.update(config)

    # routes
    app.add_url_rule('/', 'root', lambda: 'ok')
    app.add_url_rule('/sync', 'sync', sync, methods=['POST'])

    @app.after_request
    def add_headers(response):
        """additional headers for each response"""
        response.headers['X-App-Version'] = __version__
        return response

    app.executor = executor
    app.JobModel = JobModel

    # this is just for convenience during development
    if app.config['DEBUG'] and not app.JobModel.exists():
        # create table with minimal capacity
        app.JobModel.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
        )

    return app

def logging_init(app):
  # setup logging
  handler = logging.handlers.RotatingFileHandler(
      app.config['APP_LOG_FILE'],
      backupCount=app.config['APP_LOG_NUM_BACKUPS'],
      maxBytes=app.config['APP_LOG_FILESIZE'])

  if app.debug:
      handler.setLevel(logging.DEBUG)
  else:
      handler.setLevel(logging.INFO)

  msg_format = '[%(asctime)s] %(levelname)s: %(message)s'
  timestamp_format = '%Y-%m-%d %H:%M:%S %z'
  formatter = logging.Formatter(msg_format, timestamp_format)
  handler.setFormatter(formatter)
  logger = logging.getLogger(app.config['LOGGER_NAME'])
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)

  return logger
