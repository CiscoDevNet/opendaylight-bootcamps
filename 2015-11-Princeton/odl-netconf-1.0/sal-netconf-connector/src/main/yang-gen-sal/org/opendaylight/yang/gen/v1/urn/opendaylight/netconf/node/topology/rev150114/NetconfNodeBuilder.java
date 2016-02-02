package org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.concepts.Builder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.UnavailableCapabilities;
import java.math.BigInteger;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.Host;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.PassThrough;
import java.util.List;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.AvailableCapabilities;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields.ConnectionStatus;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.PortNumber;
import com.google.common.collect.Range;


/**
 * Class that builds {@link org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode} instances.
 *
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode
 *
 */
public class NetconfNodeBuilder implements Builder <org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode> {

    private AvailableCapabilities _availableCapabilities;
    private java.lang.String _connectedMessage;
    private ConnectionStatus _connectionStatus;
    private Host _host;
    private PassThrough _passThrough;
    private PortNumber _port;
    private UnavailableCapabilities _unavailableCapabilities;


    public NetconfNodeBuilder() {
    }
    public NetconfNodeBuilder(org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields arg) {
        this._connectionStatus = arg.getConnectionStatus();
        this._host = arg.getHost();
        this._port = arg.getPort();
        this._connectedMessage = arg.getConnectedMessage();
        this._availableCapabilities = arg.getAvailableCapabilities();
        this._unavailableCapabilities = arg.getUnavailableCapabilities();
        this._passThrough = arg.getPassThrough();
    }

    public NetconfNodeBuilder(NetconfNode base) {
        this._availableCapabilities = base.getAvailableCapabilities();
        this._connectedMessage = base.getConnectedMessage();
        this._connectionStatus = base.getConnectionStatus();
        this._host = base.getHost();
        this._passThrough = base.getPassThrough();
        this._port = base.getPort();
        this._unavailableCapabilities = base.getUnavailableCapabilities();
    }

    /**
     *Set fields from given grouping argument. Valid argument is instance of one of following types:
     * <ul>
     * <li>org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields</li>
     * </ul>
     *
     * @param arg grouping object
     * @throws IllegalArgumentException if given argument is none of valid types
    */
    public void fieldsFrom(DataObject arg) {
        boolean isValidArg = false;
        if (arg instanceof org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields) {
            this._connectionStatus = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getConnectionStatus();
            this._host = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getHost();
            this._port = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getPort();
            this._connectedMessage = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getConnectedMessage();
            this._availableCapabilities = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getAvailableCapabilities();
            this._unavailableCapabilities = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getUnavailableCapabilities();
            this._passThrough = ((org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields)arg).getPassThrough();
            isValidArg = true;
        }
        if (!isValidArg) {
            throw new IllegalArgumentException(
              "expected one of: [org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields] \n" +
              "but was: " + arg
            );
        }
    }

    public AvailableCapabilities getAvailableCapabilities() {
        return _availableCapabilities;
    }
    
    public java.lang.String getConnectedMessage() {
        return _connectedMessage;
    }
    
    public ConnectionStatus getConnectionStatus() {
        return _connectionStatus;
    }
    
    public Host getHost() {
        return _host;
    }
    
    public PassThrough getPassThrough() {
        return _passThrough;
    }
    
    public PortNumber getPort() {
        return _port;
    }
    
    public UnavailableCapabilities getUnavailableCapabilities() {
        return _unavailableCapabilities;
    }

    public NetconfNodeBuilder setAvailableCapabilities(AvailableCapabilities value) {
        this._availableCapabilities = value;
        return this;
    }
    
    public NetconfNodeBuilder setConnectedMessage(java.lang.String value) {
        this._connectedMessage = value;
        return this;
    }
    
    public NetconfNodeBuilder setConnectionStatus(ConnectionStatus value) {
        this._connectionStatus = value;
        return this;
    }
    
    public NetconfNodeBuilder setHost(Host value) {
        if (value != null) {
        }
        this._host = value;
        return this;
    }
    
    public NetconfNodeBuilder setPassThrough(PassThrough value) {
        this._passThrough = value;
        return this;
    }
    
