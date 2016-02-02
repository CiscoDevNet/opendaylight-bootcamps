package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;odl-sal-netconf-connector-cfg&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/odl-sal-netconf-connector-cfg.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * grouping server {
 *     leaf address {
 *         type string;
 *     }
 *     leaf port {
 *         type uint32;
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;odl-sal-netconf-connector-cfg/server&lt;/i&gt;
 *
 */
public interface Server
    extends
    DataObject
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf","2013-10-28","server"));

    java.lang.String getAddress();
    
    java.lang.Long getPort();

}

