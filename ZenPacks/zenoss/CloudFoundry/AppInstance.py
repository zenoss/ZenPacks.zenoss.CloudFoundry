from Globals import InitializeClass

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class AppInstance(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'CloudFoundryAppInstance'

    cfIndex = None
    cfState = ''
    cfSince = None

    _properties = ManagedEntity._properties + (
        {'id': 'cfIndex', 'type': 'int', 'mode': ''},
        {'id': 'cfState', 'type': 'string', 'mode': ''},
        {'id': 'cfSince', 'type': 'int', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('cfApp', ToOne(ToManyCont,
            'ZenPacks.zenoss.CloudFoundry.App.App',
            'cfAppInstances'
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
        return self.cfApp().cfEndpoint()

InitializeClass(AppInstance)

