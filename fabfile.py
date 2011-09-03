from fabric.api import *
import time

env.user = 'aegir'

# Download and import a platform using Drush Make
def build_platform(site, profile, webserver, dbserver, makefile, build):
  print "===> Building the platform..."
  run("drush make %s /var/aegir/platforms/%s" % (makefile, build), pty=True )
  run("drush --root='/var/aegir/platforms/%s' provision-save '@platform_%s' --context_type='platform'" % (build, build), pty=True)
  run("drush @hostmaster hosting-import '@platform_%s'" % build, pty=True)
  run("drush @hostmaster hosting-dispatch", pty=True)

# Install a site on a platform, and kick off an import of the site
def install_site(site, profile, webserver, dbserver, makefile, build):
  print "===> Installing the site for the first time..."
  run("drush @%s provision-install" % site, pty=True)
  run("drush @hostmaster hosting-task @platform_%s verify" % build, pty=True)
  time.sleep(5)
  run("drush @hostmaster hosting-dispatch", pty=True)
  time.sleep(5)
  run("drush @hostmaster hosting-task @%s verify" % site, pty=True)

# Migrate a site to a new platform
def migrate_site(site, profile, webserver, dbserver, makefile, build):
  print "===> Migrating the site to the new platform"
  run("drush @%s provision-migrate '@platform_%s'" % (site, build), pty=True)

# Save the Drush alias to reflect the new platform
def save_alias(site, profile, webserver, dbserver, makefile, build):
  print "===> Updating the Drush alias for this site"
  run("drush provision-save @%s --context_type=site --uri=%s --platform=@platform_%s --server=@server_%s --db_server=@server_%s --profile=%s --client_name=admin" % (site, site, build, webserver, dbserver, profile), pty=True)

# Import a site into the frontend, so that Aegir learns the site is now on the new platform
def import_site(site, profile, webserver, dbserver, makefile, build):
  print "===> Refreshing the frontend to reflect the site under the new platform"
  run("drush @hostmaster hosting-import @%s" % site, pty=True)
  run("drush @hostmaster hosting-task @platform_%s verify" % build, pty=True)
  # Seem to need to run hosting-import twice, otherwise the site's profile is 'n/a'
  run("drush @hostmaster hosting-import @%s" % site, pty=True)
  run("drush @hostmaster hosting-task @%s verify" % site, pty=True)

