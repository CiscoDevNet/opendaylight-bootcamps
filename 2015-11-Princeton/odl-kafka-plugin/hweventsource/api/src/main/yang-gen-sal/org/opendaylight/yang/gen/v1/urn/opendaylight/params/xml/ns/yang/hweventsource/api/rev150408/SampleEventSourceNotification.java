package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.Notification;


/**
 * Simple notification used in event source example.
 *
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;hweventsource&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/hweventsource.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * notification sample-event-source-notification {
 *     description
 *         "Simple notification used in event source example.";
 *     leaf source-id {
 *         type source-identifier;
 *     }
 *     leaf message {
 *         type string;
 *     }
 *     status CURRENT;
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;hweventsource/sample-event-source-notification&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotificationBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotificationBuilder
 *
 */
public interface SampleEventSourceNotification
    extends
    DataObject,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>,
    Notification
{



    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:hweventsource:api","2015-04-08","sample-event-source-notification"));

    /**
     * source identifier
     *
     */
    SourceIdentifier getSourceId();
    
    /**
     * message / content of notification
     *
     */
    java.lang.String getMessage();

}

