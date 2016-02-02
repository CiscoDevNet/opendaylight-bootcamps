package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.config.rev130405.modules.module.Configuration;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.kafka.agent.BindingBroker;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.kafka.agent.DomBroker;
import org.opendaylight.yangtools.yang.binding.Augmentable;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;kafka-agent-impl&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/kafka-agent-impl.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * case kafka-agent {
 *     container binding-broker {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:kafka-agent:impl?revision=2015-09-22)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 *     container dom-broker {
 *         leaf type {
 *             type leafref;
 *         }
 *         leaf name {
 *             type leafref;
 *         }
 *         uses service-ref {
 *             refine (urn:opendaylight:params:xml:ns:yang:kafka-agent:impl?revision=2015-09-22)type {
 *                 leaf type {
 *                     type leafref;
 *                 }
 *             }
 *         }
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;kafka-agent-impl/modules/module/configuration/(urn:opendaylight:params:xml:ns:yang:kafka-agent:impl?revision=2015-09-22)kafka-agent&lt;/i&gt;
 *
 */
public interface KafkaAgent
    extends
    DataObject,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>,
    Configuration
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:kafka-agent:impl","2015-09-22","kafka-agent"));

    BindingBroker getBindingBroker();
    
    DomBroker getDomBroker();

}

