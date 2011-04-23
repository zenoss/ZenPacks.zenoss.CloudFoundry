from Products.ZenModel.ZenPack import ZenPack as ZenPackBase

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

    def remove(self, app, leaveObjects=False):
        super(ZenPack, self).remove(app, leaveObjects=False)

