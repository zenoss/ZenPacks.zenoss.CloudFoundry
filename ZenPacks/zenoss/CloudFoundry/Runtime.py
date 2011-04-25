from Globals import InitializeClass

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class Runtime(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'CloudFoundryRuntime'

    cfName = ''
    cfDescription = ''
    cfVersion = ''

    _properties = ManagedEntity._properties + (
        {'id': 'cfName', 'type': 'string', 'mode': ''},
        {'id': 'cfDescription', 'type': 'string', 'mode': ''},
        {'id': 'cfVersion', 'type': 'string', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('cfFramework', ToOne(ToManyCont,
            'ZenPacks.zenoss.CloudFoundry.Framework.Framework',
            'cfRuntimes'
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
        return self.cfFramework().cfEndpoint()

InitializeClass(Runtime)

