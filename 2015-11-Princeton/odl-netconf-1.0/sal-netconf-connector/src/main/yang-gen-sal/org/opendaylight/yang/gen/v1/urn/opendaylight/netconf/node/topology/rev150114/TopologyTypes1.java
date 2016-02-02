package org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114;
import org.opendaylight.yangtools.yang.binding.Augmentation;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.network.topology.topology.TopologyTypes;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.network.topology.topology.topology.types.TopologyNetconf;


public interface TopologyTypes1
    extends
    DataObject,
    Augmentation<TopologyTypes>
{




    TopologyNetconf getTopologyNetconf();

}

