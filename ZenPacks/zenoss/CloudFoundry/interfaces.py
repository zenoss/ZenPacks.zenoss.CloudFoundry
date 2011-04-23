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
    instances = schema.Int(title=_t("Instances"))
    runningInstances = schema.Int(title=_t("Running Instances"))
    resourcesMemory = schema.Int(title=_t("Resources: Memory"))
    resourcesDisk = schema.Int(title=_t("Resources: Disk"))
    resourcesFDS = schema.Int(title=_t("Resources: File Descriptors"))

class IAppInstanceInfo(IComponentInfo):
    pass

class IFrameworkInfo(IComponentInfo):
    pass

class IRuntimeInfo(IComponentInfo):
    pass

class IAppServerInfo(IComponentInfo):
    pass

class ISystemServiceInfo(IComponentInfo):
    pass

class IProvisionedServiceInfo(IComponentInfo):
    pass

