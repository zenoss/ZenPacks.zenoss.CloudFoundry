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
            fieldLabel: _t('App URIs (Usage / Limit)')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilApps',
            fieldLabel: _t('Apps (Usage / Limit)')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilMemory',
            fieldLabel: _t('Memory (Usage / Limit)')
        });

        box.addField({
            xtype: 'displayfield',
            name: 'utilServices',
            fieldLabel: _t('Services (Usage / Limit)')
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
 * Cell-local custom renderers.
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
            autoExpandColumn: 'cfName',
            componentType: 'CloudFoundryApp',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'cfName'},
                {name: 'cfVersion'},
                {name: 'cfState'},
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
                id: 'cfName',
                dataIndex: 'cfName',
                header: _t('Name'),
                sortable: true
            },{
                id: 'cfVersion',
                dataIndex: 'cfVersion',
                header: _t('Version'),
                sortable: true,
                width: 265
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

})();

