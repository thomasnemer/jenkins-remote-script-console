# Jenkins remote script console

## Overview

You have one or more jenkins instance(s)?

You have an admin token?

You don't want to have to go to the UI to run a script anymore?

This is for you.

## Usage

* (Optional) Create a python venv (`python3 -m venv .venv`) and activate it (`source .venv/bin/activate`)
* Install dependencies (`pip install -r requirements.txt`)
* Create .env files containing values for `JENKINS_INSTANCE`, `JENKINS_USER`, `JENKINS_TOKEN` and `JENKINS_SSL_VERIFY` variables (see [.env.example](.env.example))
* Run the script providing the .env file path (or a list of .env files separated by commas) and a groovy script path as arguments (ie : `./jenkins-remote-script-console.py .env.example example.groovy`)
* (Optional) Have your groovy scripts print json on stdout, and nothing else (see [example.groovy](example.groovy) file), it will be parsed and accessible in the `response.text` field of the output, so that you can process it.

## Parsing the output

This tool will output errors on stderr and json on stdout, meaning you can parse stdout, for example with jq.

### Examples

```shell
$  ./jenkins-remote-script-console.py
usage: jenkins-remote-script-console.py [-h] env_files script
jenkins-remote-script-console.py: error: the following arguments are required: env_files, script
```

```shell
$ ./jenkins-remote-script-console.py -h
usage: jenkins-remote-script-console.py [-h] env_files script

positional arguments:
  env_files   List of path to an env files separated by commas (,)
  script      Path to a script file to be executed on a jenkins instance

optional arguments:
  -h, --help  show this help message and exit
```

```shell
$ ./jenkins-remote-script-console.py .env.dev example.groovy
[
  {
    "instance": "https://jenkins-dev.domain.tld/jenkins",
    "params": {
      "env_file": ".env.dev",
      "user": "admin",
      "ssl_verify": false
    },
    "response": {
      "status_code": 200,
      "text": {
        "jenkins_version": "2.289.1"
      }
    }
  }
]
```

```shell
$ ./jenkins-remote-script-console.py .env.indus example.groovy | jq '.[0].response.text.jenkins_version'
"2.289.1"
```

```shell
$ ./jenkins-remote-script-console.py .env.example,.env.non.existent example.groovy
HTTPSConnectionPool(host='jenkins.domain.tld', port=443): Max retries exceeded with url: /context/scriptText (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7fe8dacf6910>: Failed to establish a new connection: [Errno -2] Name or service not known')) # This is output on stderr
[
  {
    "instance": "https://jenkins.domain.tld/context",
    "params": {
      "env_file": ".env.example",
      "user": "admin_username",
      "ssl_verify": false
    },
    "response": {
      "status_code": -1,
      "text": "HTTPSConnectionPool(host='jenkins.domain.tld', port=443): Max retries exceeded with url: /context/scriptText (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7fe8dacf6910>: Failed to establish a new connection: [Errno -2] Name or service not known'))" # You can also get the error message in the response
    }
  },
  {
    "instance": "env file does not exist",
    "params": {
      "env_file": ".env.non.existent"
    },
    "response": {
      "status_code": -1,
      "text": "request not performed"
    }
  }
]
```

```shell
$ ./jenkins-remote-script-console.py .env.example,.env.non.existent example.groovy | jq '.[0].response.text'
HTTPSConnectionPool(host='jenkins.domain.tld', port=443): Max retries exceeded with url: /context/scriptText (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7fd25aed7910>: Failed to establish a new connection: [Errno -2] Name or service not known')) # This comes from stderr
"HTTPSConnectionPool(host='jenkins.domain.tld', port=443): Max retries exceeded with url: /context/scriptText (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7fd25aed7910>: Failed to establish a new connection: [Errno -2] Name or service not known'))" # This comes from the response
```

