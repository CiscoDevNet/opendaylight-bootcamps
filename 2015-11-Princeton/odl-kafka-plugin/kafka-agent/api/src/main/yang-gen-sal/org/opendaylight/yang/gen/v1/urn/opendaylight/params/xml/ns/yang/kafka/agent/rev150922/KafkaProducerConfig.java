package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfig.MessageSerialization;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfig.ProducerType;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfig.CompressionCodec;
import org.opendaylight.yangtools.yang.binding.Augmentable;


/**
 * &lt;p&gt;This class represents the following YANG schema fragment defined in module &lt;b&gt;kafka-agent&lt;/b&gt;
 * &lt;br&gt;(Source path: &lt;i&gt;META-INF/yang/kafka-agent.yang&lt;/i&gt;):
 * &lt;pre&gt;
 * container kafka-producer-config {
 *     leaf metadata-broker-list {
 *         type string;
 *     }
 *     leaf producer-type {
 *         type enumeration;
 *     }
 *     leaf compression-codec {
 *         type enumeration;
 *     }
 *     leaf topic {
 *         type string;
 *     }
 *     leaf message-serialization {
 *         type enumeration;
 *     }
 *     leaf dp-message-source-xpath {
 *         type string;
 *     }
 *     leaf dp-message-host-ip-xpath {
 *         type string;
 *     }
 *     leaf dp-timestamp-xpath {
 *         type string;
 *     }
 *     leaf avro-schema {
 *         type string;
 *     }
 *     leaf default-message-source {
 *         type string;
 *     }
 *     leaf default-host-ip {
 *         type string;
 *     }
 *     leaf event-subscriptions {
 *         type string;
 *     }
 * }
 * &lt;/pre&gt;
 * The schema path to identify an instance is
 * &lt;i&gt;kafka-agent/kafka-producer-config&lt;/i&gt;
 *
 * &lt;p&gt;To create instances of this class use {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfigBuilder}.
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfigBuilder
 *
 */
public interface KafkaProducerConfig
    extends
    ChildOf<KafkaAgentData>,
    Augmentable<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfig>
{


    /**
     * The enumeration built-in type represents values from a set of assigned names.
     *
     */
    public enum ProducerType {
        Sync(0),
        
        Async(1)
        ;
    
    
        int value;
        private static final java.util.Map<java.lang.Integer, ProducerType> VALUE_MAP;
    
        static {
            final com.google.common.collect.ImmutableMap.Builder<java.lang.Integer, ProducerType> b = com.google.common.collect.ImmutableMap.builder();
            for (ProducerType enumItem : ProducerType.values())
            {
                b.put(enumItem.value, enumItem);
            }
    
            VALUE_MAP = b.build();
        }
    
        private ProducerType(int value) {
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
         * @return corresponding ProducerType item
         */
        public static ProducerType forValue(int valueArg) {
            return VALUE_MAP.get(valueArg);
        }
    }
    
    /**
     * The enumeration built-in type represents values from a set of assigned names.
     *
     */
    public enum CompressionCodec {
        None(0),
        
        Gzip(1),
        
        Snappy(2)
        ;
    
    
        int value;
        private static final java.util.Map<java.lang.Integer, CompressionCodec> VALUE_MAP;
    
        static {
            final com.google.common.collect.ImmutableMap.Builder<java.lang.Integer, CompressionCodec> b = com.google.common.collect.ImmutableMap.builder();
            for (CompressionCodec enumItem : CompressionCodec.values())
            {
                b.put(enumItem.value, enumItem);
            }
    
            VALUE_MAP = b.build();
        }
    
        private CompressionCodec(int value) {
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
         * @return corresponding CompressionCodec item
         */
        public static CompressionCodec forValue(int valueArg) {
            return VALUE_MAP.get(valueArg);
        }
    }
    
    /**
     * The enumeration built-in type represents values from a set of assigned names.
     *
     */
    public enum MessageSerialization {
        Raw(0),
        
        Avro(1)
        ;
    
    
        int value;
        private static final java.util.Map<java.lang.Integer, MessageSerialization> VALUE_MAP;
    
        static {
            final com.google.common.collect.ImmutableMap.Builder<java.lang.Integer, MessageSerialization> b = com.google.common.collect.ImmutableMap.builder();
            for (MessageSerialization enumItem : MessageSerialization.values())
            {
                b.put(enumItem.value, enumItem);
            }
    
            VALUE_MAP = b.build();
        }
    
        private MessageSerialization(int value) {
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
         * @return corresponding MessageSerialization item
         */
        public static MessageSerialization forValue(int valueArg) {
            return VALUE_MAP.get(valueArg);
        }
    }

    public static final QName QNAME = org.opendaylight.yangtools.yang.common.QName.cachedReference(org.opendaylight.yangtools.yang.common.QName.create("urn:opendaylight:params:xml:ns:yang:kafka-agent","2015-09-22","kafka-producer-config"));

    /**
     * The bootstrapping used by the agent for getting metadata (topics, partitions, 
     * and replicas).
     *
     */
    java.lang.String getMetadataBrokerList();
    
    ProducerType getProducerType();
    
    CompressionCodec getCompressionCodec();
    
    java.lang.String getTopic();
    
    /**
     * if raw is set, the data
     *
     */
    MessageSerialization getMessageSerialization();
    
    /**
     * set xpath statement to extract message source message payload
     *
     */
    java.lang.String getDpMessageSourceXpath();
    
    /**
     * if this parameter is not set, runtime host ip is set as default by runtime.
     *
     */
    java.lang.String getDpMessageHostIpXpath();
    
    /**
     * if it is not set, runtime timestamp will be used.
     *
     */
    java.lang.String getDpTimestampXpath();
    
    /**
     * by default PaNDA avro schema is used.
     *
     */
    java.lang.String getAvroSchema();
    
    /**
     * set default message source that would apply to all ETB messages
     *
     */
    java.lang.String getDefaultMessageSource();
    
    java.lang.String getDefaultHostIp();
    
    /**
     * ODL event topic filter; if not set, all topics are valid
     *
     */
    java.lang.String getEventSubscriptions();

}

