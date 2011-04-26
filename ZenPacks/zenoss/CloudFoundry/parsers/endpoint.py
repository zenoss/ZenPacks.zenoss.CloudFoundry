import json

from Products.ZenRRD.CommandParser import CommandParser

class endpoint(CommandParser):
    def processResults(self, cmd, result):
        data = json.loads(cmd.result.output)
        dp_map = dict([(dp.id, dp) for dp in cmd.points])

        limitAppURIs = data['info']['limits']['app_uris']
        limitApps = data['info']['limits']['apps']
        limitMemory = data['info']['limits']['memory'] * 1024 * 1024
        limitServices = data['info']['limits']['services']

        usageAppInstances = 0
        usageAppRunningInstances = 0
        for app in data['apps']:
            usageAppInstances += len(app['instances'])
            usageAppRunningInstances += app['runningInstances']

        usageAppURIs = data['info']['usage']['app_uris']
        usageApps = data['info']['usage']['apps']
        usageMemory = data['info']['usage']['memory'] * 1024 * 1024
        usageServices = data['info']['usage']['services']

        utilAppURIs = (float(usageAppURIs) / limitAppURIs) * 100.0
        utilApps = (float(usageApps) / limitApps) * 100.0
        utilMemory = (float(usageMemory) / limitMemory) * 100.0
        utilServices = (float(usageServices) / limitServices) * 100.0

        if 'limitAppURIs' in dp_map:
            result.values.append((dp_map['limitAppURIs'], limitAppURIs))

        if 'limitApps' in dp_map:
            result.values.append((dp_map['limitApps'], limitApps))

        if 'limitMemory' in dp_map:
            result.values.append((dp_map['limitMemory'], limitMemory))

        if 'limitServices' in dp_map:
            result.values.append((dp_map['limitServices'], limitServices))

        if 'usageAppURIs' in dp_map:
            result.values.append((dp_map['usageAppURIs'], usageAppURIs))

        if 'usageApps' in dp_map:
            result.values.append((dp_map['usageApps'], usageApps))

        if 'usageAppInstances' in dp_map:
            result.values.append((
                dp_map['usageAppInstances'], usageAppInstances))

        if 'usageAppRunningInstances' in dp_map:
            result.values.append((
                dp_map['usageAppRunningInstances'], usageAppRunningInstances))

        if 'usageMemory' in dp_map:
            result.values.append((dp_map['usageMemory'], usageMemory))

        if 'usageServices' in dp_map:
            result.values.append((dp_map['usageServices'], usageServices))

        if 'utilAppURIs' in dp_map:
            result.values.append((dp_map['utilAppURIs'], utilAppURIs))

        if 'utilApps' in dp_map:
            result.values.append((dp_map['utilApps'], utilApps))

        if 'utilMemory' in dp_map:
            result.values.append((dp_map['utilMemory'], utilMemory))

        if 'utilServices' in dp_map:
            result.values.append((dp_map['utilServices'], utilServices))

        return result

