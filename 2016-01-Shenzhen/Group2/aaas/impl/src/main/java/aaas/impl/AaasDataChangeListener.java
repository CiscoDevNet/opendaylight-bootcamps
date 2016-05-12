/*
 * Copyright (c) 2016 team NO.2 of 2nd ODL-BootCamp China and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package aaas.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.opendaylight.controller.md.sal.common.api.data.AsyncDataChangeEvent;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.common.api.data.TransactionCommitFailedException;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.Ipv4AclAndPrefixList;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.DestinationNetwork;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.DestinationNetworkBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.DestinationPort;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.DestinationPortBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.SourceNetwork;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.SourceNetworkBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.SourcePort;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.ace.SourcePortBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.Accesses;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.AccessesBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.Access;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.AccessBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.AccessKey;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.access.AccessListEntries;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.access.AccessListEntriesBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.access.access.list.entries.AccessListEntry;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.access.access.list.entries.AccessListEntryBuilder;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.cfg.rev150107.ipv4.acl.and.prefix.list.accesses.access.access.list.entries.AccessListEntryKey;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.datatypes.rev150107.Ipv4AclGrantEnum;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.datatypes.rev150107.Ipv4AclPortNumber;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.datatypes.rev150107.Ipv4AclPortNumber.Enumeration;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.datatypes.rev150107.Ipv4AclProtocolNumber;
import org.opendaylight.yang.gen.v1.http.cisco.com.ns.yang.cisco.ios.xr.ipv4.acl.datatypes.rev150107.Ipv4AclSequenceNumberRange;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.IpAddress;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev130715.Ipv4Address;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev130715.Uuid;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.aaas.rev160121.AclEntries;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.aaas.rev160121.acl.entries.AclEntry;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NetworkTopology;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.TopologyId;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.network.topology.Topology;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.network.topology.TopologyKey;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.network.topology.topology.Node;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.network.topology.topology.NodeKey;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.DataChangeListener;
import org.opendaylight.controller.md.sal.binding.api.MountPoint;
import org.opendaylight.controller.md.sal.binding.api.MountPointService;
import org.opendaylight.controller.md.sal.binding.api.WriteTransaction;
import org.opendaylight.controller.md.sal.common.api.data.AsyncDataBroker.DataChangeScope;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Optional;

public class AaasDataChangeListener implements DataChangeListener, AutoCloseable {
    private static final Logger LOG = LoggerFactory.getLogger(AaasDataChangeListener.class);
    private DataBroker db;
    private ListenerRegistration<DataChangeListener> registration;
    public static final InstanceIdentifier<AclEntries> AAAS_IID = InstanceIdentifier.builder(AclEntries.class).build();

    public static final InstanceIdentifier<NetworkTopology> TOPOLOGY = InstanceIdentifier.builder(NetworkTopology.class).build();
    public static final InstanceIdentifier<Topology> NETCONF_TOPO_IID =
            InstanceIdentifier
            .create(NetworkTopology.class)
            .child(Topology.class,
                   new TopologyKey(new TopologyId("topology-netconf")));
    private MountPointService mountService;

    public List<String> routers = new ArrayList<String>();

    public AaasDataChangeListener(DataBroker db, MountPointService mountService) {
        this.db = db;
        this.mountService = mountService;
        routers.add("iosxrv-1");
        routers.add("iosxrv-2");
        routers.add("iosxrv-3");
        routers.add("iosxrv-4");
        routers.add("iosxrv-5");
        routers.add("iosxrv-6");
        routers.add("iosxrv-7");
        routers.add("iosxrv-8");
        // Register the DataChangeListener for Toaster's configuration subtree
        registration = db.registerDataChangeListener(LogicalDatastoreType.CONFIGURATION,
                                                AAAS_IID,
                                                this,
                                                DataChangeScope.SUBTREE);
    }

    @Override
    public void onDataChanged(final AsyncDataChangeEvent<InstanceIdentifier<?>, DataObject> change) {
        for (Entry<InstanceIdentifier<?>,
                DataObject> entry : change.getCreatedData().entrySet()) {
            if (entry.getKey().getTargetType() == AclEntry.class) {
                updateAcl(entry.getKey(), entry.getValue());
            }
        }
        for (Entry<InstanceIdentifier<?>,
                DataObject> entry :  change.getUpdatedData().entrySet()) {
            if (entry.getKey().getTargetType() == AclEntry.class) {
                updateAcl(entry.getKey(), entry.getValue());
            }
        }
        for (InstanceIdentifier<?> removedPath : change.getRemovedPaths()) {
            Map<InstanceIdentifier<?>, DataObject> dataOriginalDataObject = change.getOriginalData();
            DataObject dataObject = dataOriginalDataObject.get(removedPath);
            if (removedPath.getTargetType() == AclEntry.class) {
                deleteAcl(removedPath, dataObject);
            }
        }
    }

    private void updateAcl(InstanceIdentifier<?> iid, DataObject dataObject) {
        AclEntry aclEntry = (AclEntry)dataObject;

        for(String nodeId: routers) {
        	writeAcltoDS(nodeId, aclEntry);
        }

        LOG.info("A aaas acl: {} was created or updated", aclEntry);
    }

    private void deleteAcl(InstanceIdentifier<?> iid, DataObject dataObject) {
    	AclEntry aclEntry = (AclEntry)dataObject;

        for(String nodeId: routers) {
        	deletAcltoDS(nodeId, aclEntry);
        }

        LOG.info("A aaas acl: {} was deleted", aclEntry);
    }

	private void deletAcltoDS(String nodeId, AclEntry aclEntry) {
		String aclId = aclEntry.getKey().getEntryUuid();

        final Optional<MountPoint> mountPoint;
        InstanceIdentifier<Node> node_iid = NETCONF_TOPO_IID.child(Node.class, new NodeKey(new NodeId(nodeId)));
        // Get mount point for specified device
		mountPoint = mountService.getMountPoint(node_iid);

		// Get DataBroker API and create a write tx
        final DataBroker dataBroker = mountPoint.get().getService(DataBroker.class).get();
        final ReadWriteTransaction writeTx = dataBroker.newReadWriteTransaction();
        //final WriteTransaction writeTx = dataBroker.newWriteOnlyTransaction();

        InstanceIdentifier<Access> access_iid = InstanceIdentifier
        		.create(Ipv4AclAndPrefixList.class)
        		.child(Accesses.class)
        		.child(Access.class, new AccessKey(aclId));

        writeTx.delete(LogicalDatastoreType.CONFIGURATION, access_iid);

	}

	@Override
	public void close() throws Exception {
		// TODO Auto-generated method stub

	}

	public void writeAcltoDS(String nodeId, AclEntry aclEntry) {
		String aclId = aclEntry.getKey().getEntryUuid();
        IpAddress srcIp = new IpAddress(new Ipv4Address(aclEntry.getSourceNetwork().getSourceIp()));
        IpAddress srcMask = new IpAddress(new Ipv4Address(aclEntry.getSourceNetwork().getSourceNetmask()));
        Long srcPortNum = aclEntry.getSourcePort();
        IpAddress dstIp = new IpAddress(new Ipv4Address(aclEntry.getDestinationNetwork().getDestinationIp()));
        IpAddress dstMask = new IpAddress(new Ipv4Address(aclEntry.getDestinationNetwork().getDestinationNetmask()));
        Long dstPortNum = aclEntry.getDestinationPort();
        String protocol = aclEntry.getProtocol();
        String action = aclEntry.getAction();

		final Optional<MountPoint> mountPoint;
        InstanceIdentifier<Node> node_iid = NETCONF_TOPO_IID.child(Node.class, new NodeKey(new NodeId(nodeId)));
        // Get mount point for specified device
		mountPoint = mountService.getMountPoint(node_iid);

		// Get DataBroker API and create a write tx
        final DataBroker dataBroker = mountPoint.get().getService(DataBroker.class).get();
        final WriteTransaction writeTx = dataBroker.newWriteOnlyTransaction();

        SourceNetwork srcNetwork = new SourceNetworkBuilder()
        		.setSourceAddress(srcIp.getIpv4Address())
        		.setSourceWildCardBits(srcMask.getIpv4Address())
        		.build();
        SourcePort srcPort = new SourcePortBuilder()
        		.setFirstSourcePort(new Ipv4AclPortNumber(srcPortNum))
        		.build();
        DestinationNetwork dstNetwork = new DestinationNetworkBuilder()
        		.setDestinationAddress(dstIp.getIpv4Address())
        		.setDestinationWildCardBits(dstMask.getIpv4Address())
        		.build();
        DestinationPort dstPort = new DestinationPortBuilder()
        		.setFirstDestinationPort(new Ipv4AclPortNumber(dstPortNum))
        		.build();
        Ipv4AclGrantEnum grant;
        if (action.toLowerCase().equals("deny")) {
        	grant = Ipv4AclGrantEnum.Deny;
        } else {
        	grant = Ipv4AclGrantEnum.Permit;
        }
        Long protocolNum;
        if (protocol.toLowerCase().equals("udp")) {
        	protocolNum = (long) 17;
        } else {
        	protocolNum = (long) 6;
        }

        AccessListEntry acl = new AccessListEntryBuilder()
        		.setKey(new AccessListEntryKey(new Ipv4AclSequenceNumberRange((long)10)))
        		.setSourceNetwork(srcNetwork)
        		.setSourcePort(srcPort)
        		.setDestinationNetwork(dstNetwork)
        		.setDestinationPort(dstPort)
        		.setGrant(grant)
        		.setProtocol(new Ipv4AclProtocolNumber(protocolNum))
        		.build();
        List<AccessListEntry> aclList = new ArrayList<AccessListEntry>();
        aclList.add(acl);
        AccessListEntries aclLists = new AccessListEntriesBuilder()
        		.setAccessListEntry(aclList)
        		.build();
        Access access = new AccessBuilder()
        		.setKey(new AccessKey(aclId))
        		.setAccessListName(aclId)
        		.setAccessListEntries(aclLists)
        		.build();
        List<Access> accessList = new ArrayList<Access>();
        accessList.add(access);
        Accesses accesses = new AccessesBuilder()
        		.setAccess(accessList)
        		.build();

        //InstanceIdentifier<Accesses> accesses_iid = InstanceIdentifier
        //		.create(Accesses.class);
                //.builder(Accesses.class)
                //.child(Access.class, new AccessKey(aclId.toString()));

        InstanceIdentifier<Access> access_iid = InstanceIdentifier
        		.create(Ipv4AclAndPrefixList.class)
        		.child(Accesses.class)
        		.child(Access.class, new AccessKey(aclId));



        writeTx.merge(LogicalDatastoreType.CONFIGURATION, access_iid, access);

		        /*InterfaceActive active = new InterfaceActive("act");
		        InterfaceName ifname = new InterfaceName("Loopback0");
		        InterfaceConfigurationKey ifkey = new InterfaceConfigurationKey(active, ifname);

		        InterfaceConfiguration ifconf = new InterfaceConfigurationBuilder()
		        		.setKey(ifkey)
		        		.setDescription("test by zhp")
		        		.build();

		        InstanceIdentifier<InterfaceConfiguration> ifconf_iid = InstanceIdentifier
		                .builder(InterfaceConfigurations.class)
		                .child(InterfaceConfiguration.class, ifkey)
		        		.build();
		        writeTx.merge(LogicalDatastoreType.CONFIGURATION, ifconf_iid, ifconf);*/

        try {
        	writeTx.submit().checkedGet();
        } catch (TransactionCommitFailedException e) {
            LOG.error("{}", e.toString());
        }
	}
}