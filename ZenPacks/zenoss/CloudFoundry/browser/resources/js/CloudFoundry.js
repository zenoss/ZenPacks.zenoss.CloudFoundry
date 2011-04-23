(function(){

var addCloudFoundry = new Zenoss.Action({
    text: _t('Add CloudFoundry Endpoint') + '...',
    id: 'addcloudfoundry-item',
    permission: 'Manage DMD',
    handler: function(btn, e){
        var win = new Zenoss.dialog.CloseDialog({
            width: 300,
            title: _t('Add CloudFoundry Endpoint'),
            items: [{
                xtype: 'form',
                buttonAlign: 'left',
                monitorValid: true,
                labelAlign: 'top',
                footerStyle: 'padding-left: 0',
                border: false,
                items: [{
                    xtype: 'textfield',
                    name: 'target',
                    fieldLabel: _t('Target'),
                    id: "cloudfoundryTargetField",
                    width: 200,
                    allowBlank: false
                }, {
                    xtype: 'textfield',
                    name: 'email',
                    fieldLabel: _t('Email (Username)'),
                    id: "cloudfoundryEmailField",
                    width: 200,
                    allowBlank: false
                }, {
                    xtype: 'textfield',
                    name: 'password',
                    inputType: 'password',
                    fieldLabel: _t('Password'),
                    id: "cloudfoundryPasswordField",
                    width: 200,
                    allowBlank: false
                }/*, {
                    // TODO: enable use of different collectors
                    disabled: true,
                    xtype: 'combo',
                    width: 160,
                    name: 'collector',
                    fieldLabel: _t('Collector'),
                    id: 'cellCollector',
                    mode: 'local',
                    store: new Ext.data.ArrayStore({
                        data: Zenoss.env.COLLECTORS,
                        fields: ['name']
                    }),
                    valueField: 'name',
                    displayField: 'name',
                    forceSelection: true,
                    editable: false,
                    allowBlank: false,
                    triggerAction: 'all',
                    selectOnFocus: true,
                    listeners: {
                        'afterrender': function(component) {
                            var index = component.store.find('name', 'localhost');
                            if (index >= 0) {
                                component.setValue('localhost');
                            }
                        }
                    }
                }*/],
                buttons: [{
                    xtype: 'DialogButton',
                    id: 'addCloudFoundrydevice-submit',
                    text: _t('Add'),
                    formBind: true,
                    handler: function(b) {
                        var form = b.ownerCt.ownerCt.getForm();
                        var opts = form.getFieldValues();
                        
                        Zenoss.remote.CloudFoundryRouter.addEndpoint(opts,
                        function(response) {
                            if (response.success) {
                                new Zenoss.dialog.SimpleMessageDialog({
                                    message: _t('Add CloudFoundry Endpoint job submitted.'),
                                    buttons: [{
                                        xtype: 'DialogButton',
                                        text: _t('OK')
                                    }, {
                                        xtype: 'button',
                                        text: _t('View Job Log'),
                                        handler: function() {
                                            window.location =
                                                '/zport/dmd/JobManager/jobs/' +
                                                response.jobId + '/viewlog';
                                        }
                                    }]
                                }).show();
                            }
                            else {
                                new Zenoss.dialog.SimpleMessageDialog({
                                    message: response.msg,
                                    buttons: [{
                                        xtype: 'DialogButton',
                                        text: _t('OK')
                                    }]
                                }).show();
                            }
                        });
                    }
                }, Zenoss.dialog.CANCEL]
            }]
        });
        win.show();
    }
});

// Push the addCloudFoundry action to the adddevice button
Ext.ns('Zenoss.extensions');
Zenoss.extensions.adddevice = Zenoss.extensions.adddevice instanceof Array ?
                              Zenoss.extensions.adddevice : [];
Zenoss.extensions.adddevice.push(addCloudFoundry);

}());

