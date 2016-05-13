/*
 * Cisco Systems, Inc. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.hack.impl;

import org.opendaylight.controller.sal.binding.api.BindingAwareBroker.ProviderContext;
import org.opendaylight.controller.sal.binding.api.BindingAwareBroker.RpcRegistration;
import org.opendaylight.controller.sal.binding.api.BindingAwareProvider;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hack.rev150105.HackService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HackProvider implements BindingAwareProvider, AutoCloseable {

    private static final Logger LOG = LoggerFactory.getLogger(HackProvider.class);
    private RpcRegistration<HackService> hackService;

    @Override
    public void onSessionInitiated(ProviderContext session) {
        LOG.info("HackProvider Session Initiated");
        hackService=session.addRpcImplementation(HackService.class, new HackImpl());
    }

    @Override
    public void close() throws Exception {
        LOG.info("HackProvider Closed");
        if(hackService!=null)
        	hackService.close();
    }

}
