# janrain-mailchimp

## Configuration

### Primary

- `FIELD_MAPPING`: A JSON string which maps janrain attribute to MailChimp List Fields.

#### AWS

- `AWS_ACCESS_KEY_ID`: AWS Access Key ID

- `AWS_SECRET_ACCESS_KEY`: AWS Secret Access Key

#### Janrain

- `JANRAIN_URI`: Hostname to use when making API calls to Capture.

- `JANRAIN_CLIENT_ID`: Janrain client Id.

- `JANRAIN_CLIENT_SECRET`: Secret for the client.

- `JANRAIN_SCHEMA_NAME`: Name of the Capture schema containing the user records.
(default: `user`)

#### MailChimp

- `MC_API_KEY`: MailChimp API Key

- `MC_LIST_ID`: The id of the list. This is not the name.

### Secondary

- `DEBUG`: If this is set to anything other than empty string or the word
`FALSE`, then the app will run in debug mode. Additional info will be written
to the log.

- `LOGGER_NAME`: Name of the logger.

#### APP

- `APP_LOG_FILE`: Full path to the file where the app will write the log.
(should only be used during local development, leave blank when deployed
to elastic beanstalk)

- `APP_LOG_FILESIZE`: Maximum size in bytes of the app log before it gets
rotated. (default: `10000000`)

- `APP_LOG_NUM_BACKUPS`: Number of rotated backups of the app log that will
be kept. (default: `20`)

#### AWS

- `AWS_DEFAULT_REGION`: AWS region the app runs in.

- `AWS_DYNAMODB_URL`: Url of the DynamoDB service to use.
(should only be used during local development, leave blank when deployed
to elastic beanstalk. [Requires having .aws/credentials file for local 
DynamoDB development](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html))

- `AWS_DYNAMODB_TABLE`: Name of the table in DynamoDB to use. (default: `janrain-mailchimp`)

#### Janrain

- `JANRAIN_BATCH_SIZE`: The size of batch for each Janrain Capture Call.

- `JANRAIN_MAX_LASTUPDATED`: Number of Days the lastUpdated cannot exceed. (default: `1`)

- `JANRAIN_FULL_EXPORT`: If `True` ignore `JANRAIN_MAX_LASTUPDATED` and export everything. (default: `False`)

- `JANRAIN_OPT_IN_ATTRIBUTE`: The Attribute to use to opt-in each user. (default: `list_optIn_status`)

#### MailChimp

- `MC_URI_TEMPLATE`: Template used to create MailChimp API URI.

- `MC_TIME_BETWEEN_BATCHES`: The time in seconds to wait before checking if the MailChimp batch is complete. (default `5`)
    
- `MC_MAX_RECORDS_IN_BATCH`: The max number of records allowed in MailChimp the batch. (default `20000`)
    
- `MC_MAX_BYTES_IN_BATCH`: The max number of bytes allowed in the MailChimp batch. (default `4000000`)

## Development

### Running Locally

1. Edit `bin/environment` to include your values
1. Start application `./bin/run`

### Testing

1. Run test suite `./bin/test`
