/*
 * Customizations to Endpoint Overview Page
 */
Ext.onReady(function() {
    var DEVICE_OVERVIEW_ID = 'deviceoverviewpanel_summary';
    Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_ID, function(){
        var box = Ext.getCmp(DEVICE_OVERVIEW_ID);
        box.removeField('uptime');
        box.removeField('memory');
    });

    var DEVICE_OVERVIEW_DESCRIPTION = 'deviceoverviewpanel_descriptionsummary';
    Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_DESCRIPTION, function(){
        var box = Ext.getCmp(DEVICE_OVERVIEW_DESCRIPTION);
        box.removeField('rackSlot');
        box.removeField('collector');
        box.removeField('hwManufacturer');
        box.removeField('hwModel');
        box.removeField('osManufacturer');
        box.removeField('osModel');

        box.addField({
            xtype: 'displayfield',
            name: 'cfName',
            fieldLabel: _t('CloudFoundry Name')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'cfDescription',
            fieldLabel: _t('CloudFoundry Description')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilAppURIs',
            fieldLabel: _t('App URIs')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilApps',
            fieldLabel: _t('Apps')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilMemory',
            fieldLabel: _t('Memory')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilServices',
            fieldLabel: _t('Services')
        });
    });

    var DEVICE_OVERVIEW_SNMP = 'deviceoverviewpanel_snmpsummary';
    Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_SNMP, function(){
        var box = Ext.getCmp(DEVICE_OVERVIEW_SNMP);
        box.removeField('snmpSysName');
        box.removeField('snmpLocation');
        box.removeField('snmpContact');
        box.removeField('snmpDescr');
        box.removeField('snmpCommunity');
        box.removeField('snmpVersion');

        box.addField({
            name: 'cfVersion',
            fieldLabel: _t('CloudFoundry Version')
        });

        box.addField({
            name: 'cfBuild',
            fieldLabel: _t('CloudFoundry Build')
        });

        box.addField({
            name: 'cfUser',
            fieldLabel: _t('CloudFoundry User')
        });

        box.addField({
            name: 'cfSupport',
            fieldLabel: _t('CloudFoundry Support')
        });
    });
});

(function(){

var ZC = Ext.ns('Zenoss.component');

/*
 * Friendly names for the components.
 */
ZC.registerName('CloudFoundryApp',
    _t('App'), _t('Apps'));

ZC.registerName('CloudFoundryAppInstance',
    _t('App Instance'), _t('App Instances'));

ZC.registerName('CloudFoundryFramework',
    _t('Framework'), _t('Frameworks'));

ZC.registerName('CloudFoundryRuntime',
    _t('Runtime'), _t('Runtimes'));

ZC.registerName('CloudFoundryAppServer',
    _t('App Server'), _t('App Servers'));

ZC.registerName('CloudFoundrySystemService',
    _t('System Service'), _t('System Services'));

ZC.registerName('CloudFoundryProvisionedService',
    _t('Provisioned Service'), _t('Provisioned Services'));

/*
 * Register types so jumpToEntity will work.
 */

// The DeviceClass matcher got too greedy in 3.1.x branch. Throttling it.
Zenoss.types.TYPES.DeviceClass[0] = new RegExp(
    "^/zport/dmd/Devices(/(?!devices)[^/*])*/?$");

Zenoss.types.register({
    'CloudFoundryApp':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfApps/[^/]*/?$",
    'CloudFoundryAppInstance':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfAppInstances/[^/]*/?$",
    'CloudFoundryFramework':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfFrameworks/[^/]*/?$",
    'CloudFoundryRuntime':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfRuntimes/[^/]*/?$",
    'CloudFoundryAppServer':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfAppServers/[^/]*/?$",
    'CloudFoundrySystemService':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfSystemServices/[^/]*/?$",
    'CloudFoundryProvisionedService':
        "^/zport/dmd/Devices/CloudFoundry/devices/.*/cfProvisionedServices/[^/]*/?$"
});


/*
 * Endpoint-local custom renderers.
 */
Ext.apply(Zenoss.render, {    
    entityLinkFromGrid: function(obj) {
        if (obj && obj.uid && obj.name) {
            if ( !this.panel || this.panel.subComponentGridPanel) {
                return String.format(
                    '<a href="javascript:Ext.getCmp(\'component_card\').componentgrid.jumpToEntity(\'{0}\', \'{1}\');">{1}</a>',
                    obj.uid, obj.name);
            } else {
                return obj.name;
            }
        }
    },
    
    deviceLinkFromGrid: function(obj) {
        if (obj && obj.uid && obj.name) {
            return Zenoss.render.Device(obj.uid, obj.name);
        }
    }
});

/*
 * Generic ComponentGridPanel
 */
ZC.CloudFoundryComponentGridPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,
    
    jumpToEntity: function(uid, name) {
        var tree = Ext.getCmp('deviceDetailNav').treepanel,
            sm = tree.getSelectionModel(),
            compsNode = tree.getRootNode().findChildBy(function(n){
                return n.text=='Components';
            });
    
        var compType = Zenoss.types.type(uid);
        var componentCard = Ext.getCmp('component_card');
        componentCard.setContext(compsNode.id, compType);
        componentCard.selectByToken(uid);
        sm.suspendEvents();
        compsNode.findChildBy(function(n){return n.id==compType;}).select();
        sm.resumeEvents();
    }
});

