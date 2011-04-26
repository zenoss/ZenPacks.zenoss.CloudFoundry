from Globals import InitializeClass

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

from ZenPacks.zenoss.CloudFoundry.util import CollectedOrModeledMixin

class AppInstance(DeviceComponent, ManagedEntity, CollectedOrModeledMixin):
    meta_type = portal_type = 'CloudFoundryAppInstance'

    cfIndex = None
    cfState = ''
    cfSince = None
    cfCores = None
    cfHost = ''
    cfPort = None

    # We do more frequent collection of these values, but it's good to have an
    # immediate value to use as soon as the device is added.
    modeled_quotaMemory = None
    modeled_quotaDisk = None
    modeled_usageCPU = None
    modeled_usageMemory = None
    modeled_usageDisk = None

    _properties = ManagedEntity._properties + (
        {'id': 'cfIndex', 'type': 'int', 'mode': ''},
        {'id': 'cfState', 'type': 'string', 'mode': ''},
        {'id': 'cfSince', 'type': 'int', 'mode': ''},
        {'id': 'cfCores', 'type': 'int', 'mode':''},
        {'id': 'cfHost', 'type': 'string', 'mode':''},
        {'id': 'cfPort', 'type': 'int', 'mode':''},
        {'id': 'modeled_quotaMemory', 'type': 'int', 'mode':''},
        {'id': 'modeled_quotaDisk', 'type': 'int', 'mode':''},
        {'id': 'modeled_usageCPU', 'type': 'float', 'mode':''},
        {'id': 'modeled_usageMemory', 'type': 'float', 'mode':''},
        {'id': 'modeled_usageDisk', 'type': 'float', 'mode':''},
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

