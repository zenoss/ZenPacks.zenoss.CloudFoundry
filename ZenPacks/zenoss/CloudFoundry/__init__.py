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
        self.removePluginSymlink()
        super(ZenPack, self).remove(app, leaveObjects=False)

    def symlinkPlugin(self):
        os.system('ln -sf {0}/poll_vcap {1}/poll_vcap'.format(
            self.path(), zenPath('libexec')))
            
    def removePluginSymlink(self):
        os.system('rm -f {0}'.format(zenPath('libexec', 'poll_vcap')))

