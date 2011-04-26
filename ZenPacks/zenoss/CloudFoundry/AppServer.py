from Globals import InitializeClass

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class AppServer(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'CloudFoundryAppServer'

    cfName = ''
    cfDescription = ''

    _properties = ManagedEntity._properties + (
        {'id': 'cfName', 'type': 'string', 'mode': ''},
        {'id': 'cfDescription', 'type': 'string', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('cfFramework', ToOne(ToManyCont,
            'ZenPacks.zenoss.CloudFoundry.Framework.Framework',
            'cfAppServers'
            )
        ),
    )

    def device(self):
        return self.cfFramework().cfEndpoint()

InitializeClass(AppServer)

