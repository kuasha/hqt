# Trivia Game System
This is the core repository for the system.

The goal of this project is to develop a production grade system to develop a single click deployment on top of AWS infrastructure. We will try to use best practices for both development and cloud infrastructure. 

## System state

![Build and test badge](https://github.com/kuasha/hqt/actions/workflows/main.yml/badge.svg)

## Core Subsystems

* Game objects API
* Authentication and authorization
* Report API
* Static object delivery
* Notification susyem (eg. push notification to let user know game is starting)

## Design

System is designed using AWS services and checked into a github repository.

Github workflow is used to run linting and unit testing after each checkin and result (pass/fail) is shown on the README.md page on the repository.

The system is deployed using a single deploy.sh command to a AWS account (aws configure needs to be run first to configure credentials).

Once deployed API endpoint and cognito user pool will be ready. Users can signup and signin but authentication information is not being validated in the API yer. The simple authorizer will just check if an "Authorization" header is present for each request. The authorization header should be the cognito access token and system should check that for authentication and authorization.

API is designed to use http POST to create a new record and GET to read it.

On each create API request system validates the data and submits to the database.

We have a few object types:
* User
* Question
* Game (holds a set of questions)
* Episode (an instance of a game)
* Participant (user registration record of a specific episode)
* Response (to a question)
* Statistics (counts the submission for each question)

Objects are submitted to the API Gateway. API Gateway invokes a single 
lambda function that routes the call to specific handler for each resource/calls.

Resource are saved in their corrosponding dynamodb table. Some tables have streams associates with them. 

For example when a participant object is created (episode_id, user_id) the stream invokes a lambda function that updates the participant_count in the Episode object.

When a Response is posted to the API, the handler checks if the answer can be accepted at this time. After recording the response the stream invokes a lambda handler that checks if the answe is correct or not. For wrong answer it updates the participant object and mark it as eliminated. Eliminated count is updated on the episode object.

We use atomic increament operation for increasing counts and those are done one at a time but in parallel by any  number of lambda function is requered. To scale beyond 1000 requests per second we need to increase the lambda function concurrent execution limit for the account.

Statistics for each option selected for a question is updated after each answer submition.

A worker function that handles episode is run every one minute and it checks if there are enough participant in the episode and move it to running state. 

It will move from first question to last giestion with configurable time interval given to the participants. Answers (response) is accepted for 10 seconds (configurable) after the question is made available. 

After all questions are made available the system ends the episode. The worker will end the episode is there is only one participant left (not eliminated).

### Code quality

Code quality is non existant in the current implementation :D

The single responsibility principle is severely broken (most of SOLID actually). 
At the moment it just works but reorganization of code is required.
The field names of objects are coded as string all over the modules - needs to be in single object / module that exposes functions/classes to wrap the individual concepts.

The unit tests are now completely removed, fixing unit tests will fix some of the code issues.

### Resource names

We are not using hardcoded resource names to be able to deploy multiple instances of the system in same account. But it makes it harder in terms of operational experience. Since this is a small system small number of resources, it is OK. 

Before going to production the data table names and other names should be fixed so it is easier to understand the system. At the moment names are being supplied to the code using environment variables.

## Topics Covered

* Unit tests
* Integration tests
* Canary, Monitoring, Auto recovery and Alarms
* Load testing
* Code linting
* Code performance measurement 
* Logging
* Internationalization (languages, currencies, timezones etc.)
* Metrics collection - for system and user actions
* Alpha Beta Configuration
* API Version management
* CDN for static resource delivery (html/css/images etc.)
* Cache TTL management
* Throttling
* Network isolation and firewall (using AWS VPC and network rules)
* DDoS prevention
* Alpha/ Beta/ Gamma / Prod environment configuration
* Data security - encryption at rest and on flight traffic
* Development and Deployment pipeline, code checkin policy, deployment checks and manual approval process
* System health reporting
* Data backup and restore
* Data archive and retention policy management
* Role management for system access
* Audit trail for system access by users and sysadmins
* Key rotation and audit
* Multi region deployment
* User region/home location registry and data migration
* Security review and mitigation (for example OWASP Top 10 security risks)
