from Products.Zuul.form import schema
from Products.Zuul.interfaces import IFacade
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.interfaces.device import IDeviceInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

class ICloudFoundryFacade(IFacade):
    def addEndpoint(self, target, email, password, collector):
        """
        Add CloudFoundry Endpoint.
        """

class IEndpointInfo(IDeviceInfo):
    cfName = schema.Text(title=_t(u"Name"))
    cfDescription = schema.Text(title=_t(u"Description"))
    cfVersion = schema.Text(title=_t(u"Version"))
    cfBuild = schema.Text(title=_t(u"Build"))
    cfUser = schema.Text(title=_t(u"User"))
    cfSupport = schema.Text(title=_t(u"Support"))
    limitAppURIs = schema.Int(title=_t(u"Limit: App URIs"))
    limitApps = schema.Int(title=_t(u"Limit: Apps"))
    limitMemory = schema.Int(title=_t(u"Limit: Memory"))
    limitServices = schema.Int(title=_t(u"Limit: Services"))
    usageAppURIs = schema.Int(title=_t(u"Usage: App URIs"))
    usageApps = schema.Int(title=_t(u"Usage: Apps"))
    usageMemory = schema.Int(title=_t(u"Usage: Memory"))
    usageServices = schema.Int(title=_t(u"Usage: Services"))
    utilAppURIs = schema.Text(title=_t(u"App URIs (Usage / Limit)"))
    utilApps = schema.Text(title=_t(u"Apps (Usage / Limit)"))
    utilMemory = schema.Text(title=_t(u"Memory (Usage / Limit)"))
    utilServices = schema.Text(title=_t(u"Services (Usage / Limit)"))

class IAppInfo(IComponentInfo):
    cfName = schema.Text(title=_t(u"Name"))
    cfVersion = schema.Text(title=_t(u"Version"))
    cfState = schema.Text(title=_t("State"))
    cfMetaCreated = schema.Int(title=_t("Created"))
    cfMetaVersion = schema.Text(title=_t("Version"))
    cfURIs = schema.List(title=_t("URIs"))
    cfServices = schema.List(title=_t("Services"))
    cfStagingModel = schema.Text(title=_t(u"Model"))
    cfStagingStack = schema.Text(title=_t(u"Stack"))
    instances = schema.Text(title=_t("Instances"))
    resourcesMemory = schema.Int(title=_t("Resources: Memory"))
    resourcesDisk = schema.Int(title=_t("Resources: Disk"))
    cfFramework = schema.Entity(title=_t("Framework"))
    cfRuntime = schema.Entity(title=_t("Runtime"))

class IAppInstanceInfo(IComponentInfo):
    cfApp = schema.Entity(title=_t(u"App"))
    cfIndex = schema.Int(title=_t(u"Index"))
    cfState = schema.Text(title=_t(u"State"))
    utilCPU = schema.Text(title=_t(u"CPU Utilization"))
    utilMemory = schema.Text(title=_t(u"Memory Utilization"))
    utilDisk = schema.Text(title=_t(u"Disk Utilization"))
    cfHost = schema.Text(title=_t(u"Host"))
    cfPort = schema.Int(title=_t(u"Port"))
    cfSince = schema.Int(title=_t(u"Since"))

class IFrameworkInfo(IComponentInfo):
    cfName = schema.Text(title=_t(u"Name"))
    cfDetection = schema.List(title=_t(u"Detection"))
    cfRuntimeCount = schema.Int(title=_t(u"# Runtimes"))
    cfAppServerCount = schema.Int(title=_t(u"# App Servers"))
    cfAppCount = schema.Int(title=_t(u"# Apps"))

class IRuntimeInfo(IComponentInfo):
    cfFramework = schema.Entity(title=_t(u"Framework"))
    cfName = schema.Text(title=_t(u"Name"))
    cfDescription = schema.Text(title=_t(u"Description"))
    cfVersion = schema.Text(title=_t(u"Version"))
    cfAppCount = schema.Text(title=_t(u"# Apps"))

class IAppServerInfo(IComponentInfo):
    cfFramework = schema.Entity(title=_t(u"Framework"))
    cfName = schema.Text(title=_t(u"Name"))
    cfDescription = schema.Text(title=_t(u"Description"))

class ISystemServiceInfo(IComponentInfo):
    cfId = schema.Int(title=_t(u"ID"))
    cfName = schema.Text(title=_t(u"Name"))
    cfDescription = schema.Text(title=_t(u"Description"))
    cfVersion = schema.Text(title=_t(u"Version"))
    cfVendor = schema.Text(title=_t(u"Vendor"))
    cfType = schema.Text(title=_t(u"Type"))
    cfTiers = schema.Text(title=_t(u"Tiers"))
    cfProvisionedCount = schema.Int(title=_t(u"# Provisioned"))

class IProvisionedServiceInfo(IComponentInfo):
    cfSystemService = schema.Entity(title=_t(u"System Service"))
    cfName = schema.Text(title=_t(u"Name"))
    cfVersion = schema.Text(title=_t(u"Version"))
    cfVendor = schema.Text(title=_t(u"Vendor"))
    cfType = schema.Text(title=_t(u"Type"))
    cfTier = schema.Text(title=_t(u"Tier"))
    cfMetaCreated = schema.Int(title=_t(u"Created (Meta)"))
    cfMetaUpdated = schema.Int(title=_t(u"Updated (Meta)"))
    cfMetaVersion = schema.Int(title=_t(u"Version (Meta)"))
    cfMetaTags = schema.Text(title=_t(u"Tags"))
    cfProperties = schema.Text(title=_t(u"Properties"))

