"""Flask application setup."""
import flask
from janrain_mailchimp_connect._version import __version__
# from janrain_mailchimp_connect.actions import sync

def create_app():
    app = flask.Flask(__name__)
    # app.config.update(config)

    # routes
    app.add_url_rule('/', 'root', lambda: 'ok')
    # app.add_url_rule('/sync', 'sync', sync, methods=['POST'])

    @app.after_request
    def add_headers(response):
        """additional headers for each response"""
        response.headers['X-App-Version'] = __version__
        return response

    # # add the job executor to the app
    # app.jobsexecutor = jobsexecutor
    #
    # # set the jobs model class
    # app.jobsmodelclass = jobsmodelclass

    return app
