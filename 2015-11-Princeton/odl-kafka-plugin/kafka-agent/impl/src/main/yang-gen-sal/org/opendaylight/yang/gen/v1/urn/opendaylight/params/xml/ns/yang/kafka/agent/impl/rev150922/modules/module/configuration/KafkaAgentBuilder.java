package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration;
import org.opendaylight.yangtools.yang.binding.Augmentation;
import org.opendaylight.yangtools.yang.binding.AugmentationHolder;
import org.opendaylight.yangtools.yang.binding.DataObject;
import java.util.HashMap;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.kafka.agent.BindingBroker;
import org.opendaylight.yangtools.concepts.Builder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.kafka.agent.DomBroker;
import java.util.Collections;
import java.util.Map;


/**
 * Class that builds {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent} instances.
 *
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent
 *
 */
public class KafkaAgentBuilder implements Builder <org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent> {

    private BindingBroker _bindingBroker;
    private DomBroker _domBroker;

    Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> augmentation = Collections.emptyMap();

    public KafkaAgentBuilder() {
    }

    public KafkaAgentBuilder(KafkaAgent base) {
        this._bindingBroker = base.getBindingBroker();
        this._domBroker = base.getDomBroker();
        if (base instanceof KafkaAgentImpl) {
            KafkaAgentImpl impl = (KafkaAgentImpl) base;
            if (!impl.augmentation.isEmpty()) {
                this.augmentation = new HashMap<>(impl.augmentation);
            }
        } else if (base instanceof AugmentationHolder) {
            @SuppressWarnings("unchecked")
            AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent> casted =(AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>) base;
            if (!casted.augmentations().isEmpty()) {
                this.augmentation = new HashMap<>(casted.augmentations());
            }
        }
    }


    public BindingBroker getBindingBroker() {
        return _bindingBroker;
    }
    
    public DomBroker getDomBroker() {
        return _domBroker;
    }
    
    @SuppressWarnings("unchecked")
    public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> E getAugmentation(java.lang.Class<E> augmentationType) {
        if (augmentationType == null) {
            throw new IllegalArgumentException("Augmentation Type reference cannot be NULL!");
        }
        return (E) augmentation.get(augmentationType);
    }

    public KafkaAgentBuilder setBindingBroker(BindingBroker value) {
        this._bindingBroker = value;
        return this;
    }
    
    public KafkaAgentBuilder setDomBroker(DomBroker value) {
        this._domBroker = value;
        return this;
    }
    
    public KafkaAgentBuilder addAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> augmentationType, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent> augmentation) {
        if (augmentation == null) {
            return removeAugmentation(augmentationType);
        }
    
        if (!(this.augmentation instanceof HashMap)) {
            this.augmentation = new HashMap<>();
        }
    
        this.augmentation.put(augmentationType, augmentation);
        return this;
    }
    
    public KafkaAgentBuilder removeAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> augmentationType) {
        if (this.augmentation instanceof HashMap) {
            this.augmentation.remove(augmentationType);
        }
        return this;
    }

    public KafkaAgent build() {
        return new KafkaAgentImpl(this);
    }

    private static final class KafkaAgentImpl implements KafkaAgent {

        public java.lang.Class<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent> getImplementedInterface() {
            return org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent.class;
        }

        private final BindingBroker _bindingBroker;
        private final DomBroker _domBroker;

        private Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> augmentation = Collections.emptyMap();

        private KafkaAgentImpl(KafkaAgentBuilder base) {
            this._bindingBroker = base.getBindingBroker();
            this._domBroker = base.getDomBroker();
            switch (base.augmentation.size()) {
            case 0:
                this.augmentation = Collections.emptyMap();
                break;
            case 1:
                final Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> e = base.augmentation.entrySet().iterator().next();
                this.augmentation = Collections.<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>>singletonMap(e.getKey(), e.getValue());
                break;
            default :
                this.augmentation = new HashMap<>(base.augmentation);
            }
        }

        @Override
        public BindingBroker getBindingBroker() {
            return _bindingBroker;
        }
        
        @Override
        public DomBroker getDomBroker() {
            return _domBroker;
        }
        
        @SuppressWarnings("unchecked")
        @Override
        public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> E getAugmentation(java.lang.Class<E> augmentationType) {
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
            result = prime * result + ((_bindingBroker == null) ? 0 : _bindingBroker.hashCode());
            result = prime * result + ((_domBroker == null) ? 0 : _domBroker.hashCode());
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
            if (!org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent.class.equals(((DataObject)obj).getImplementedInterface())) {
                return false;
            }
            org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent other = (org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent)obj;
            if (_bindingBroker == null) {
                if (other.getBindingBroker() != null) {
                    return false;
                }
            } else if(!_bindingBroker.equals(other.getBindingBroker())) {
                return false;
            }
            if (_domBroker == null) {
                if (other.getDomBroker() != null) {
                    return false;
                }
            } else if(!_domBroker.equals(other.getDomBroker())) {
                return false;
            }
            if (getClass() == obj.getClass()) {
                // Simple case: we are comparing against self
                KafkaAgentImpl otherImpl = (KafkaAgentImpl) obj;
                if (augmentation == null) {
                    if (otherImpl.augmentation != null) {
                        return false;
                    }
                } else if(!augmentation.equals(otherImpl.augmentation)) {
                    return false;
                }
            } else {
                // Hard case: compare our augments with presence there...
                for (Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.impl.rev150922.modules.module.configuration.KafkaAgent>> e : augmentation.entrySet()) {
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
            java.lang.StringBuilder builder = new java.lang.StringBuilder ("KafkaAgent [");
            boolean first = true;
        
            if (_bindingBroker != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_bindingBroker=");
                builder.append(_bindingBroker);
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
