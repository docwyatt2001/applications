import nginx
import os

from arkos.languages import php
from arkos.websites import Site
from arkos.system import users, groups


class Lychee(Site):
    addtoblock = [
        nginx.Location(
            '= /favicon.ico',
            nginx.Key('log_not_found', 'off'),
            nginx.Key('access_log', 'off')
        ),
        nginx.Location(
            '= /robots.txt',
            nginx.Key('allow', 'all'),
            nginx.Key('log_not_found', 'off'),
            nginx.Key('access_log', 'off')
        ),
        nginx.Location(
            '~ \.php$',
            nginx.Key('fastcgi_pass', 'unix:/run/php-fpm/php-fpm.sock'),
            nginx.Key('fastcgi_index', 'index.php'),
            nginx.Key('include', 'fastcgi.conf')
        )]

    def pre_install(self, extra_vars):
        pass

    def post_install(self, extra_vars, dbpasswd=""):
        # Create Lychee automatic configuration file
        with open(os.path.join(self.path, 'data', 'config.php'), 'w') as f:
            f.write(
                "<?php\n"
                "   if(!defined('LYCHEE')) "
                "exit('Error: Direct access is allowed!');\n"
                "   $dbHost = 'localhost';\n"
                "   $dbUser = '{0}';\n"
                "   $dbPassword = '{1}';\n"
                "   $dbName = '{0}';\n"
                "   $dbTablePrefix = '';\n"
                "?>\n".format(self.db.id, dbpasswd)
            )

        # Make sure that the correct PHP settings are enabled
        php.enable_mod('mysql', 'mysqli', 'gd',
                       'zip', 'exif', 'json', 'mbstring')

        # Rename lychee index.html to index.php to make it
        # work with our default nginx config
        os.rename(os.path.join(self.path, "index.html"),
                  os.path.join(self.path, "index.php"))

        # Finally, make sure that permissions are set so that Lychee
        # can make adjustments and save plugins when need be.
        uid, gid = users.get_system("http").uid, groups.get_system("http").gid
        for r, d, f in os.walk(self.path):
            for x in d:
                os.chown(os.path.join(r, x), uid, gid)
            for x in f:
                os.chown(os.path.join(r, x), uid, gid)

    def pre_remove(self):
        pass

    def post_remove(self):
        pass

    def enable_ssl(self, cfile, kfile):
        pass

    def disable_ssl(self):
        pass
