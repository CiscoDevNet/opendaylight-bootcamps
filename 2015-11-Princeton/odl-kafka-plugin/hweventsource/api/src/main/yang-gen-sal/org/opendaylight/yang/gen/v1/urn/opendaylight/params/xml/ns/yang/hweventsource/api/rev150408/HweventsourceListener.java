package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408;
import org.opendaylight.yangtools.yang.binding.NotificationListener;


/**
 * Interface for receiving the following YANG notifications defined in module &lt;b&gt;hweventsource&lt;/b&gt;
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
 * notification utilization-notification {
 *     description
 *         "Utilization message from network device";
 *     leaf utilization {
 *         type uint8;
 *     }
 *     status CURRENT;
 * }
 * &lt;/pre&gt;
 *
 */
public interface HweventsourceListener
    extends
    NotificationListener
{




    /**
     * Simple notification used in event source example.
     *
     */
    void onSampleEventSourceNotification(SampleEventSourceNotification notification);
    
    /**
     * Utilization message from network device
     *
     */
    void onUtilizationNotification(UtilizationNotification notification);

}

