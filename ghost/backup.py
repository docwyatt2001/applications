import os

from arkos.languages import nodejs
from arkos.system import services, users
from arkos.backup import BackupController


class GhostBackup(BackupController):
    def get_config(self, site):
        return ["/etc/supervisor.d/%s.ini" % site.name]
    
    def get_data(self, site):
        pass
    
    def pre_backup(self, site):
        pass
    
    def post_backup(self, site):
        pass
    
    def pre_restore(self, site):
        pass
    
    def post_restore(self, site):
        nodejs.install_from_package(site.path, 'production', 
            {'sqlite': '/usr/bin', 'python': '/usr/bin/python2'})
        users.SystemUser("ghost").add()
        uid = users.get_system("ghost").uid
        for r, d, f in os.walk(site.path):
            for x in d:
                os.chown(os.path.join(root, x), uid, -1)
            for x in f:
                os.chown(os.path.join(root, x), uid, -1)
        services.get(site.name).enable()