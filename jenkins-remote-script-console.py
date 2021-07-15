#!/usr/bin/env python3

import os,argparse,requests
from dotenv import load_dotenv
from pathlib import Path
requests.packages.urllib3.disable_warnings()

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("env_file", help="Path to an env file containing credentials and instance configuration")
parser.add_argument("script", help="Path to a script file to be executed on a jenkins instance")
args = parser.parse_args()

# Parse env file
load_dotenv(dotenv_path=Path(args.env_file))
INSTANCE = os.getenv('JENKINS_INSTANCE')
USER = os.getenv('JENKINS_USER')
TOKEN = os.getenv('JENKINS_TOKEN')
SSL_VERIFY = os.getenv('JENKINS_SSL_VERIFY', 'true').lower in ('true', '1')

# Parse script file
with open(args.script, 'r') as script_file:
  script = script_file.read()

# Do the thing
endpoint = INSTANCE + '/scriptText'
r = requests.post(endpoint, auth=(USER, TOKEN), data={'script': script}, verify=SSL_VERIFY)
print(r.text)
