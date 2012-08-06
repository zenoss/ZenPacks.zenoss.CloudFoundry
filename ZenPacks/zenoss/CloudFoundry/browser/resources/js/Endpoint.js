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
ZC.registerName('CloudFoundryApp', _t('App'), _t('Apps'));
ZC.registerName('CloudFoundryAppInstance', _t('App Instance'), _t('App Instances'));
ZC.registerName('CloudFoundryFramework', _t('Framework'), _t('Frameworks'));
ZC.registerName('CloudFoundryRuntime', _t('Runtime'), _t('Runtimes'));
ZC.registerName('CloudFoundryAppServer', _t('App Server'), _t('App Servers'));
ZC.registerName('CloudFoundrySystemService', _t('System Service'), _t('System Services'));
ZC.registerName('CloudFoundryProvisionedService', _t('Provisioned Service'), _t('Provisioned Services'));

/*
 * Endpoint-local custom renderers.
 */
Ext.apply(Zenoss.render, {
    CloudFoundry_entityLinkFromGrid: function(obj, col, record) {
        if (!obj)
            return;

        if (typeof(obj) == 'string')
            obj = record.data;

        if (!obj.title && obj.name)
            obj.title = obj.name;

        var isLink = false;

        if (this.refName == 'componentgrid') {
            // Zenoss >= 4.2 / ExtJS4
            if (this.subComponentGridPanel || this.componentType != obj.meta_type)
                isLink = true;
        } else {
            // Zenoss < 4.2 / ExtJS3
            if (!this.panel || this.panel.subComponentGridPanel)
                isLink = true;
        }

        if (isLink) {
            return '<a href="javascript:Ext.getCmp(\'component_card\').componentgrid.jumpToEntity(\''+obj.uid+'\', \''+obj.meta_type+'\');">'+obj.title+'</a>';
        } else {
            return obj.title;
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

    jumpToEntity: function(uid, meta_type) {
        var tree = Ext.getCmp('deviceDetailNav').treepanel;
        var tree_selection_model = tree.getSelectionModel();
        var components_node = tree.getRootNode().findChildBy(
            function(n) {
                if (n.data) {
                    // Zenoss >= 4.2 / ExtJS4
                    return n.data.text == 'Components';
                }

                // Zenoss < 4.2 / ExtJS3
                return n.text == 'Components';
            });

        // Reset context of component card.
        var component_card = Ext.getCmp('component_card');

        if (components_node.data) {
            // Zenoss >= 4.2 / ExtJS4
            component_card.setContext(components_node.data.id, meta_type);
        } else {
            // Zenoss < 4.2 / ExtJS3
            component_card.setContext(components_node.id, meta_type);
        }

        // Select chosen row in component grid.
        component_card.selectByToken(uid);

        // Select chosen component type from tree.
        var component_type_node = components_node.findChildBy(
            function(n) {
                if (n.data) {
                    // Zenoss >= 4.2 / ExtJS4
                    return n.data.id == meta_type;
                }

                // Zenoss < 4.2 / ExtJS3
                return n.id == meta_type;
            });

        if (component_type_node.select) {
            tree_selection_model.suspendEvents();
            component_type_node.select();
            tree_selection_model.resumeEvents();
        } else {
            tree_selection_model.select([component_type_node], false, true);
        }
    }
});

/*
 * App ComponentGridPanel
 */
ZC.CloudFoundryAppPanel = Ext.extend(ZC.CloudFoundryComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'CloudFoundryApp',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'severity'},
                {name: 'cfFramework'},
                {name: 'cfRuntime'},
                {name: 'cfAppServer'},
                {name: 'cfState'},
                {name: 'instances'},
                {name: 'resourcesMemory'},
                {name: 'resourcesDisk'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
                panel: this
            },{
                id: 'cfFramework',
                dataIndex: 'cfFramework',
                header: _t('Framework'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
                width: 70
            },{
                id: 'cfRuntime',
                dataIndex: 'cfRuntime',
                header: _t('Runtime'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
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
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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
                {name: 'meta_type'},
                {name: 'severity'},
                {name: 'cfApp'},
                {name: 'cfState'},
                {name: 'utilCPU'},
                {name: 'utilMemory'},
                {name: 'utilDisk'},
                {name: 'cfHost'},
                {name: 'cfPort'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'}
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
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Index'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
                panel: this,
                width: 45
            },{
                id: 'cfState',
                dataIndex: 'cfState',
                header: _t('State'),
                sortable: true,
                width: 80
            },{
                id: 'utilCPU',
                dataIndex: 'utilCPU',
                header: _t('CPU'),
                width: 70
            },{
                id: 'utilMemory',
                dataIndex: 'utilMemory',
                header: _t('Memory'),
                width: 145
            },{
                id: 'utilDisk',
                dataIndex: 'utilDisk',
                header: _t('Disk'),
                width: 145
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
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 65
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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
                {name: 'meta_type'},
                {name: 'cfDetection'},
                {name: 'cfRuntimeCount'},
                {name: 'cfAppServerCount'},
                {name: 'cfAppCount'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
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
                id: 'cfAppServerCount',
                dataIndex: 'cfAppServerCount',
                header: _t('# App Servers'),
                sortable: true,
                width: 80
            },{
                id: 'cfAppCount',
                dataIndex: 'cfAppCount',
                header: _t('# Apps'),
                sortable: true,
                width: 50
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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
            autoExpandColumn: 'name',
            componentType: 'CloudFoundryRuntime',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'cfFramework'},
                {name: 'cfDescription'},
                {name: 'cfVersion'},
                {name: 'cfAppCount'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'cfFramework',
                dataIndex: 'cfFramework',
                header: _t('Framework'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
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
                id: 'cfAppCount',
                dataIndex: 'cfAppCount',
                header: _t('# Apps'),
                sortable: true,
                width: 50
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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
            autoExpandColumn: 'name',
            componentType: 'CloudFoundryAppServer',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'cfFramework'},
                {name: 'cfDescription'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'cfFramework',
                dataIndex: 'cfFramework',
                header: _t('Framework'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
                panel: this
            },{
                id: 'cfDescription',
                dataIndex: 'cfDescription',
                header: _t('Description'),
                sortable: true
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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
                {name: 'meta_type'},
                {name: 'cfId'},
                {name: 'cfDescription'},
                {name: 'cfVersion'},
                {name: 'cfVendor'},
                {name: 'cfType'},
                {name: 'cfTiers'},
                {name: 'cfProvisionedCount'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'cfId',
                dataIndex: 'cfId',
                header: _t('ID'),
                sortable: true,
                width: 30
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
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
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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
            autoExpandColumn: 'name',
            componentType: 'CloudFoundryProvisionedService',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'cfSystemService'},
                {name: 'cfVersion'},
                {name: 'cfVendor'},
                {name: 'cfType'},
                {name: 'cfTier'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'cfSystemService',
                dataIndex: 'cfSystemService',
                header: _t('System Service'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
                width: 95
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.CloudFoundry_entityLinkFromGrid,
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
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
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

