from Globals import InitializeClass
from persistent.list import PersistentList

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

from ZenPacks.zenoss.CloudFoundry.util import CollectedOrModeledMixin

class App(DeviceComponent, ManagedEntity, CollectedOrModeledMixin):
    meta_type = portal_type = 'CloudFoundryApp'

    cfName = ''
    cfVersion = ''
    cfState = ''
    cfMetaCreated = None
    cfMetaVersion = ''
    cfURIs = PersistentList()
    cfServices = PersistentList()
    cfStagingModel = ''
    cfStagingStack = ''

    # We do more frequent collection of these values, but it's good to have an
    # immediate value to use as soon as the device is added.
    modeled_instances = None
    modeled_runningInstances = None
    modeled_resourcesMemory = None
    modeled_resourcesDisk = None

    _properties = ManagedEntity._properties + (
        {'id': 'cfName', 'type': 'string', 'mode': ''},
        {'id': 'cfVersion', 'type': 'string', 'mode': ''},
        {'id': 'cfState', 'type': 'string', 'mode': ''},
        {'id': 'cfMetaCreated', 'type': 'int', 'mode': ''},
        {'id': 'cfMetaVersion', 'type': 'string', 'mode': ''},
        {'id': 'cfURIs', 'type': 'lines', 'mode': ''},
        {'id': 'cfServices', 'type': 'lines', 'mode': ''},
        {'id': 'cfStagingModel', 'type': 'string', 'mode': ''},
        {'id': 'cfStagingStack', 'type': 'string', 'mode': ''},
        {'id': 'modeled_instances', 'type':'int', 'mode': ''},
        {'id': 'modeled_runningInstances', 'type':'int', 'mode': ''},
        {'id': 'modeled_resourcesMemory', 'type':'int', 'mode': ''},
        {'id': 'modeled_resourcesDisk', 'type':'int', 'mode': ''},
    )

    _relations = ManagedEntity._relations + (
        ('cfEndpoint', ToOne(ToManyCont,
            'ZenPacks.zenoss.CloudFoundry.Endpoint.Endpoint',
            'cfApps'
            )
        ),
        ('cfAppInstances', ToManyCont(ToOne,
            'ZenPacks.zenoss.CloudFoundry.AppInstance.AppInstance',
            'cfApp'
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

    def getCFURIs(self):
        return self.cfURIs

    def setCFURIs(self, uris):
        self.cfURIs = PersistentList(uris)

    def getCFServices(self):
        return self.cfServices

    def setCFServices(self, services):
        self.cfServices = PersistentList(services)

    @property
    def cfFramework(self):
        return self.cfEndpoint().cfFrameworks._getOb(self.cfStagingModel, None)

    @property
    def cfRuntime(self):
        framework = self.cfFramework
        return framework.cfRuntimes._getOb(self.cfStagingStack, None)

InitializeClass(App)

