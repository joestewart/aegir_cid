#! /usr/bin/env python

import sys
import string
import os
from fabric.api import *

# Add a new site deployment job to Jenkins
def jenkins_project_deployment(filename):
  email = open(filename, 'r')
  args = [ ]
  for line in email:
    for key in [ "site", "install_profile", "aegirserver", "webserver", "dbserver", "makefile", "repo", "branch" ]:
      if key in line: 
        splitter = string.split(line, "=")
        splitter = string.split(splitter[1], ": ")
        splitter = string.split(splitter[1], "\n")
        args.append(splitter[0])
  
  arguments = string.join(args, ' ')

  # Kick off the new deploy job in Jenkins
  os.system('/usr/local/bin/newjenkinsjob %s' % arguments)

# Let's test to see if the request has come in via email or from CLI
def process_request():
  if not sys.stdin.isatty():

    rawmessage = sys.stdin.read()
    
    filename = '/tmp/rawmessage.%s.txt' % os.getpid()
    logfile = open(filename, 'w')
    logfile.write(rawmessage)
    logfile.close()

    logfile = open(filename, 'r')
    for line in logfile:
      if 'Subject' in line:
        _split_arg = string.split(line, ":")
        subject = _split_arg[1]
        if "New Aegir Site deployment" in subject:
          jenkins_project_deployment(filename)
    logfile.close()

if __name__ == "__main__":
  process_request()
