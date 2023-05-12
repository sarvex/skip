#!/usr/bin/env python3

import http.client
import json
import os
import subprocess
import sys
import time


def circleci_command(method, url, body=None):
  token = os.environ['CIRCLE_TOKEN']
  conn = http.client.HTTPSConnection('circleci.com')
  conn.request(
      method,
      f'/api/v1.1/project/github/skiplang/skip{url}?circle-token={token}',
      body,
      {'Accept': 'application/json'},
  )
  res = conn.getresponse()
  return json.loads(res.read())

branch = os.environ['CIRCLE_BRANCH']
# Only do this optimization on pull request jobs
if not branch.startswith('pull/'):
    sys.exit(0)

while 1:
  output = subprocess.check_output([
      'git',
      'ls-remote',
      'git@github.com:skiplang/skip.git',
      f'refs/{branch}/head',
  ])
  rev = output.split()[0]
  print(f"Found rev ({rev}) vs running rev ({os.environ['CIRCLE_SHA1']})")
  if rev != os.environ['CIRCLE_SHA1']:
    print(f"Canceling myself (build: {os.environ['CIRCLE_BUILD_NUM']})")
    circleci_command('POST', f"/{os.environ['CIRCLE_BUILD_NUM']}/cancel")
  time.sleep(30)
