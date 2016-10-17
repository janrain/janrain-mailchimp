from janrain_mailchimp_connect import create_app
from janrain_mailchimp_connect.config import get_config



if __name__ == '__main__':
    config = get_config()
    # must be named application for beanstalk to find it automatically
    application = create_app(config)
    application.run()
