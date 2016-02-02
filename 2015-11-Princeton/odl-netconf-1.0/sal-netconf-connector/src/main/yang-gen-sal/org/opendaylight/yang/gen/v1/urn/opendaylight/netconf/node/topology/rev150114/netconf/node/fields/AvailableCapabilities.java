package org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.NetconfNodeFields;
import java.util.List;
import org.opendaylight.yangtools.yang.binding.Augmentable;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;netconf-node-topology&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/netconf-node-topology.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * container available-capabilities {
 *     leaf-list available-capability {
 *         type string;
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;netconf-node-topology/netconf-node-fields/available-capabilities&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.AvailableCapabilitiesBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.AvailableCapabilitiesBuilder
 *
 */
public interface AvailableCapabilities
    extends
    ChildOf<NetconfNodeFields>,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.netconf.node.topology.rev150114.netconf.node.fields.AvailableCapabilities>
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:netconf-node-topology","2015-01-14","available-capabilities"));

    List<java.lang.String> getAvailableCapability();

}