    private static void checkPortRange(final int value) {
        if (value >= 0 && value <= 65535) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥65535]].", value));
    }
    
    public NetconfNodeBuilder setPort(PortNumber value) {
        if (value != null) {
            checkPortRange(value.getValue());
        }
        this._port = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _port_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(65535L)));
        return ret;
    }
    
    public NetconfNodeBuilder setUnavailableCapabilities(UnavailableCapabilities value) {
        this._unavailableCapabilities = value;
        return this;
    }

    public NetconfNode build() {
        return new NetconfNodeImpl(this);
    }

    private static final class NetconfNodeImpl implements NetconfNode {

        public java.lang.Class<org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode> getImplementedInterface() {
            return org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode.class;
        }

        private final AvailableCapabilities _availableCapabilities;
        private final java.lang.String _connectedMessage;
        private final ConnectionStatus _connectionStatus;
        private final Host _host;
        private final PassThrough _passThrough;
        private final PortNumber _port;
        private final UnavailableCapabilities _unavailableCapabilities;


        private NetconfNodeImpl(NetconfNodeBuilder base) {
            this._availableCapabilities = base.getAvailableCapabilities();
            this._connectedMessage = base.getConnectedMessage();
            this._connectionStatus = base.getConnectionStatus();
            this._host = base.getHost();
            this._passThrough = base.getPassThrough();
            this._port = base.getPort();
            this._unavailableCapabilities = base.getUnavailableCapabilities();
        }

        @Override
        public AvailableCapabilities getAvailableCapabilities() {
            return _availableCapabilities;
        }
        
        @Override
        public java.lang.String getConnectedMessage() {
            return _connectedMessage;
        }
        
        @Override
        public ConnectionStatus getConnectionStatus() {
            return _connectionStatus;
        }
        
        @Override
        public Host getHost() {
            return _host;
        }
        
        @Override
        public PassThrough getPassThrough() {
            return _passThrough;
        }
        
        @Override
        public PortNumber getPort() {
            return _port;
        }
        
        @Override
        public UnavailableCapabilities getUnavailableCapabilities() {
            return _unavailableCapabilities;
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
            result = prime * result + ((_availableCapabilities == null) ? 0 : _availableCapabilities.hashCode());
            result = prime * result + ((_connectedMessage == null) ? 0 : _connectedMessage.hashCode());
            result = prime * result + ((_connectionStatus == null) ? 0 : _connectionStatus.hashCode());
            result = prime * result + ((_host == null) ? 0 : _host.hashCode());
            result = prime * result + ((_passThrough == null) ? 0 : _passThrough.hashCode());
            result = prime * result + ((_port == null) ? 0 : _port.hashCode());
            result = prime * result + ((_unavailableCapabilities == null) ? 0 : _unavailableCapabilities.hashCode());
        
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
            if (!org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode.class.equals(((DataObject)obj).getImplementedInterface())) {
                return false;
            }
            org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode other = (org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNode)obj;
            if (_availableCapabilities == null) {
                if (other.getAvailableCapabilities() != null) {
                    return false;
                }
            } else if(!_availableCapabilities.equals(other.getAvailableCapabilities())) {
                return false;
            }
            if (_connectedMessage == null) {
                if (other.getConnectedMessage() != null) {
                    return false;
                }
            } else if(!_connectedMessage.equals(other.getConnectedMessage())) {
                return false;
            }
            if (_connectionStatus == null) {
                if (other.getConnectionStatus() != null) {
                    return false;
                }
            } else if(!_connectionStatus.equals(other.getConnectionStatus())) {
                return false;
            }
            if (_host == null) {
                if (other.getHost() != null) {
                    return false;
                }
            } else if(!_host.equals(other.getHost())) {
                return false;
            }
            if (_passThrough == null) {
                if (other.getPassThrough() != null) {
                    return false;
                }
            } else if(!_passThrough.equals(other.getPassThrough())) {
                return false;
            }
            if (_port == null) {
                if (other.getPort() != null) {
                    return false;
                }
            } else if(!_port.equals(other.getPort())) {
                return false;
            }
            if (_unavailableCapabilities == null) {
                if (other.getUnavailableCapabilities() != null) {
                    return false;
                }
            } else if(!_unavailableCapabilities.equals(other.getUnavailableCapabilities())) {
                return false;
            }
            return true;
        }

        @Override
        public java.lang.String toString() {
            java.lang.StringBuilder builder = new java.lang.StringBuilder ("NetconfNode [");
            boolean first = true;
        
            if (_availableCapabilities != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_availableCapabilities=");
                builder.append(_availableCapabilities);
             }
            if (_connectedMessage != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_connectedMessage=");
                builder.append(_connectedMessage);
             }
            if (_connectionStatus != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_connectionStatus=");
                builder.append(_connectionStatus);
             }
            if (_host != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_host=");
                builder.append(_host);
             }
            if (_passThrough != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_passThrough=");
                builder.append(_passThrough);
             }
            if (_port != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_port=");
                builder.append(_port);
             }
            if (_unavailableCapabilities != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_unavailableCapabilities=");
                builder.append(_unavailableCapabilities);
             }
            return builder.append(']').toString();
        }
    }

}
