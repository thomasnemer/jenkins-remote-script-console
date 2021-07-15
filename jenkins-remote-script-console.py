#!/usr/bin/env python3

import os,argparse,requests,sys
from dotenv import load_dotenv
from pathlib import Path

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

# If we don't want to check for ssl certificate validity, we don't want to be warned about it either
if not SSL_VERIFY:
  requests.packages.urllib3.disable_warnings()

# Parse script file
with open(args.script, 'r') as script_file:
  script = script_file.read()

# Do the thing
endpoint = INSTANCE + '/scriptText'
try:
  req = requests.post(endpoint, auth=(USER, TOKEN), data={'script': script}, verify=SSL_VERIFY)
  req.raise_for_status()
except requests.ConnectionError as e:
  print(str(e), file=sys.stderr)
  print("Check your network connection.", file=sys.stderr)
  sys.exit(1)
except requests.Timeout as e:
  print(str(e), file= sys.stderr)
  print("Check jenkins is up.", file=sys.stderr)
  sys.exit(1)
except KeyboardInterrupt:
  print("User interruption.", file=sys.stderr)
  sys.exit(1)
except requests.exceptions.HTTPError as e:
  print(str(e), file=sys.stderr)
  sys.exit(1)
except requests.RequestException as e:
  print(str(e), file=sys.stderr)
  sys.exit(1)

print(req.text)
