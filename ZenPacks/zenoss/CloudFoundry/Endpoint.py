from Globals import InitializeClass

from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

from ZenPacks.zenoss.CloudFoundry.util import CollectedOrModeledMixin

class Endpoint(Device, CollectedOrModeledMixin):
    meta_type = portal_type = 'CloudFoundryEndpoint'

    cfName = ''
    cfDescription = ''
    cfVersion = ''
    cfBuild = ''
    cfUser = ''
    cfSupport = ''

    # We do more frequent collection of these values, but it's good to have an
    # immediate value to use as soon as the device is added.
    modeled_limitAppURIs = None
    modeled_limitApps = None
    modeled_limitMemory = None
    modeled_limitServices = None
    modeled_usageAppURIs = None
    modeled_usageApps = None
    modeled_usageMemory = None
    modeled_usageServices = None

    _properties = Device._properties + (
        {'id': 'cfName', 'type': 'string', 'mode': ''},
        {'id': 'cfDescription', 'type': 'string', 'mode': ''},
        {'id': 'cfVersion', 'type': 'string', 'mode': ''},
        {'id': 'cfBuild', 'type': 'string', 'mode': ''},
        {'id': 'cfUser', 'type': 'string', 'mode': ''},
        {'id': 'cfSupport', 'type': 'string', 'mode': ''},
        {'id': 'modeled_limitAppURIs', 'type': 'int', 'mode': ''},
        {'id': 'modeled_limitApps', 'type': 'int', 'mode': ''},
        {'id': 'modeled_limitMemory', 'type': 'int', 'mode': ''},
        {'id': 'modeled_limitServices', 'type': 'int', 'mode': ''},
        {'id': 'modeled_usageAppURIs', 'type': 'int', 'mode': ''},
        {'id': 'modeled_usageApps', 'type': 'int', 'mode': ''},
        {'id': 'modeled_usageMemory', 'type': 'int', 'mode': ''},
        {'id': 'modeled_usageServices', 'type': 'int', 'mode': ''},
    )

    _relations = Device._relations + (
        ('cfApps', ToManyCont(ToOne,
            'ZenPacks.zenoss.CloudFoundry.App.App',
            'cfEndpoint'
            )
        ),
        ('cfFrameworks', ToManyCont(ToOne,
            'ZenPacks.zenoss.CloudFoundry.Framework.Framework',
            'cfEndpoint'
            )
        ),
        ('cfSystemServices', ToManyCont(ToOne,
            'ZenPacks.zenoss.CloudFoundry.SystemService.SystemService',
            'cfEndpoint'
            )
        ),
        ('cfProvisionedServices', ToManyCont(ToOne,
            'ZenPacks.zenoss.CloudFoundry.ProvisionedService.ProvisionedService',
            'cfEndpoint'
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

InitializeClass(Endpoint)

