package org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.concepts.Builder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.network.topology.topology.topology.types.TopologyNetconf;


/**
 * Class that builds {@link org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1} instances.
 *
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1
 *
 */
public class TopologyTypes1Builder implements Builder <org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1> {

    private TopologyNetconf _topologyNetconf;


    public TopologyTypes1Builder() {
    }

    public TopologyTypes1Builder(TopologyTypes1 base) {
        this._topologyNetconf = base.getTopologyNetconf();
    }


    public TopologyNetconf getTopologyNetconf() {
        return _topologyNetconf;
    }

    public TopologyTypes1Builder setTopologyNetconf(TopologyNetconf value) {
        this._topologyNetconf = value;
        return this;
    }

    public TopologyTypes1 build() {
        return new TopologyTypes1Impl(this);
    }

    private static final class TopologyTypes1Impl implements TopologyTypes1 {

        public java.lang.Class<org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1> getImplementedInterface() {
            return org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1.class;
        }

        private final TopologyNetconf _topologyNetconf;


        private TopologyTypes1Impl(TopologyTypes1Builder base) {
            this._topologyNetconf = base.getTopologyNetconf();
        }

        @Override
        public TopologyNetconf getTopologyNetconf() {
            return _topologyNetconf;
        }

        private int hash = 0;
        private volatile boolean hashValid = false;
        
        @Override
        public int hashCode() {
            if (hashValid) {
                return hash;
            }
        
            final int prime = 31;
            int result = 1;
            result = prime * result + ((_topologyNetconf == null) ? 0 : _topologyNetconf.hashCode());
        
            hash = result;
            hashValid = true;
            return result;
        }

        @Override
        public boolean equals(java.lang.Object obj) {
            if (this == obj) {
                return true;
            }
            if (!(obj instanceof DataObject)) {
                return false;
            }
            if (!org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1.class.equals(((DataObject)obj).getImplementedInterface())) {
                return false;
            }
            org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1 other = (org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.TopologyTypes1)obj;
            if (_topologyNetconf == null) {
                if (other.getTopologyNetconf() != null) {
                    return false;
                }
            } else if(!_topologyNetconf.equals(other.getTopologyNetconf())) {
                return false;
            }
            return true;
        }

        @Override
        public java.lang.String toString() {
            java.lang.StringBuilder builder = new java.lang.StringBuilder ("TopologyTypes1 [");
            boolean first = true;
        
            if (_topologyNetconf != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_topologyNetconf=");
                builder.append(_topologyNetconf);
             }
            return builder.append(']').toString();
        }
    }

}
