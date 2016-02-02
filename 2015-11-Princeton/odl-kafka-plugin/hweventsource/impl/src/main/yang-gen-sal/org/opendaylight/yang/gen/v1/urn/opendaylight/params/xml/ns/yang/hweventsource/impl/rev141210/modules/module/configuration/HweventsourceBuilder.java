package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration;
import org.opendaylight.yangtools.yang.binding.AugmentationHolder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource.Broker;
import java.util.HashMap;
import org.opendaylight.yangtools.concepts.Builder;
import java.util.ArrayList;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource.DomBroker;
import com.google.common.collect.Range;
import org.opendaylight.yangtools.yang.binding.Augmentation;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.hweventsource.EventSourceRegistry;
import java.math.BigInteger;
import java.util.List;
import java.util.Collections;
import java.util.Map;


/**
 * Class that builds {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource} instances.
 *
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource
 *
 */
public class HweventsourceBuilder implements Builder <org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource> {

    private Broker _broker;
    private DomBroker _domBroker;
    private EventSourceRegistry _eventSourceRegistry;
    private java.lang.Short _messageGeneratePeriod;
    private java.lang.String _messageText;
    private static void check_messageTextLength(final String value) {
        final int length = value.length();
        if (length >= 1 && length <= 1024) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid length: %s, expected: [[1‥1024]].", value));
    }
    private java.lang.Short _numberEventSources;

    Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> augmentation = Collections.emptyMap();

    public HweventsourceBuilder() {
    }

    public HweventsourceBuilder(Hweventsource base) {
        this._broker = base.getBroker();
        this._domBroker = base.getDomBroker();
        this._eventSourceRegistry = base.getEventSourceRegistry();
        this._messageGeneratePeriod = base.getMessageGeneratePeriod();
        this._messageText = base.getMessageText();
        this._numberEventSources = base.getNumberEventSources();
        if (base instanceof HweventsourceImpl) {
            HweventsourceImpl impl = (HweventsourceImpl) base;
            if (!impl.augmentation.isEmpty()) {
                this.augmentation = new HashMap<>(impl.augmentation);
            }
        } else if (base instanceof AugmentationHolder) {
            @SuppressWarnings("unchecked")
            AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource> casted =(AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>) base;
            if (!casted.augmentations().isEmpty()) {
                this.augmentation = new HashMap<>(casted.augmentations());
            }
        }
    }


    public Broker getBroker() {
        return _broker;
    }
    
    public DomBroker getDomBroker() {
        return _domBroker;
    }
    
    public EventSourceRegistry getEventSourceRegistry() {
        return _eventSourceRegistry;
    }
    
    public java.lang.Short getMessageGeneratePeriod() {
        return _messageGeneratePeriod;
    }
    
    public java.lang.String getMessageText() {
        return _messageText;
    }
    
    public java.lang.Short getNumberEventSources() {
        return _numberEventSources;
    }
    
    @SuppressWarnings("unchecked")
    public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> E getAugmentation(java.lang.Class<E> augmentationType) {
        if (augmentationType == null) {
            throw new IllegalArgumentException("Augmentation Type reference cannot be NULL!");
        }
        return (E) augmentation.get(augmentationType);
    }

    public HweventsourceBuilder setBroker(Broker value) {
        this._broker = value;
        return this;
    }
    
    public HweventsourceBuilder setDomBroker(DomBroker value) {
        this._domBroker = value;
        return this;
    }
    
    public HweventsourceBuilder setEventSourceRegistry(EventSourceRegistry value) {
        this._eventSourceRegistry = value;
        return this;
    }
    