/*
 * App ComponentGridPanel
 */
ZC.CloudFoundryAppPanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'entity',
            componentType: 'CloudFoundryApp',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'entity'},
                {name: 'cfFramework'},
                {name: 'cfRuntime'},
                {name: 'cfAppServer'},
                {name: 'cfState'},
                {name: 'instances'},
                {name: 'resourcesMemory'},
                {name: 'resourcesDisk'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Name'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this
            },{
                id: 'cfFramework',
                dataIndex: 'cfFramework',
                header: _t('Framework'),
                renderer: Zenoss.render.entityLinkFromGrid,
                width: 70
            },{
                id: 'cfRuntime',
                dataIndex: 'cfRuntime',
                header: _t('Runtime'),
                renderer: Zenoss.render.entityLinkFromGrid,
                width: 70
            },{
                id: 'cfState',
                dataIndex: 'cfState',
                header: _t('State'),
                sortable: true,
                width: 70
            },{
                id: 'resourcesMemory',
                dataIndex: 'resourcesMemory',
                header: _t('Memory'),
                sortable: true,
                width: 60
            },{
                id: 'resourcesDisk',
                dataIndex: 'resourcesDisk',
                header: _t('Disk'),
                sortable: true,
                width: 60
            },{
                id: 'instances',
                dataIndex: 'instances',
                header: _t('Instances'),
                width: 60
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundryAppPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundryAppPanel', ZC.CloudFoundryAppPanel);

/*
 * AppInstance ComponentGridPanel
 */
ZC.CloudFoundryAppInstancePanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'cfApp',
            componentType: 'CloudFoundryAppInstance',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'cfApp'},
                {name: 'entity'},
                {name: 'cfHost'},
                {name: 'cfPort'},
                {name: 'cfCores'},
                {name: 'cfState'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'cfApp',
                dataIndex: 'cfApp',
                header: _t('App'),
                renderer: Zenoss.render.entityLinkFromGrid
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Index'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this,
                width: 45
            },{
                id: 'cfHost',
                dataIndex: 'cfHost',
                header: _t('Host'),
                sortable: true,
                width: 75
            },{
                id: 'cfPort',
                dataIndex: 'cfPort',
                header: _t('Port'),
                sortable: true,
                width: 50
            },{
                id: 'cfCores',
                dataIndex: 'cfCores',
                header: _t('Cores'),
                sortable: true,
                width: 45
            },{
                id: 'cfState',
                dataIndex: 'cfState',
                header: _t('State'),
                sortable: true,
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundryAppInstancePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundryAppInstancePanel', ZC.CloudFoundryAppInstancePanel);

/*
 * Framework ComponentGridPanel
 */
ZC.CloudFoundryFrameworkPanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'cfDetection',
            componentType: 'CloudFoundryFramework',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'entity'},
                {name: 'cfDetection'},
                {name: 'cfRuntimeCount'},
                {name: 'cfAppServerCount'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Name'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this,
                width: 100
            },{
                id: 'cfDetection',
                dataIndex: 'cfDetection',
                header: _t('Detection'),
                sortable: true
            },{
                id: 'cfRuntimeCount',
                dataIndex: 'cfRuntimeCount',
                header: _t('# Runtimes'),
                sortable: true,
                width: 70
            },{
                id: 'cfAppServers',
                dataIndex: 'cfAppServerCount',
                header: _t('# App Servers'),
                sortable: true,
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundryFrameworkPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundryFrameworkPanel', ZC.CloudFoundryFrameworkPanel);

/*
 * Runtime ComponentGridPanel
 */
ZC.CloudFoundryRuntimePanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'entity',
            componentType: 'CloudFoundryRuntime',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'cfFramework'},
                {name: 'entity'},
                {name: 'cfDescription'},
                {name: 'cfVersion'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'cfFramework',
                dataIndex: 'cfFramework',
                header: _t('Framework'),
                renderer: Zenoss.render.entityLinkFromGrid
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Name'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this
            },{
                id: 'cfDescription',
                dataIndex: 'cfDescription',
                header: _t('Description'),
                sortable: true
            },{
                id: 'cfVersion',
                dataIndex: 'cfVersion',
                header: _t('Version'),
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundryRuntimePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundryRuntimePanel', ZC.CloudFoundryRuntimePanel);

/*
 * AppServer ComponentGridPanel
 */
ZC.CloudFoundryAppServerPanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'entity',
            componentType: 'CloudFoundryAppServer',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'cfFramework'},
                {name: 'entity'},
                {name: 'cfDescription'},
                {name: 'cfVersion'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'cfFramework',
                dataIndex: 'cfFramework',
                header: _t('Framework'),
                renderer: Zenoss.render.entityLinkFromGrid
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Name'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this
            },{
                id: 'cfDescription',
                dataIndex: 'cfDescription',
                header: _t('Description'),
                sortable: true
            },{
                id: 'cfVersion',
                dataIndex: 'cfVersion',
                header: _t('Version'),
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundryAppServerPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundryAppServerPanel', ZC.CloudFoundryAppServerPanel);

/*
 * SystemService ComponentGridPanel
 */
ZC.CloudFoundrySystemServicePanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'cfDescription',
            componentType: 'CloudFoundrySystemService',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'cfId'},
                {name: 'entity'},
                {name: 'cfDescription'},
                {name: 'cfVersion'},
                {name: 'cfVendor'},
                {name: 'cfType'},
                {name: 'cfTiers'},
                {name: 'cfProvisionedCount'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'cfId',
                dataIndex: 'cfId',
                header: _t('ID'),
                sortable: true,
                width: 30
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Name'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this,
                width: 100
            },{
                id: 'cfDescription',
                dataIndex: 'cfDescription',
                header: _t('Description'),
                sortable: true
            },{
                id: 'cfVersion',
                dataIndex: 'cfVersion',
                header: _t('Version'),
                sortable: true,
                width: 50
            },{
                id: 'cfVendor',
                dataIndex: 'cfVendor',
                header: _t('Vendor'),
                sortable: true,
                width: 70
            },{
                id: 'cfType',
                dataIndex: 'cfType',
                header: _t('Type'),
                sortable: true,
                width: 70
            },{
                id: 'cfTiers',
                dataIndex: 'cfTiers',
                header: _t('Tiers'),
                sortable: true,
                width: 70
            },{
                id: 'cfProvisionedCount',
                dataIndex: 'cfProvisionedCount',
                header: _t('# Provisioned'),
                sortable: true,
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundrySystemServicePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundrySystemServicePanel', ZC.CloudFoundrySystemServicePanel);

/*
 * ProvisionedService ComponentGridPanel
 */
ZC.CloudFoundryProvisionedServicePanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'entity',
            componentType: 'CloudFoundryProvisionedService',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'cfSystemService'},
                {name: 'entity'},
                {name: 'cfVersion'},
                {name: 'cfVendor'},
                {name: 'cfType'},
                {name: 'cfTier'},
                {name: 'monitor'},
                {name: 'monitored'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'cfSystemService',
                dataIndex: 'cfSystemService',
                header: _t('System Service'),
                renderer: Zenoss.render.entityLinkFromGrid,
                width: 95
            },{
                id: 'entity',
                dataIndex: 'entity',
                header: _t('Name'),
                renderer: Zenoss.render.entityLinkFromGrid,
                panel: this
            },{
                id: 'cfVersion',
                dataIndex: 'cfVersion',
                header: _t('Version'),
                sortable: true,
                width: 50
            },{
                id: 'cfVendor',
                dataIndex: 'cfVendor',
                header: _t('Vendor'),
                sortable: true,
                width: 70
            },{
                id: 'cfType',
                dataIndex: 'cfType',
                header: _t('Type'),
                sortable: true,
                width: 70
            },{
                id: 'cfTier',
                dataIndex: 'cfTier',
                header: _t('Tier'),
                sortable: true,
                width: 70
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            }]
        });
        ZC.CloudFoundryProvisionedServicePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CloudFoundryProvisionedServicePanel', ZC.CloudFoundryProvisionedServicePanel);

