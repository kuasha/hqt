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

## API Examples

### Base URL

```
https://ovsel7v009.execute-api.us-east-1.amazonaws.com
```

#### Create a Game 

URL:

```
$BASE_URL/api/v1/game/
```
Method: ```POST```

Header:
```
Authorization: dummy
```

Body:

```
    {
        "qset": ["cd3049e4-1362-4340-b520-eab9a50ae003", "aab6384d-e392-4508-8a2f-21b1bdd5b551"],
        "id": "74cc6161-9380-4aef-9344-3b48ecc9a8d1"
    }
    
```

#### Create a Question 

URL:

```
$BASE_URL/api/v1/question/
```
Method: ```POST```

Header:
```
Authorization: dummy
```

Body:

```
    {
        "id": "aab6384d-e392-4508-8a2f-21b1bdd5b551",
        "question": "The Blackstreet lyric “I like the way you work it” is from what iconic song?",
        "options": [
            "No Diggity", "Yes Diggity", "Maybe a Lil Diggity"
        ],
        "answer": "0"
    }
```

We should create two more questions.

Question 2 body
```
    {
        "id": "8375a054-9817-4cac-9aa9-c09c0e78c202",
        "question": "The American episodic TV show that’s produced the most episodes is in what genre?",
        "options": ["Animated", "Game show", "Soap opera"],
        "answer": "2"
    }
```
Question 3 body
```
    {
        "id": "cd3049e4-1362-4340-b520-eab9a50ae003",
        "question": "What does Edward prepare for the Christmas party in “Edward Scissorhands”?",
        "options": ["Cronuts", "Ice sculpture", "Santa costume"],
        "answer": "1"
    },
    
```

#### Create an Episode 

URL:

```
$BASE_URL/api/v1/episode/
```
Method: ```POST```

Header:
```
Authorization: dummy
```

Body:

```
    {
        "id": "c62d941b-5de5-46b5-8d6c-3db7c679f96c",
        "game_id": "74cc6161-9380-4aef-9344-3b48ecc9a8d1",
        "min_participant": 2
    }
    
```

#### Register a participant

URL:

```
$BASE_URL/api/v1/participant/
```
Method: ```POST```

Header:
```
Authorization: dummy
```

Body:
```
    {
        "episode_id": "c62d941b-5de5-46b5-8d6c-3db7c679f96c",
        "user_id": "4e1f7af7-2ac6-45bb-834c-a4269fe6d4fd"
    }
```
The user_id will be validated against authorization token - which has not been implemented yet. And since we need at least two users (see the body of episode above) we create another registration with following body:

```
    {
        "episode_id": "c62d941b-5de5-46b5-8d6c-3db7c679f96c",
        "user_id": "7714a925-40f2-4125-8670-d40391ceb501"
    }
```

After two participants are registered the episode will move to ```STARTED``` state and submission of the answer to first question can be submitted in about a minute. The start time is set to about a minute in future so we can send notification to all users within that time.

#### Response to a question


URL:

```
$BASE_URL/api/v1/response/
```
Method: ```POST```

Header:
```
Authorization: dummy
```

Body:
```
  {
        "episode_id": "c62d941b-5de5-46b5-8d6c-3db7c679f96c",
        "question_id":  "cd3049e4-1362-4340-b520-eab9a50ae003",
        "user_id": "4e1f7af7-2ac6-45bb-834c-a4269fe6d4fd",
        "answer":"1"
  }
```

We can sumbit a wrong answer here and the workflow will eliminate the user and then END the episode as there will be only one user left.

The worker will continue to watch the episode, move to next question and ultimately end the episode. 

#### Get episode data


URL:

```
$BASE_URL/api/v1/episode/
```
Method: ```GET```

Header:
```
Authorization: dummy
```

Response:
```
{
    "participant_count": 0,
    "qset": [
        "cd3049e4-1362-4340-b520-eab9a50ae003",
        "aab6384d-e392-4508-8a2f-21b1bdd5b551"
    ],
    "question_start_timestamp": 0,
    "eliminated_count": 0,
    "min_participant": 2,
    "id": "c62d941b-5de5-46b5-8d6c-3db7c679f96c",
    "current_question_index": -1,
    "state": "",
    "game_id": "74cc6161-9380-4aef-9344-3b48ecc9a8d1"
}
```

## Production Readiness Considerations

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
