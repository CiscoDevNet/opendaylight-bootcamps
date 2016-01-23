/*
 * Copyright (c) 2016 team NO.2 of 2nd ODL-BootCamp China and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
 
package aaas.impl;

import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.Uri;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.TopologyId;


public class AaasConstants {
	
	/*public static final ImmutableBiMap<String,IpAddress> ROUTERS_INFO
    = new ImmutableBiMap.Builder<String,IpAddress>()
        .put("iosxrv-1",new IpAddress(new Ipv4Address("198.18.1.30")))
        .put("iosxrv-2",new IpAddress(new Ipv4Address("198.18.1.31")))
        .put("iosxrv-3",new IpAddress(new Ipv4Address("198.18.1.32")))
        .put("iosxrv-4",new IpAddress(new Ipv4Address("198.18.1.33")))
        .put("iosxrv-5",new IpAddress(new Ipv4Address("198.18.1.34")))
        .put("iosxrv-6",new IpAddress(new Ipv4Address("198.18.1.35")))
        .put("iosxrv-7",new IpAddress(new Ipv4Address("198.18.1.36")))
        .put("iosxrv-8",new IpAddress(new Ipv4Address("198.18.1.37")))
        .build();*/
	public static final TopologyId NETCONF_TOPOLOGY_ID = new TopologyId(new Uri("topology-netconf"));
	

}