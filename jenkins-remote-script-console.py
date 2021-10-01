#!/usr/bin/env python3

import os,argparse,requests,sys,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv
from pathlib import Path

def clean_env():
  try:
    del os.environ['JENKINS_INSTANCE']
    del os.environ['JENKINS_USER']
    del os.environ['JENKINS_TOKEN']
    del os.environ['JENKINS_SSL_VERIFY']
  except:
    pass

def run_script_on_env(env_file, script):
  # Clean env
  clean_env()

  # Parse env file
  load_dotenv(dotenv_path=Path(env_file))
  instance = os.getenv('JENKINS_INSTANCE')
  user = os.getenv('JENKINS_USER')
  token = os.getenv('JENKINS_TOKEN')
  ssl_verify = os.getenv('JENKINS_SSL_VERIFY').lower() in ('true', '1')

  # If we don't want to check for ssl certificate validity, we don't want to be warned about it either
  if not ssl_verify:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

  # Do the thing
  params = dict()
  params['env_file'] = env_file
  params['user'] = user
  params['ssl_verify'] = ssl_verify
  result = dict()
  result['instance'] = instance
  result['params'] = params
  result['response'] = dict()

  # Perform the request
  endpoint = instance + '/scriptText'
  try:
    response = requests.post(endpoint, auth=(user, token), data={'script': script}, verify=ssl_verify)
    response.raise_for_status()
  except Exception as e:
    print(str(e), file=sys.stderr)
    result['response']['status_code'] = -1
    result['response']['text'] = str(e)
    clean_env()
    return result
  except KeyboardInterrupt as e:
    print("User interruption.", file=sys.stderr)
    clean_env()
    sys.exit(1)
  result['response']['status_code'] = response.status_code
  try:
    json_response = json.loads(response.text)
    result['response']['text'] = json_response
  except ValueError as e:
    result['response']['text'] = response.text
  clean_env()
  return result

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("env_files", help="List of path to an env files separated by commas (,)")
parser.add_argument("script", help="Path to a script file to be executed on a jenkins instance")
args = parser.parse_args()
args.env_files.replace(", ", ",")
env_files = args.env_files.split(",")

# Parse script file
if not os.path.exists(args.script):
  print("Script file {} does not exist.".format(args.script), file=sys.stderr)
  sys.exit(1)
with open(args.script, 'r') as script_file:
  script = script_file.read()

all_requests = []
for env_file in env_files:
  if os.path.exists(env_file):
    all_requests.append(run_script_on_env(env_file, script))
  else:
    result = dict()
    result['instance'] = "env file does not exist"
    result['params'] = dict()
    result['params']['env_file'] = env_file
    result['response'] = dict()
    result['response']['status_code'] = -1
    result['response']['text'] = "request not performed"
    all_requests.append(result)

# Print the results
print(json.dumps(all_requests, indent=2))
