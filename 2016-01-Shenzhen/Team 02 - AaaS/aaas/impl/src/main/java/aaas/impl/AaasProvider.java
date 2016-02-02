/*
 * Copyright (c) 2016 team NO.2 of 2nd ODL-BootCamp China and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package aaas.impl;

import org.opendaylight.controller.sal.binding.api.BindingAwareBroker.ProviderContext;

import java.util.ArrayList;
import java.util.List;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.MountPointService;
import org.opendaylight.controller.md.sal.binding.api.WriteTransaction;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.sal.binding.api.BindingAwareProvider;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.aaas.rev160121.AclEntries;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.aaas.rev160121.AclEntriesBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.aaas.rev160121.acl.entries.AclEntry;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;

public class AaasProvider implements BindingAwareProvider, AutoCloseable {

    private static final Logger LOG = LoggerFactory.getLogger(AaasProvider.class);
    private DataBroker db;
    private AaasDataChangeListener listener;
    private MountPointService mountService;
    
    public static final InstanceIdentifier<AclEntries> ACL_ENTRIES_IID = InstanceIdentifier.builder(AclEntries.class).build();

    @Override
    public void onSessionInitiated(ProviderContext session) {
        LOG.info("AaasProvider Session Initiated");
        this.db = session.getSALService(DataBroker.class);
        this.mountService = session.getSALService(MountPointService.class);
        listener = new AaasDataChangeListener(db,mountService);
        
        
        
        //Initiate the config and operational datastore
        initConfiguration();
        initOperational();

        LOG.info("onSessionInitiated: AaasProvider initialization done");
    }

    /**************************************************************************
     * AaasProvide Private Methods
     *************************************************************************/

    /**
     * Populates toaster's initial operational data into the MD-SAL operational
     * data store.
     * Note - we are simulating a device whose manufacture and model are fixed
     * (embedded) into the hardware. / This is why the manufacture and model
     * number are hardcoded.
     */
    private void initOperational() {
        // Build the initial operational data
        List<AclEntry> aclList= new ArrayList<AclEntry>();
        AclEntries aclEntries = new AclEntriesBuilder()
        		.setAclEntry(aclList)
                .build();

        // Put the toaster operational data into the MD-SAL data store
        WriteTransaction tx = db.newWriteOnlyTransaction();
        tx.put(LogicalDatastoreType.OPERATIONAL, ACL_ENTRIES_IID, aclEntries);

        // Perform the tx.submit asynchronously
        Futures.addCallback(tx.submit(), new FutureCallback<Void>() {
            @Override
            public void onSuccess(final Void result) {
                LOG.info("initToasterOperational: transaction succeeded");
            }

            @Override
            public void onFailure(final Throwable t) {
                LOG.error("initToasterOperational: transaction failed");
            }
        });

        LOG.info("initToasterOperational: operational status populated: {}", aclEntries);
    }

    /**
     * Populates toaster's default config data into the MD-SAL configuration
     * data store.  Note the database write to the tree are done in a synchronous fashion
     */
    private void initConfiguration() {
        // Build the default config data
        List<AclEntry> aclList= new ArrayList<AclEntry>();
        AclEntries aclEntries = new AclEntriesBuilder().setAclEntry(aclList)
                .build();

        // Place default config data in data store tree
        WriteTransaction tx = db.newWriteOnlyTransaction();
        tx.put(LogicalDatastoreType.CONFIGURATION, ACL_ENTRIES_IID, aclEntries);
        // Perform the tx.submit synchronously
        tx.submit();

        LOG.info("initToasterConfiguration: default config populated: {}", aclEntries);
    }

    /**************************************************************************
     * AutoCloseable Method
     *************************************************************************/
    /**
     * Called when MD-SAL closes the active session. Cleanup is performed, i.e.
     * all active registrations with MD-SAL are closed,
     */
    @Override
    public void close() throws Exception {
        LOG.info("Impl: registrations closed");
    }

}
