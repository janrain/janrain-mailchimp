"""Flask application setup."""
import flask
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
