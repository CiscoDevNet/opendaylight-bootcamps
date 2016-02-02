package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.config.rev130405.modules.Module;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.config.rev130405.ServiceRef;
import org.opendaylight.yangtools.yang.binding.Augmentable;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;hweventsource-impl&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/hweventsource-impl.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * container event-source-registry {
 *     leaf type {
 *         type leafref;
 *     }
 *     leaf name {
 *         type leafref;
 *     }
 *     uses service-ref {
 *         refine (urn:opendaylight:params:xml:ns:yang:hweventsource:impl?revision=2014-12-10)type {
 *             leaf type {
 *                 type leafref;
 *             }
 *         }
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;hweventsource-impl/modules/module/configuration/(urn:opendaylight:params:xml:ns:yang:hweventsource:impl?revision=2014-12-10)hweventsource/event-source-registry&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource.EventSourceRegistryBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource.EventSourceRegistryBuilder
 *
 */
public interface EventSourceRegistry
    extends
    ChildOf<Module>,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource.EventSourceRegistry>,
    ServiceRef
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:hweventsource:impl","2014-12-10","event-source-registry"));


}

