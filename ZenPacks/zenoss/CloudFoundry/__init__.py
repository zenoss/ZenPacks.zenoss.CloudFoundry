import logging
log = logging.getLogger('zen.CloudFoundry')

import os

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenUtils.Utils import zenPath

class ZenPack(ZenPackBase):
    """
    Custom ZenPack object for CloudFoundry ZenPack. Handles specific
    installation and removal requirements.
    """
    packZProperties =  [
        ('zCloudFoundryTarget', '', 'string'),
        ('zCloudFoundryEmail', '', 'string'),
        ('zCloudFoundryPassword', '', 'password'),
        ]

    def install(self, app):
        super(ZenPack, self).install(app)
        self.symlinkPlugin()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            self.removePluginSymlink()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def symlinkPlugin(self):
        log.info('Linking poll_vcap plugin into $ZENHOME/libexec/')
        plugin_path = zenPath('libexec', 'poll_vcap')
        os.system('ln -sf {0} {1}'.format(
            self.path('poll_vcap'), plugin_path))
        os.system('chmod 0755 {0}'.format(plugin_path))
            
    def removePluginSymlink(self):
        log.info('Removing poll_vcap plugin link from $ZENHOME/libexec/')
        os.system('rm -f {0}'.format(zenPath('libexec', 'poll_vcap')))

