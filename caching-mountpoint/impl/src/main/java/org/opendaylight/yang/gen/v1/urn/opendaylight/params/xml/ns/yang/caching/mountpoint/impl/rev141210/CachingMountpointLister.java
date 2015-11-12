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

public class CachingMountpointLister implements MountProvisionListener {

    private DOMMountPointService service;

    public CachingMountpointLister(final DOMMountPointService service) {
        this.service = service;
    }

    @Override public void onMountPointCreated(final YangInstanceIdentifier yangInstanceIdentifier) {
        final Optional<DOMMountPoint> mountPoint = service.getMountPoint(yangInstanceIdentifier);
        Preconditions.checkState(mountPoint.isPresent());
        final DOMMountPoint domMountPoint = mountPoint.get();

        final Optional<DOMDataBroker> dataBroker = domMountPoint.getService(DOMDataBroker.class);
        final Optional<DOMRpcService> rpcService = domMountPoint.getService(DOMRpcService.class);
        final Optional<DOMNotificationService> notificationService = domMountPoint.getService(DOMNotificationService.class);
        final SchemaContext schemaContext = domMountPoint.getSchemaContext();

        final DOMMountPointService.DOMMountPointBuilder cachingMountPointBuilder = service
            .createMountPoint(addCachingSuffixToId(yangInstanceIdentifier));

        cachingMountPointBuilder.addService(DOMRpcService.class, rpcService.get());
        cachingMountPointBuilder.addService(DOMNotificationService.class, notificationService.get());
        cachingMountPointBuilder.addService(DOMDataBroker.class, new CachingDOMDataBroker(dataBroker.get(), schemaContext));

        cachingMountPointBuilder.register();
    }

    // TODO test !
    private YangInstanceIdentifier addCachingSuffixToId(final YangInstanceIdentifier yangInstanceIdentifier) {
        final YangInstanceIdentifier.PathArgument lastPathArgument = yangInstanceIdentifier.getLastPathArgument();
        final Map<QName, Object> keyValues = ((YangInstanceIdentifier.NodeIdentifierWithPredicates) lastPathArgument)
            .getKeyValues();

        final QName idQName = QName.cachedReference(QName.create(lastPathArgument.getNodeType(), "node-id"));
        final String mountPointName = ((String) keyValues.get(idQName));

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
