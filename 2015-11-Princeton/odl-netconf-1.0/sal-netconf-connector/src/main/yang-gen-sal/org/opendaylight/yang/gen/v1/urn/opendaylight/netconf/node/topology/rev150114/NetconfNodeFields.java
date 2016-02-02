package org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.UnavailableCapabilities;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.Host;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.PassThrough;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.AvailableCapabilities;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields.ConnectionStatus;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.PortNumber;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;netconf-node-topology&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/netconf-node-topology.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * grouping netconf-node-fields {
 *     leaf connection-status {
 *         type enumeration;
 *     }
 *     leaf host {
 *         type host;
 *     }
 *     leaf port {
 *         type port-number;
 *     }
 *     leaf connected-message {
 *         type string;
 *     }
 *     container available-capabilities {
 *         leaf-list available-capability {
 *             type string;
 *         }
 *     }
 *     container unavailable-capabilities {
 *         list unavailable-capability {
 *             key     leaf capability {
 *                 type string;
 *             }
 *             leaf failure-reason {
 *                 type enumeration;
 *             }
 *         }
 *     }
 *     container pass-through {
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;netconf-node-topology/netconf-node-fields&lt;/i&gt;
 *
 */
public interface NetconfNodeFields
    extends
    DataObject
{


    /**
     * The enumeration built-in type represents values from a set of assigned names.
     *
     */
    public enum ConnectionStatus {
        Connecting(0),
        
        Connected(1),
        
        UnableToConnect(2)
        ;
    
    
        int value;
        private static final java.util.Map<java.lang.Integer, ConnectionStatus> VALUE_MAP;
    
        static {
            final com.google.common.collect.ImmutableMap.Builder<java.lang.Integer, ConnectionStatus> b = com.google.common.collect.ImmutableMap.builder();
            for (ConnectionStatus enumItem : ConnectionStatus.values())
            {
                b.put(enumItem.value, enumItem);
            }
    
            VALUE_MAP = b.build();
        }
    
        private ConnectionStatus(int value) {
            this.value = value;
        }
    
        /**
         * @return integer value
         */
        public int getIntValue() {
            return value;
        }
    
        /**
         * @param valueArg
         * @return corresponding ConnectionStatus item
         */
        public static ConnectionStatus forValue(int valueArg) {
            return VALUE_MAP.get(valueArg);
        }
    }

    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:netconf-node-topology","2015-01-14","netconf-node-fields"));

    ConnectionStatus getConnectionStatus();
    
    Host getHost();
    
    PortNumber getPort();
    
    java.lang.String getConnectedMessage();
    
    AvailableCapabilities getAvailableCapabilities();
    
    UnavailableCapabilities getUnavailableCapabilities();
    
    /**
     * When the underlying node is connected, its NETCONF context is available verbatim
     * under this container through the mount extension.
     *
     */
    PassThrough getPassThrough();

}

