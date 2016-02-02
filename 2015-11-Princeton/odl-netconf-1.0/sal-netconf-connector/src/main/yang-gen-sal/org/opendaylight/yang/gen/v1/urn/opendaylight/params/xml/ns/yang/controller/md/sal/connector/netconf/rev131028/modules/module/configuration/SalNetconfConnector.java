package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.config.rev130405.modules.module.Configuration;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.ProcessingExecutor;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.Host;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.DomRegistry;
import java.math.BigDecimal;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.EventExecutor;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.KeepaliveExecutor;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.YangModuleCapabilities;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.BindingRegistry;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.ClientDispatcher;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.PortNumber;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;odl-sal-netconf-connector-cfg&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/odl-sal-netconf-connector-cfg.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * case sal-netconf-connector {
 *     leaf address {
 *         type host;
 *     }
 *     leaf port {
 *         type port-number;
 *     }
 *     leaf tcp-only {
 *         type boolean;
 *     }
 *     leaf username {
 *         type string;
 *     }
 *     leaf password {
 *         type string;
 *     }
 *     container yang-module-capabilities {
 *         leaf-list capability {
 *             type string;
 *         }
 *     }
 *     leaf reconnect-on-changed-schema {
 *         type boolean;
 *     }
 *     container dom-registry {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 *     container binding-registry {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 *     container event-executor {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 *     container processing-executor {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 *     container client-dispatcher {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 *     leaf connection-timeout-millis {
 *         type uint32;
 *     }
 *     leaf default-request-timeout-millis {
 *         type uint32;
 *     }
 *     leaf max-connection-attempts {
 *         type uint32;
 *     }
 *     leaf between-attempts-timeout-millis {
 *         type uint16;
 *     }
 *     leaf sleep-factor {
 *         type decimal64;
 *     }
 *     leaf keepalive-delay {
 *         type uint32;
 *     }
 *     container keepalive-executor {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;odl-sal-netconf-connector-cfg/modules/module/configuration/(urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf?revision=2013-10-28)sal-netconf-connector&lt;/i&gt;
 *
 */
public interface SalNetconfConnector
    extends
    DataObject,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>,
    Configuration
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:controller:md:sal:connector:netconf","2013-10-28","sal-netconf-connector"));

    Host getAddress();
    
    PortNumber getPort();
    
    java.lang.Boolean isTcpOnly();
    
    java.lang.String getUsername();
    
    java.lang.String getPassword();
    
    YangModuleCapabilities getYangModuleCapabilities();
    
    /**
     * If true, the connector would auto disconnect/reconnect when schemas are changed 
     * in the remote device. The connector subscribes (right after connect) to base 
     * netconf notifications and listens for netconf-capability-change notification
     *
     */
    java.lang.Boolean isReconnectOnChangedSchema();
    
    DomRegistry getDomRegistry();
    
    BindingRegistry getBindingRegistry();
    
    EventExecutor getEventExecutor();
    
    /**
     * Makes up for flaws in netty threading design
     *
     */
    ProcessingExecutor getProcessingExecutor();
    
    ClientDispatcher getClientDispatcher();
    
    /**
     * Specifies timeout in milliseconds after which connection must be established.
     *
     */
    java.lang.Long getConnectionTimeoutMillis();
    
    /**
     * Timeout for blocking operations within transactions.
     *
     */
    java.lang.Long getDefaultRequestTimeoutMillis();
    
    /**
     * Maximum number of connection retries. Non positive value or null is interpreted 
     * as infinity.
     *
     */
    java.lang.Long getMaxConnectionAttempts();
    
    /**
     * Initial timeout in milliseconds to wait between connection attempts. Will be 
     * multiplied by sleep-factor with every additional attempt
     *
     */
    java.lang.Integer getBetweenAttemptsTimeoutMillis();
    
    BigDecimal getSleepFactor();
    
    /**
     * Netconf connector sends keepalive RPCs while the session is idle, this delay 
     * specifies the delay between keepalive RPC in seconds If a value &lt;1 is 
     * provided, no keepalives will be sent
     *
     */
    java.lang.Long getKeepaliveDelay();
    
    /**
     * Dedicated solely to keepalive execution
     *
     */
    KeepaliveExecutor getKeepaliveExecutor();

}

