from fabric.api import *
import time

env.user = 'aegir'
env.shell = '/bin/bash -c'

# Download and import a platform using Drush Make
def build_platform(site, profile, webserver, dbserver, makefile, build, platform = 'platform'):
  print "===> Building the platform..."
  run("drush make %s /var/aegir/platforms/%s_%s" % (makefile, platform, build))
  run("drush --root='/var/aegir/platforms/%s_%s' provision-save '@%s_%s' --context_type='platform'" % (platform, build, platform, build))
  run("drush @hostmaster hosting-import '@%s_%s'" % (platform, build))
  run("drush @hostmaster hosting-dispatch")

# Install a site on a platform, and kick off an import of the site
def install_site(site, profile, webserver, dbserver, makefile, build, platform = 'platform'):
  print "===> Installing the site for the first time..."
  run("drush @%s provision-install" % site)
  run("drush @hostmaster hosting-task @%s_%s verify" % (platform, build))
  time.sleep(5)
  run("drush @hostmaster hosting-dispatch")
  time.sleep(5)
  run("drush @hostmaster hosting-task @%s verify" % site)

# Migrate a site to a new platform
def migrate_site(site, profile, webserver, dbserver, makefile, build, platform = 'platform'):
  print "===> Migrating the site to the new platform"
  run("drush @%s provision-migrate '@%s_%s'" % (site, platform, build))

# Save the Drush alias to reflect the new platform
def save_alias(site, profile, webserver, dbserver, makefile, build, platform = 'platform'):
  print "===> Updating the Drush alias for this site"
  run("drush provision-save @%s --context_type=site --uri=%s --platform=@%s_%s --server=@server_%s --db_server=@server_%s --profile=%s --client_name=admin" % (site, site, platform, build, webserver, dbserver, profile))

# Import a site into the frontend, so that Aegir learns the site is now on the new platform
def import_site(site, profile, webserver, dbserver, makefile, build, platform = 'platform'):
  print "===> Refreshing the frontend to reflect the site under the new platform"
  run("drush @hostmaster hosting-import @%s" % site)
  run("drush @hostmaster hosting-task @%s_%s verify" % (platform, build))
  run("drush @hostmaster hosting-import @%s" % site)
  run("drush @hostmaster hosting-task @%s verify" % site)
