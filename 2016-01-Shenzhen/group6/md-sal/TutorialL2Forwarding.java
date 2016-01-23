/*
 * Copyright (C) 2015 SDN Hub

 Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3.
 You may not use this file except in compliance with this License.
 You may obtain a copy of the License at

    http://www.gnu.org/licenses/gpl-3.0.txt

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 implied.

 *
 */

package org.sdnhub.odl.tutorial.learningswitch.impl;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.nio.channels.SocketChannel;
import java.nio.charset.Charset;
import java.net.InetSocketAddress;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.sal.binding.api.NotificationProviderService;
import org.opendaylight.controller.sal.binding.api.RpcProviderRegistry;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev100924.MacAddress;
import org.opendaylight.yang.gen.v1.urn.opendaylight.action.types.rev131112.action.list.Action;
import org.opendaylight.yang.gen.v1.urn.opendaylight.action.types.rev131112.action.action.OutputActionCaseBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.action.types.rev131112.action.action.output.action._case.OutputActionBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.action.types.rev131112.action.list.ActionBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.action.types.rev131112.action.list.ActionKey;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.FlowCapableNode;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.FlowId;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.tables.Table;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.tables.TableKey;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.tables.table.Flow;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.tables.table.FlowBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.inventory.rev130819.tables.table.FlowKey;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.flow.InstructionsBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.flow.MatchBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.instruction.instruction.ApplyActionsCaseBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.instruction.instruction.apply.actions._case.ApplyActionsBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.instruction.list.Instruction;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.instruction.list.InstructionBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.flow.types.rev131026.instruction.list.InstructionKey;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.NodeConnectorId;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.NodeConnectorRef;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.NodeId;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.NodeRef;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.Nodes;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.nodes.Node;
import org.opendaylight.yang.gen.v1.urn.opendaylight.inventory.rev130819.nodes.NodeKey;
import org.opendaylight.yang.gen.v1.urn.opendaylight.packet.service.rev130709.PacketProcessingListener;
import org.opendaylight.yang.gen.v1.urn.opendaylight.packet.service.rev130709.PacketProcessingService;
import org.opendaylight.yang.gen.v1.urn.opendaylight.packet.service.rev130709.PacketReceived;
import org.opendaylight.yang.gen.v1.urn.opendaylight.packet.service.rev130709.TransmitPacketInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.packet.service.rev130709.TransmitPacketInputBuilder;
import org.opendaylight.yangtools.concepts.Registration;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.sdnhub.odl.tutorial.utils.GenericTransactionUtils;
import org.sdnhub.odl.tutorial.utils.PacketParsingUtils;
import org.sdnhub.odl.tutorial.utils.inventory.InventoryUtils;
import org.sdnhub.odl.tutorial.utils.openflow13.MatchUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Preconditions;
import com.google.common.collect.Lists;



class GDBPacketParsingUtils {
	private static final int IP_SRC_START_POSITION = 26;
	private static final int IP_SRC_END_POSITION = 30;
	private static final int IP_DST_START_POSITION = 30;
	private static final int IP_DST_END_POSITION = 34;

	private static final int IP_PROTOCOL_START_POSITION = 23;


	private static final int DEST_PORT_START_POSITION = 36;
	private static final int DEST_PORT_END_POSITION = 38;



	private GDBPacketParsingUtils() {
		//prohibite to instantiate this class
	}
	public static int extractDestPort(final byte[] payload) {
		return 0xffff & ByteBuffer.wrap(Arrays.copyOfRange(payload,  DEST_PORT_START_POSITION  , DEST_PORT_END_POSITION )).getShort();
	}

	public static byte extractIPprotocol(final byte[] payload) {
		return payload[IP_PROTOCOL_START_POSITION];
	}

	public static byte[] extractSrcIP(final byte[] payload) {
		return Arrays.copyOfRange(payload,  IP_SRC_START_POSITION , IP_SRC_END_POSITION);
	}

	public static byte[] extractDstIP(final byte[] payload) {
		return Arrays.copyOfRange(payload, IP_DST_START_POSITION, IP_DST_END_POSITION);
	}

	public static String rawIpToString(final byte[] rawIp) {
		if (rawIp.length != 4)
			return "";
		StringBuilder sb = new StringBuilder();
		for (byte octet : rawIp) {
			sb.append(String.format("%d.", octet));
		}
		return sb.substring(0, sb.length()-1);
	}

}




public class TutorialL2Forwarding  implements AutoCloseable, PacketProcessingListener {
	private final Logger LOG = LoggerFactory.getLogger(this.getClass());
	private final static long FLOOD_PORT_NUMBER = 0xfffffffbL;


	//Members related to MD-SAL operations
	private List<Registration> registrations;
	private DataBroker dataBroker;
	private PacketProcessingService packetProcessingService;


