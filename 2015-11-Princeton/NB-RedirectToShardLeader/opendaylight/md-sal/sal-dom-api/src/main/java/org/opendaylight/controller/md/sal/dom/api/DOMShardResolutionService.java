package org.opendaylight.controller.md.sal.dom.api;

import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier;


public interface DOMShardResolutionService extends DOMDataBrokerExtension {

/**
 * Returns host name of shard leader for path.  Returns null if current host is shard leader.
 * @param type - data store type (CONFIGURATION, OPERATIONAL)
 * @param path - Instance identifier
 * @return
 */
 public String getShardLeaderForPath(LogicalDatastoreType type, YangInstanceIdentifier path);
}
