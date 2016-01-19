package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.caching.mountpoint.impl.rev141210;

import com.google.common.base.Optional;
import com.google.common.base.Preconditions;
import com.google.common.collect.Lists;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import org.opendaylight.controller.md.sal.dom.api.DOMDataBroker;
import org.opendaylight.controller.md.sal.dom.api.DOMMountPoint;
import org.opendaylight.controller.md.sal.dom.api.DOMMountPointService;
import org.opendaylight.controller.md.sal.dom.api.DOMNotificationService;
import org.opendaylight.controller.md.sal.dom.api.DOMRpcService;
import org.opendaylight.controller.sal.core.api.mount.MountProvisionListener;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier;
import org.opendaylight.yangtools.yang.model.api.SchemaContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CachingMountpointLister implements MountProvisionListener {

	private static final Logger LOG = LoggerFactory.getLogger(CachingMountpointLister.class);

    private DOMMountPointService service;

    public CachingMountpointLister(final DOMMountPointService service) {
        this.service = service;
    }



    @Override public void onMountPointCreated(final YangInstanceIdentifier yangInstanceIdentifier) {

    	LOG.info("received onMountPointCreated event for id={}", yangInstanceIdentifier);

        final Optional<DOMMountPoint> mountPoint = service.getMountPoint(yangInstanceIdentifier);
        Preconditions.checkState(mountPoint.isPresent());
        final DOMMountPoint domMountPoint = mountPoint.get();

        final Optional<DOMDataBroker> dataBroker = domMountPoint.getService(DOMDataBroker.class);

        if(dataBroker.isPresent() && dataBroker.get() instanceof CachingDOMDataBroker) {
        	LOG.info("Ignoring CachingDOMDataBroker creation ...");
        	return;
        }

        final Optional<DOMRpcService> rpcService = domMountPoint.getService(DOMRpcService.class);
        final Optional<DOMNotificationService> notificationService = domMountPoint.getService(DOMNotificationService.class);
        final SchemaContext schemaContext = domMountPoint.getSchemaContext();

        YangInstanceIdentifier yangid= addCachingSuffixToId(yangInstanceIdentifier);

        final DOMMountPointService.DOMMountPointBuilder cachingMountPointBuilder = service
            .createMountPoint(yangid);

        cachingMountPointBuilder.addService(DOMRpcService.class, rpcService.get());
        cachingMountPointBuilder.addInitialSchemaContext(schemaContext);
        cachingMountPointBuilder.addService(DOMNotificationService.class, notificationService.get());
        LOG.info("creating CachingDOMDataBroker for yangInstanceIdentifier={} with new id={}", yangInstanceIdentifier, yangid);
        cachingMountPointBuilder.addService(DOMDataBroker.class, new CachingDOMDataBroker(dataBroker.get(), schemaContext));

        cachingMountPointBuilder.register();
    }

    // TODO test !
    private YangInstanceIdentifier addCachingSuffixToId(final YangInstanceIdentifier yangInstanceIdentifier) {
        final YangInstanceIdentifier.PathArgument lastPathArgument = yangInstanceIdentifier.getLastPathArgument();
        final Map<QName, Object> keyValues = ((YangInstanceIdentifier.NodeIdentifierWithPredicates) lastPathArgument)
            .getKeyValues();

        //to do
       //final QName idQName = QName.cachedReference(QName.create(lastPathArgument.getNodeType(), "node-id"));

        final QName idQName = keyValues.keySet().iterator().next();
        //final String mountPointName = ((String) keyValues.get(idQName));

        final String mountPointName = ((String) keyValues.values().iterator().next());

        final String cachedNodeId = mountPointName + "-cached";

        final YangInstanceIdentifier.NodeIdentifierWithPredicates cachedLastPathArgument =
            new YangInstanceIdentifier.NodeIdentifierWithPredicates(
            lastPathArgument.getNodeType(), Collections.<QName, Object>singletonMap(idQName, cachedNodeId));

        final List<YangInstanceIdentifier.PathArgument> cachedPathArguments = Lists
            .newArrayList(yangInstanceIdentifier.getPathArguments());
        cachedPathArguments.remove(cachedPathArguments.size() - 1);

        cachedPathArguments.add(cachedLastPathArgument);

        return YangInstanceIdentifier.create(cachedPathArguments);
    }

    @Override public void onMountPointRemoved(final YangInstanceIdentifier yangInstanceIdentifier) {
        // Ignoring because we want to keep the cache without connection
    }
}
