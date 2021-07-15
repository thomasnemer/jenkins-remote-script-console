#!/usr/bin/env python3

import os,argparse,requests,sys,json
from dotenv import load_dotenv
from pathlib import Path

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("env_files", help="List of path to an env files separated by commas (,)")
parser.add_argument("script", help="Path to a script file to be executed on a jenkins instance")
args = parser.parse_args()
args.env_files.replace(", ", ",")
env_files = args.env_files.split(",")

def run_script_on_env(env_file, script):
  # Clean env
  try:
    del os.environ['JENKINS_INSTANCE']
    del os.environ['JENKINS_USER']
    del os.environ['JENKINS_TOKEN']
    del os.environ['JENKINS_SSL_VERIFY']
  except:
    pass

  # Parse env file
  load_dotenv(dotenv_path=Path(env_file))
  instance = os.getenv('JENKINS_INSTANCE')
  user = os.getenv('JENKINS_USER')
  token = os.getenv('JENKINS_TOKEN')
  ssl_verify = os.getenv('JENKINS_SSL_VERIFY', 'true').lower in ('true', '1')

  # If we don't want to check for ssl certificate validity, we don't want to be warned about it either
  if not ssl_verify:
    requests.packages.urllib3.disable_warnings()

  # Do the thing
  result = dict()
  result['instance'] = instance
  params = dict()
  params['user'] = user
  params['ssl_verify'] = ssl_verify
  result['params'] = params
  result['response'] = dict()

  endpoint = instance + '/scriptText'

  try:
    response = requests.post(endpoint, auth=(user, token), data={'script': script}, verify=ssl_verify)
    response.raise_for_status()
  except requests.ConnectionError as e:
    print(str(e), file=sys.stderr)
    print("Check your network connection.", file=sys.stderr)
    result['response']['status_code'] = -1
    result['response']['text'] = str(e)
    return result
  except requests.Timeout as e:
    print(str(e), file= sys.stderr)
    print("Check jenkins is up.", file=sys.stderr)
    result['response']['status_code'] = -1
    result['response']['text'] = str(e)
    return result
  except KeyboardInterrupt:
    print("User interruption.", file=sys.stderr)
    result['response']['status_code'] = -1
    result['response']['text'] = str(e)
    return result
  except requests.exceptions.HTTPError as e:
    print(str(e), file=sys.stderr)
    result['response']['status_code'] = -1
    result['response']['text'] = str(e)
    return result
  except requests.RequestException as e:
    print(str(e), file=sys.stderr)
    result['response']['status_code'] = -1
    result['response']['text'] = str(e)
    return result
  result['response']['status_code'] = response.status_code
  result['response']['text'] = response.text
  return result

# Parse script file
with open(args.script, 'r') as script_file:
  script = script_file.read()

all_requests = []
for env_file in env_files:
  all_requests.append(run_script_on_env(env_file, script))
print(json.dumps(all_requests, indent=2))
