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

TODO: Degin high level diagram and detailed design link

## Topics Covered

* Unit tests
* Integration tests
* Canary, Monitoring, Auto recovery and Alarms
* Load testing
* Code linting
* Code performance measurement 
* Logging
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
