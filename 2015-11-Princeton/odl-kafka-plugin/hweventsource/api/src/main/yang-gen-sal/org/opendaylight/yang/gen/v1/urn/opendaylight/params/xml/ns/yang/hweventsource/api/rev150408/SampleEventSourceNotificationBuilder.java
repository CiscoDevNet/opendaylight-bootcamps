package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408;
import org.opendaylight.yangtools.yang.binding.Augmentation;
import org.opendaylight.yangtools.yang.binding.AugmentationHolder;
import org.opendaylight.yangtools.yang.binding.DataObject;
import java.util.HashMap;
import org.opendaylight.yangtools.concepts.Builder;
import java.util.ArrayList;
import java.math.BigInteger;
import java.util.List;
import java.util.Collections;
import com.google.common.collect.Range;
import java.util.Map;


/**
 * Class that builds {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification} instances.
 *
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification
 *
 */
public class SampleEventSourceNotificationBuilder implements Builder <org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification> {

    private java.lang.String _message;
    private SourceIdentifier _sourceId;
    private static void check_sourceIdLength(final String value) {
        final int length = value.length();
        if (length >= 1) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid length: %s, expected: [[1‥2147483647]].", value));
    }

    Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> augmentation = Collections.emptyMap();

    public SampleEventSourceNotificationBuilder() {
    }

    public SampleEventSourceNotificationBuilder(SampleEventSourceNotification base) {
        this._message = base.getMessage();
        this._sourceId = base.getSourceId();
        if (base instanceof SampleEventSourceNotificationImpl) {
            SampleEventSourceNotificationImpl impl = (SampleEventSourceNotificationImpl) base;
            if (!impl.augmentation.isEmpty()) {
                this.augmentation = new HashMap<>(impl.augmentation);
            }
        } else if (base instanceof AugmentationHolder) {
            @SuppressWarnings("unchecked")
            AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification> casted =(AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>) base;
            if (!casted.augmentations().isEmpty()) {
                this.augmentation = new HashMap<>(casted.augmentations());
            }
        }
    }


    public java.lang.String getMessage() {
        return _message;
    }
    
    public SourceIdentifier getSourceId() {
        return _sourceId;
    }
    
    @SuppressWarnings("unchecked")
    public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> E getAugmentation(java.lang.Class<E> augmentationType) {
        if (augmentationType == null) {
            throw new IllegalArgumentException("Augmentation Type reference cannot be NULL!");
        }
        return (E) augmentation.get(augmentationType);
    }

    public SampleEventSourceNotificationBuilder setMessage(java.lang.String value) {
        this._message = value;
        return this;
    }
    
    public SampleEventSourceNotificationBuilder setSourceId(SourceIdentifier value) {
        if (value != null) {
            check_sourceIdLength(value.getValue());
        }
        this._sourceId = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _sourceId_length() {
        List<Range<BigInteger>> ret = new ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ONE, BigInteger.valueOf(2147483647L)));
        return ret;
    }
    
    public SampleEventSourceNotificationBuilder addAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> augmentationType, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification> augmentation) {
        if (augmentation == null) {
            return removeAugmentation(augmentationType);
        }
    
        if (!(this.augmentation instanceof HashMap)) {
            this.augmentation = new HashMap<>();
        }
    
        this.augmentation.put(augmentationType, augmentation);
        return this;
    }
    
    public SampleEventSourceNotificationBuilder removeAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> augmentationType) {
        if (this.augmentation instanceof HashMap) {
            this.augmentation.remove(augmentationType);
        }
        return this;
    }

    public SampleEventSourceNotification build() {
        return new SampleEventSourceNotificationImpl(this);
    }

    private static final class SampleEventSourceNotificationImpl implements SampleEventSourceNotification {

        public java.lang.Class<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification> getImplementedInterface() {
            return org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification.class;
        }

        private final java.lang.String _message;
        private final SourceIdentifier _sourceId;

        private Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> augmentation = Collections.emptyMap();

        private SampleEventSourceNotificationImpl(SampleEventSourceNotificationBuilder base) {
            this._message = base.getMessage();
            this._sourceId = base.getSourceId();
            switch (base.augmentation.size()) {
            case 0:
                this.augmentation = Collections.emptyMap();
                break;
            case 1:
                final Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> e = base.augmentation.entrySet().iterator().next();
                this.augmentation = Collections.<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>>singletonMap(e.getKey(), e.getValue());
                break;
            default :
                this.augmentation = new HashMap<>(base.augmentation);
            }
        }

        @Override
        public java.lang.String getMessage() {
            return _message;
        }
        
        @Override
        public SourceIdentifier getSourceId() {
            return _sourceId;
        }
        
        @SuppressWarnings("unchecked")
        @Override
        public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> E getAugmentation(java.lang.Class<E> augmentationType) {
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
            result = prime * result + ((_message == null) ? 0 : _message.hashCode());
            result = prime * result + ((_sourceId == null) ? 0 : _sourceId.hashCode());
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
            if (!org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification.class.equals(((DataObject)obj).getImplementedInterface())) {
                return false;
            }
            org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification other = (org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification)obj;
            if (_message == null) {
                if (other.getMessage() != null) {
                    return false;
                }
            } else if(!_message.equals(other.getMessage())) {
                return false;
            }
            if (_sourceId == null) {
                if (other.getSourceId() != null) {
                    return false;
                }
            } else if(!_sourceId.equals(other.getSourceId())) {
                return false;
            }
            if (getClass() == obj.getClass()) {
                // Simple case: we are comparing against self
                SampleEventSourceNotificationImpl otherImpl = (SampleEventSourceNotificationImpl) obj;
                if (augmentation == null) {
                    if (otherImpl.augmentation != null) {
                        return false;
                    }
                } else if(!augmentation.equals(otherImpl.augmentation)) {
                    return false;
                }
            } else {
                // Hard case: compare our augments with presence there...
                for (Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.hweventsource.api.rev150408.SampleEventSourceNotification>> e : augmentation.entrySet()) {
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
            java.lang.StringBuilder builder = new java.lang.StringBuilder ("SampleEventSourceNotification [");
            boolean first = true;
        
            if (_message != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_message=");
                builder.append(_message);
             }
            if (_sourceId != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_sourceId=");
                builder.append(_sourceId);
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
