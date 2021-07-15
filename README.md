# Jenkins remote script console

## Overview

You have one or more jenkins instance(s)?

You have an admin token?

You don't want to have to go to the UI to run a script anymore?

This is for you.

## Usage

* (Optional) Create a python venv (python3 -m venv .venv) and activate it (source .venv/bin/activate).
* Install dependencies (pip install -r requirements.txt)
* Create .env files containing values for JENKINS_INSTANCE, JENKINS_USER, JENKINS_TOKEN and JENKINS_SSL_VERIFY variables (see .env.example file)
* Run the script providing the .env file path (or a list of .env files separated by commas) and a groovy script path as arguments

## Tips and tricks

* Have your groovy scripts print structured data on the standard output (and nothing else) so that you can use this tool in other, larger scripts/tools
