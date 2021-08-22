#!/bin/bash

flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
