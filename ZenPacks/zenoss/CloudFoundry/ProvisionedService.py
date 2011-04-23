from Globals import InitializeClass
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class ProvisionedService(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'CloudFoundryProvisionedService'

    cfName = ''
    cfVersion = ''
    cfVendor = ''
    cfType = ''
    cfTier = ''
    cfMetaCreated = None
    cfMetaUpdated = None
    cfMetaVersion = None
    cfMetaTags = PersistentList()
    cfProperties = PersistentMapping()

    _properties = ManagedEntity._properties + (
        {'id': 'cfName', 'type': 'string', 'mode': ''},
        {'id': 'cfVersion', 'type': 'string', 'mode': ''},
        {'id': 'cfVendor', 'type': 'string', 'mode': ''},
        {'id': 'cfType', 'type': 'string', 'mode': ''},
        {'id': 'cfTier', 'type': 'string', 'mode': ''},
        {'id': 'cfMetaCreated', 'type': 'int', 'mode': ''},
        {'id': 'cfMetaUpdated', 'type': 'int', 'mode': ''},
        {'id': 'cfMetaVersion', 'type': 'int', 'mode': ''},
        {'id': 'cfMetaTags', 'type': 'string', 'mode': ''},
        {'id': 'cfProperties', 'type': 'string', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('cfEndpoint', ToOne(ToManyCont,
            'ZenPacks.zenoss.CloudFoundry.Endpoint.Endpoint',
            'cfProvisionedServices'
            )
        ),
    )

    def device(self):
        return self.cfEndpoint()

    def getCFProperties(self):
        return self.cfProperties

    def setCFProperties(self, properties):
        self.cfProperties = PersistentMapping(properties)

    def getCFMetaTags(self):
        return self.cfMetaTags

    def setCFMetaTags(self, metaTags):
        self.cfMetaTags = PersistentList(metaTags)

InitializeClass(ProvisionedService)

