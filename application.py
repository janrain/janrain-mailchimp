import logging
import concurrent.futures
from janrain_mailchimp_connect.models import JobModel
from janrain_mailchimp_connect import create_app
from janrain_mailchimp_connect.config import get_config



if __name__ == '__main__':
    config = get_config()
    logger = logging.getLogger(config['LOGGER_NAME'])
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    # must be named application for beanstalk to find it automatically
    application = create_app(config, JobModel, executor)
    application.run()
