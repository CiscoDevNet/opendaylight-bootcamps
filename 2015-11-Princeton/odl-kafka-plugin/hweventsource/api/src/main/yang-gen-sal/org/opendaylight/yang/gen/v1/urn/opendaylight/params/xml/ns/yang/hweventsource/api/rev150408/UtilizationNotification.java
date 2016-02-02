package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.Notification;


/**
 * Utilization message from network device
 *
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;hweventsource&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/hweventsource.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * notification utilization-notification {
 *     description
 *         "Utilization message from network device";
 *     leaf utilization {
 *         type uint8;
 *     }
 *     status CURRENT;
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;hweventsource/utilization-notification&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.UtilizationNotificationBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.UtilizationNotificationBuilder
 *
 */
public interface UtilizationNotification
    extends
    DataObject,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.UtilizationNotification>,
    Notification
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:hweventsource:api","2015-04-08","utilization-notification"));

    /**
     * Utilization percentage, 0..100
     *
     */
    java.lang.Short getUtilization();

}

