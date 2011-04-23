from Products.ZenUtils.Ext import DirectRouter, DirectResponse
from Products import Zuul

class CloudFoundryRouter(DirectRouter):
    def _getFacade(self):
        return Zuul.getFacade('cloudfoundry', self.context)

    def addEndpoint(self, target, email, password, collector=None):
        if not collector:
            collector = 'localhost'

        facade = self._getFacade()
        success, message = facade.addEndpoint(
            target, email, password, collector)
        
        if success:
            return DirectResponse.succeed(jobId=message)
        else:
            return DirectResponse.fail(message)

