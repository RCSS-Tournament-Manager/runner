# runner
The program that runs the games using docker and store the logs and events in S3 and RabbitMQ.


## Development

1. Clone the repository
2. Create a virtual environment
    ```bash
    python3 -m pipenv install
    python3 -m pipenv shell
    ```
3. Copy the `.env.example` file to `.env` and update the values
4. Run the docker-compose file
    ```bash
    docker-compose up -d
    ```
5. Run the program
    ```bash
    pipenv run python runner.py
    ```


## Testing

* To access the RabbitMQ Manager in the test environment, use the following link:
    [http://localhost:15672/](http://localhost:15672/)
    the username and password are in the `.env` file.
    demo username: `test`
    demo password: `test`

* To access the Minio in the test environment, use the following link:
    [http://localhost:9000/](http://localhost:9000/)
    the access key and secret key are in the `.env` file.
    demo access key: `minioadmin`
    demo secret key: `minioadmin`


* test commands example
    ```bash
    pipenv run python ./test.py name_test
    ```




# TODO

### RUN Match
- [ ] check the validation of the message
- [ ] loop trough all the keys in the message and add "client" field to external connections
- [ ] if the external connection is not available, create the connection class and put it on client field
- [ ] run the match
- [ ] create tasks for streams





# listen to the rabbitmq queue
# on message received, log the message
# if the message is shutdown, exit the loop
# if the message is to stop the match, stop the match
# if the message is to start a new match, start a new match
# to start a new match, first check the massage format is correct
# if the message format is incorrect, let the rabbitmq know that the message format is incorrect
# if the match is already running, let the rabbitmq know that the match is already running
# if the message format is correct, retrieve the team details
# if the team details are correct, get the teams images from docker hub
# if the images are not available, download the images from docker registry
# if the images are available, start the match with the given configuration
# let the rabbitmq know that the match has started
# if the match is stopped, let the rabbitmq know that the match has stopped
# if the match ends, let the rabbitmq know that the match has ended
# check the massage for the log and event storage configuration
# upload the log and event of the match to S3
# let the rabbitmq know that the match has been uploaded to S3