/*
 * Custom Component Views
 */
Zenoss.nav.appendTo('Component', [{
    id: 'component_cf_runtimes',
    text: _t('Runtimes'),
    xtype: 'CloudFoundryRuntimePanel',
    subComponentGridPanel: true,
    filterNav: function(navpanel) {
        if (navpanel.refOwner.componentType == 'CloudFoundryFramework') {
            return true;
        } else {
            return false;
        }
    },
    setContext: function(uid) {
        ZC.CloudFoundryRuntimePanel.superclass.setContext.apply(this, [uid]);
    }
}]);

Zenoss.nav.appendTo('Component', [{
    id: 'component_cf_appservers',
    text: _t('App Servers'),
    xtype: 'CloudFoundryAppServerPanel',
    subComponentGridPanel: true,
    filterNav: function(navpanel) {
        if (navpanel.refOwner.componentType == 'CloudFoundryFramework') {
            return true;
        } else {
            return false;
        }
    },
    setContext: function(uid) {
        ZC.CloudFoundryAppServerPanel.superclass.setContext.apply(this, [uid]);
    }
}]);

Zenoss.nav.appendTo('Component', [{
    id: 'component_cf_appinstances',
    text: _t('Instances'),
    xtype: 'CloudFoundryAppInstancePanel',
    subComponentGridPanel: true,
    filterNav: function(navpanel) {
        if (navpanel.refOwner.componentType == 'CloudFoundryApp') {
            return true;
        } else {
            return false;
        }
    },
    setContext: function(uid) {
        ZC.CloudFoundryAppInstancePanel.superclass.setContext.apply(this, [uid]);
    }
}]);

})();

