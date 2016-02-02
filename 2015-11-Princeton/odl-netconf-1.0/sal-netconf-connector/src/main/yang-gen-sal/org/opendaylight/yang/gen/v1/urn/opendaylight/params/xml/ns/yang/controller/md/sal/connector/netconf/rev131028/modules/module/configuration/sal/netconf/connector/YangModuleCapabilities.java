package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.common.QName;
import java.util.List;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.config.rev130405.modules.Module;
import org.opendaylight.yangtools.yang.binding.Augmentable;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;odl-sal-netconf-connector-cfg&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/odl-sal-netconf-connector-cfg.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * container yang-module-capabilities {
 *     leaf-list capability {
 *         type string;
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;odl-sal-netconf-connector-cfg/modules/module/configuration/(urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)sal-netconf-connector/yang-module-capabilities&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.YangModuleCapabilitiesBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.YangModuleCapabilitiesBuilder
 *
 */
public interface YangModuleCapabilities
    extends
    ChildOf<Module>,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.YangModuleCapabilities>
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf","2013-10-28","yang-module-capabilities"));

    /**
     * Set a list of capabilities to override capabilities provided in device's hello 
     * message. Can be used for devices that do not report any yang modules in their 
     * hello message
     *
     */
    List<java.lang.String> getCapability();

}

