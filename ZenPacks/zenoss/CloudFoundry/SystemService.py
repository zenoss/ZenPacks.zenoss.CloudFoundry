from Globals import InitializeClass
from persistent.mapping import PersistentMapping

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class SystemService(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'CloudFoundrySystemService'

    cfId = None
    cfName = ''
    cfVersion = ''
    cfDescription = ''
    cfVendor = ''
    cfType = ''
    cfTiers = PersistentMapping()

    _properties = ManagedEntity._properties + (
        {'id': 'cfId', 'type': 'int', 'mode': ''},
        {'id': 'cfName', 'type': 'string', 'mode': ''},
        {'id': 'cfVersion', 'type': 'string', 'mode': ''},
        {'id': 'cfDescription', 'type': 'string', 'mode': ''},
        {'id': 'cfVendor', 'type': 'string', 'mode': ''},
        {'id': 'cfType', 'type': 'string', 'mode': ''},
        {'id': 'cfTiers', 'type': 'string', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('cfEndpoint', ToOne(ToManyCont,
            'ZenPacks.zenoss.CloudFoundry.Endpoint.Endpoint',
            'cfSystemServices'
            )
        ),
    )

    def device(self):
        return self.cfEndpoint()

    def getCFTiers(self):
        return self.cfTiers

    def setCFTiers(self, tiers):
        self.cfTiers = PersistentMapping(tiers)

InitializeClass(SystemService)

