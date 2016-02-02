package org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.unavailable.capabilities;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.UnavailableCapabilities;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.unavailable.capabilities.UnavailableCapability.FailureReason;
import org.opendaylight.yangtools.yang.binding.Augmentable;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;netconf-node-topology&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/netconf-node-topology.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * list unavailable-capability {
 *     key     leaf capability {
 *         type string;
 *     }
 *     leaf failure-reason {
 *         type enumeration;
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;netconf-node-topology/netconf-node-fields/unavailable-capabilities/unavailable-capability&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.unavailable.capabilities.UnavailableCapabilityBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.unavailable.capabilities.UnavailableCapabilityBuilder
 *
 *
 */
public interface UnavailableCapability
    extends
    ChildOf<UnavailableCapabilities>,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.unavailable.capabilities.UnavailableCapability>
{


    /**
     * The enumeration built-in type represents values from a set of assigned names.
     *
     */
    public enum FailureReason {
        MissingSource(0),
        
        UnableToResolve(1)
        ;
    
    
        int value;
        private static final java.util.Map<java.lang.Integer, FailureReason> VALUE_MAP;
    
        static {
            final com.google.common.collect.ImmutableMap.Builder<java.lang.Integer, FailureReason> b = com.google.common.collect.ImmutableMap.builder();
            for (FailureReason enumItem : FailureReason.values())
            {
                b.put(enumItem.value, enumItem);
            }
    
            VALUE_MAP = b.build();
        }
    
        private FailureReason(int value) {
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
         * @return corresponding FailureReason item
         */
        public static FailureReason forValue(int valueArg) {
            return VALUE_MAP.get(valueArg);
        }
    }

    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:netconf-node-topology","2015-01-14","unavailable-capability"));

    java.lang.String getCapability();
    
    FailureReason getFailureReason();

}