	private String REMOTEIP = "10.1.0.202";

//	curl -X POST -H "Content-Type: application/json"
	//-d '{"packetin":{"src_mac":"3E:EB:72:7B:61:95","src_ip":"10.0.0.1", "dst_mac": "111", "dst_ip": ""}}'
	//http://127.0.0.1:8000/packetin
	private void send(String srcIp, String srcMac, String dstIp, String dstMac, String protocol, int port) throws IOException {
		String head = "curl -X POST -H 'Content-Type: application/jsoo' ";
		String content = "-d  "
				+ srcMac + ","
				+ srcIp + ","
				+ dstMac + ","
				+ dstIp + ","
				+ protocol + ","
				+ port;
		String address = "  http://"
				+ REMOTEIP
				+ ":8000/packetin";

		StringBuilder sb = new StringBuilder();
		sb.append(head);
		sb.append(content);
		sb.append(address);
		LOG.error(sb.toString());

		Runtime.getRuntime().exec(sb.toString());
	}

	public TutorialL2Forwarding(DataBroker dataBroker, NotificationProviderService notificationService, RpcProviderRegistry rpcProviderRegistry) {
		//Store the data broker for reading/writing from inventory store
		this.dataBroker = dataBroker;

		//Get access to the packet processing service for making RPC calls later
		this.packetProcessingService = rpcProviderRegistry.getRpcService(PacketProcessingService.class);

		//List used to track notification (both data change and YANG-defined) listener registrations
		this.registrations = Lists.newArrayList();

		//Register this object for receiving notifications when there are PACKET_INs
		registrations.add(notificationService.registerNotificationListener(this));
	}

	@Override
	public void close() throws Exception {
		for (Registration registration : registrations) {
			registration.close();
		}
		registrations.clear();
	}



	@Override
	public void onPacketReceived(PacketReceived notification) {
		LOG.trace("Received packet notification {}", notification.getMatch());

		NodeConnectorRef ingressNodeConnectorRef = notification.getIngress();
		NodeRef ingressNodeRef = InventoryUtils.getNodeRef(ingressNodeConnectorRef);
		NodeConnectorId ingressNodeConnectorId = InventoryUtils.getNodeConnectorId(ingressNodeConnectorRef);
		NodeId ingressNodeId = InventoryUtils.getNodeId(ingressNodeConnectorRef);

		NodeConnectorId floodNodeConnectorId = InventoryUtils.getNodeConnectorId(ingressNodeId, FLOOD_PORT_NUMBER);
		NodeConnectorRef floodNodeConnectorRef = InventoryUtils.getNodeConnectorRef(floodNodeConnectorId);

		byte[] payload = notification.getPayload();

		byte[] etherTypeRaw = PacketParsingUtils.extractEtherType(notification.getPayload());
		int etherType = (0x0000ffff & ByteBuffer.wrap(etherTypeRaw).getShort());
		if (etherType != 0x0800) {
			packetOut(ingressNodeRef, floodNodeConnectorRef, payload);
			return;
		}


		byte[] srcMacRaw = PacketParsingUtils.extractSrcMac(payload);
		String srcMac = PacketParsingUtils.rawMacToString(srcMacRaw);
		byte[] dstMacRaw = PacketParsingUtils.extractDstMac(payload);
		String dstMac = PacketParsingUtils.rawMacToString(dstMacRaw);

		byte[] srcIpRaw = GDBPacketParsingUtils.extractSrcIP(payload);
		String srcIp = GDBPacketParsingUtils.rawIpToString(srcIpRaw);
		byte[] dstIpRaw = GDBPacketParsingUtils.extractDstIP(payload);
		String dstIp = GDBPacketParsingUtils.rawIpToString(dstIpRaw);

		String protocol;
		byte p = GDBPacketParsingUtils.extractIPprotocol(payload);
		if (p == 0x11)
			protocol = "UDP";
		else
			protocol = "TCP";

		int port = GDBPacketParsingUtils.extractDestPort(payload);
		try {
			this.send(srcIp, srcMac, dstIp, dstMac, protocol, port);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		//packetOut(ingressNodeRef, floodNodeConnectorRef, payload);
	}



	private void packetOut(NodeRef egressNodeRef, NodeConnectorRef egressNodeConnectorRef, byte[] payload) {
		Preconditions.checkNotNull(packetProcessingService);
		LOG.debug("Flooding packet of size {} out of port {}", payload.length, egressNodeConnectorRef);

		//Construct input for RPC call to packet processing service
		TransmitPacketInput input = new TransmitPacketInputBuilder()
				.setPayload(payload)
				.setNode(egressNodeRef)
				.setEgress(egressNodeConnectorRef)
				.build();
		packetProcessingService.transmitPacket(input);
	}

	private void programL2Flow(NodeId nodeId, String dstMac, NodeConnectorId ingressNodeConnectorId, NodeConnectorId egressNodeConnectorId) {

		/* Programming a flow involves:
		 * 1. Creating a Flow object that has a match and a list of instructions,
		 * 2. Adding Flow object as an augmentation to the Node object in the inventory.
		 * 3. FlowProgrammer module of OpenFlowPlugin will pick up this data change and eventually program the switch.
		 */

		//Creating match object
		MatchBuilder matchBuilder = new MatchBuilder();
		
	}
}
