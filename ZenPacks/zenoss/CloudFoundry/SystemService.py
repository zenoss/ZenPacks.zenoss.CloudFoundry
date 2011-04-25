from Globals import InitializeClass
from persistent.mapping import PersistentMapping

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
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

    # Meta-data: Zope object views and actions
    factory_type_information = ({
        'actions': ({ 
            'id': 'perfConf', 
            'name': 'Template', 
            'action': 'objTemplates', 
            'permissions': (ZEN_CHANGE_DEVICE,), 
            },), 
        },)

    def device(self):
        return self.cfEndpoint()

    def getCFTiers(self):
        return self.cfTiers

    def setCFTiers(self, tiers):
        self.cfTiers = PersistentMapping(tiers)

InitializeClass(SystemService)

