package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.caching.mountpoint.impl.rev141210;

import java.util.Collection;
import org.opendaylight.controller.md.sal.dom.api.DOMMountPointService;
import org.opendaylight.controller.sal.core.api.Broker;
import org.opendaylight.controller.sal.core.api.Consumer;

public class CachingMountpointSalCOnsumer implements Consumer, AutoCloseable {

    @Override public void onSessionInitiated(final Broker.ConsumerSession consumerSession) {
        final DOMMountPointService service = consumerSession.getService(DOMMountPointService.class);
        service.registerProvisionListener(new CachingMountpointLister(service));
    }

    @Override public Collection<ConsumerFunctionality> getConsumerFunctionality() {
        return null;
    }

    @Override public void close() throws Exception {
        // TODO Close everything
    }
}