    private static void checkMessageGeneratePeriodRange(final short value) {
        if (value >= (short)1 && value <= (short)10) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[1‥10]].", value));
    }
    
    public HweventsourceBuilder setMessageGeneratePeriod(java.lang.Short value) {
        if (value != null) {
            checkMessageGeneratePeriodRange(value);
        }
        this._messageGeneratePeriod = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _messageGeneratePeriod_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ONE, BigInteger.TEN));
        return ret;
    }
    
    public HweventsourceBuilder setMessageText(java.lang.String value) {
        if (value != null) {
            check_messageTextLength(value);
        }
        this._messageText = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _messageText_length() {
        List<Range<BigInteger>> ret = new ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ONE, BigInteger.valueOf(1024L)));
        return ret;
    }
    
    private static void checkNumberEventSourcesRange(final short value) {
        if (value >= (short)1 && value <= (short)20) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[1‥20]].", value));
    }
    
    public HweventsourceBuilder setNumberEventSources(java.lang.Short value) {
        if (value != null) {
            checkNumberEventSourcesRange(value);
        }
        this._numberEventSources = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _numberEventSources_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ONE, BigInteger.valueOf(20L)));
        return ret;
    }
    
    public HweventsourceBuilder addAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> augmentationType, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource> augmentation) {
        if (augmentation == null) {
            return removeAugmentation(augmentationType);
        }
    
        if (!(this.augmentation instanceof HashMap)) {
            this.augmentation = new HashMap<>();
        }
    
        this.augmentation.put(augmentationType, augmentation);
        return this;
    }
    
    public HweventsourceBuilder removeAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> augmentationType) {
        if (this.augmentation instanceof HashMap) {
            this.augmentation.remove(augmentationType);
        }
        return this;
    }

    public Hweventsource build() {
        return new HweventsourceImpl(this);
    }

    private static final class HweventsourceImpl implements Hweventsource {

        public java.lang.Class<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource> getImplementedInterface() {
            return org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource.class;
        }

        private final Broker _broker;
        private final DomBroker _domBroker;
        private final EventSourceRegistry _eventSourceRegistry;
        private final java.lang.Short _messageGeneratePeriod;
        private final java.lang.String _messageText;
        private final java.lang.Short _numberEventSources;

        private Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> augmentation = Collections.emptyMap();

        private HweventsourceImpl(HweventsourceBuilder base) {
            this._broker = base.getBroker();
            this._domBroker = base.getDomBroker();
            this._eventSourceRegistry = base.getEventSourceRegistry();
            this._messageGeneratePeriod = base.getMessageGeneratePeriod();
            this._messageText = base.getMessageText();
            this._numberEventSources = base.getNumberEventSources();
            switch (base.augmentation.size()) {
            case 0:
                this.augmentation = Collections.emptyMap();
                break;
            case 1:
                final Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> e = base.augmentation.entrySet().iterator().next();
                this.augmentation = Collections.<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>>singletonMap(e.getKey(), e.getValue());
                break;
            default :
                this.augmentation = new HashMap<>(base.augmentation);
            }
        }

        @Override
        public Broker getBroker() {
            return _broker;
        }
        
        @Override
        public DomBroker getDomBroker() {
            return _domBroker;
        }
        
        @Override
        public EventSourceRegistry getEventSourceRegistry() {
            return _eventSourceRegistry;
        }
        
        @Override
        public java.lang.Short getMessageGeneratePeriod() {
            return _messageGeneratePeriod;
        }
        
        @Override
        public java.lang.String getMessageText() {
            return _messageText;
        }
        
        @Override
        public java.lang.Short getNumberEventSources() {
            return _numberEventSources;
        }
        
        @SuppressWarnings("unchecked")
        @Override
        public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> E getAugmentation(java.lang.Class<E> augmentationType) {
            if (augmentationType == null) {
                throw new IllegalArgumentException("Augmentation Type reference cannot be NULL!");
            }
            return (E) augmentation.get(augmentationType);
        }

        private int hash = 0;
        private volatile boolean hashValid = false;
        
        @Override
        public int hashCode() {
            if (hashValid) {
                return hash;
            }
        
            final int prime = 31;
            int result = 1;
            result = prime * result + ((_broker == null) ? 0 : _broker.hashCode());
            result = prime * result + ((_domBroker == null) ? 0 : _domBroker.hashCode());
            result = prime * result + ((_eventSourceRegistry == null) ? 0 : _eventSourceRegistry.hashCode());
            result = prime * result + ((_messageGeneratePeriod == null) ? 0 : _messageGeneratePeriod.hashCode());
            result = prime * result + ((_messageText == null) ? 0 : _messageText.hashCode());
            result = prime * result + ((_numberEventSources == null) ? 0 : _numberEventSources.hashCode());
            result = prime * result + ((augmentation == null) ? 0 : augmentation.hashCode());
        
            hash = result;
            hashValid = true;
            return result;
        }

        @Override
        public boolean equals(java.lang.Object obj) {
            if (this == obj) {
                return true;
            }
            if (!(obj instanceof DataObject)) {
                return false;
            }
            if (!org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource.class.equals(((DataObject)obj).getImplementedInterface())) {
                return false;
            }
            org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource other = (org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource)obj;
            if (_broker == null) {
                if (other.getBroker() != null) {
                    return false;
                }
            } else if(!_broker.equals(other.getBroker())) {
                return false;
            }
            if (_domBroker == null) {
                if (other.getDomBroker() != null) {
                    return false;
                }
            } else if(!_domBroker.equals(other.getDomBroker())) {
                return false;
            }
            if (_eventSourceRegistry == null) {
                if (other.getEventSourceRegistry() != null) {
                    return false;
                }
            } else if(!_eventSourceRegistry.equals(other.getEventSourceRegistry())) {
                return false;
            }
            if (_messageGeneratePeriod == null) {
                if (other.getMessageGeneratePeriod() != null) {
                    return false;
                }
            } else if(!_messageGeneratePeriod.equals(other.getMessageGeneratePeriod())) {
                return false;
            }
            if (_messageText == null) {
                if (other.getMessageText() != null) {
                    return false;
                }
            } else if(!_messageText.equals(other.getMessageText())) {
                return false;
            }
            if (_numberEventSources == null) {
                if (other.getNumberEventSources() != null) {
                    return false;
                }
            } else if(!_numberEventSources.equals(other.getNumberEventSources())) {
                return false;
            }
            if (getClass() == obj.getClass()) {
                // Simple case: we are comparing against self
                HweventsourceImpl otherImpl = (HweventsourceImpl) obj;
                if (augmentation == null) {
                    if (otherImpl.augmentation != null) {
                        return false;
                    }
                } else if(!augmentation.equals(otherImpl.augmentation)) {
                    return false;
                }
            } else {
                // Hard case: compare our augments with presence there...
                for (Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.impl.rev141210.modules.module.configuration.Hweventsource>> e : augmentation.entrySet()) {
                    if (!e.getValue().equals(other.getAugmentation(e.getKey()))) {
                        return false;
                    }
                }
                // .. and give the other one the chance to do the same
                if (!obj.equals(this)) {
                    return false;
                }
            }
            return true;
        }

        @Override
        public java.lang.String toString() {
            java.lang.StringBuilder builder = new java.lang.StringBuilder ("Hweventsource [");
            boolean first = true;
        
            if (_broker != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_broker=");
                builder.append(_broker);
             }
            if (_domBroker != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_domBroker=");
                builder.append(_domBroker);
             }
            if (_eventSourceRegistry != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_eventSourceRegistry=");
                builder.append(_eventSourceRegistry);
             }
            if (_messageGeneratePeriod != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_messageGeneratePeriod=");
                builder.append(_messageGeneratePeriod);
             }
            if (_messageText != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_messageText=");
                builder.append(_messageText);
             }
            if (_numberEventSources != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_numberEventSources=");
                builder.append(_numberEventSources);
             }
            if (first) {
                first = false;
            } else {
                builder.append(", ");
            }
            builder.append("augmentation=");
            builder.append(augmentation.values());
            return builder.append(']').toString();
        }
    }

}
