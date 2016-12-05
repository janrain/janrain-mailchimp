import concurrent.futures
from janrain_mailchimp_connect.models import JobModel
from janrain_mailchimp_connect import create_app, logging_init
from janrain_mailchimp_connect.config import get_config

config = get_config()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
# must be named application for beanstalk to find it automatically
application = create_app(config, JobModel, executor)
logger = logging_init(application)

# XXX This is hacky. Get the config again after we have a logger to log the errors if any
get_config(logger)

if __name__ == '__main__':
    application.run()
