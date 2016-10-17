from janrain_mailchimp_connect import create_app

# must be named application for beanstalk to find it automatically
application = create_app()

if __name__ == '__main__':
    application.run()
