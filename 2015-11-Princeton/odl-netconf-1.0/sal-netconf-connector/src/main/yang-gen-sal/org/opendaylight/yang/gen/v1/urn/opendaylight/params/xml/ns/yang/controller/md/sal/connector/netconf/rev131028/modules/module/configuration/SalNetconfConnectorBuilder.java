package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration;
import org.opendaylight.yangtools.yang.binding.AugmentationHolder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.ProcessingExecutor;
import java.util.HashMap;
import org.opendaylight.yangtools.concepts.Builder;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.Host;
import com.google.common.collect.Range;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.DomRegistry;
import java.math.BigDecimal;
import org.opendaylight.yangtools.yang.binding.Augmentation;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.EventExecutor;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.KeepaliveExecutor;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.YangModuleCapabilities;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.BindingRegistry;
import java.math.BigInteger;
import java.util.List;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.sal.netconf.connector.ClientDispatcher;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.inet.types.rev100924.PortNumber;
import java.util.Collections;
import java.util.Map;


/**
 * Class that builds {@link org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector} instances.
 *
 * @see org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector
 *
 */
public class SalNetconfConnectorBuilder implements Builder <org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector> {

    private Host _address;
    private java.lang.Integer _betweenAttemptsTimeoutMillis;
    private BindingRegistry _bindingRegistry;
    private ClientDispatcher _clientDispatcher;
    private java.lang.Long _connectionTimeoutMillis;
    private java.lang.Long _defaultRequestTimeoutMillis;
    private DomRegistry _domRegistry;
    private EventExecutor _eventExecutor;
    private java.lang.Long _keepaliveDelay;
    private KeepaliveExecutor _keepaliveExecutor;
    private java.lang.Long _maxConnectionAttempts;
    private java.lang.String _password;
    private PortNumber _port;
    private ProcessingExecutor _processingExecutor;
    private BigDecimal _sleepFactor;
    private java.lang.String _username;
    private YangModuleCapabilities _yangModuleCapabilities;
    private java.lang.Boolean _reconnectOnChangedSchema;
    private java.lang.Boolean _tcpOnly;

    Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> augmentation = Collections.emptyMap();

    public SalNetconfConnectorBuilder() {
    }

    public SalNetconfConnectorBuilder(SalNetconfConnector base) {
        this._address = base.getAddress();
        this._betweenAttemptsTimeoutMillis = base.getBetweenAttemptsTimeoutMillis();
        this._bindingRegistry = base.getBindingRegistry();
        this._clientDispatcher = base.getClientDispatcher();
        this._connectionTimeoutMillis = base.getConnectionTimeoutMillis();
        this._defaultRequestTimeoutMillis = base.getDefaultRequestTimeoutMillis();
        this._domRegistry = base.getDomRegistry();
        this._eventExecutor = base.getEventExecutor();
        this._keepaliveDelay = base.getKeepaliveDelay();
        this._keepaliveExecutor = base.getKeepaliveExecutor();
        this._maxConnectionAttempts = base.getMaxConnectionAttempts();
        this._password = base.getPassword();
        this._port = base.getPort();
        this._processingExecutor = base.getProcessingExecutor();
        this._sleepFactor = base.getSleepFactor();
        this._username = base.getUsername();
        this._yangModuleCapabilities = base.getYangModuleCapabilities();
        this._reconnectOnChangedSchema = base.isReconnectOnChangedSchema();
        this._tcpOnly = base.isTcpOnly();
        if (base instanceof SalNetconfConnectorImpl) {
            SalNetconfConnectorImpl impl = (SalNetconfConnectorImpl) base;
            if (!impl.augmentation.isEmpty()) {
                this.augmentation = new HashMap<>(impl.augmentation);
            }
        } else if (base instanceof AugmentationHolder) {
            @SuppressWarnings("unchecked")
            AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector> casted =(AugmentationHolder<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>) base;
            if (!casted.augmentations().isEmpty()) {
                this.augmentation = new HashMap<>(casted.augmentations());
            }
        }
    }


    public Host getAddress() {
        return _address;
    }
    
    public java.lang.Integer getBetweenAttemptsTimeoutMillis() {
        return _betweenAttemptsTimeoutMillis;
    }
    
    public BindingRegistry getBindingRegistry() {
        return _bindingRegistry;
    }
    
    public ClientDispatcher getClientDispatcher() {
        return _clientDispatcher;
    }
    
    public java.lang.Long getConnectionTimeoutMillis() {
        return _connectionTimeoutMillis;
    }
    
    public java.lang.Long getDefaultRequestTimeoutMillis() {
        return _defaultRequestTimeoutMillis;
    }
    
    public DomRegistry getDomRegistry() {
        return _domRegistry;
    }
    
    public EventExecutor getEventExecutor() {
        return _eventExecutor;
    }
    
    public java.lang.Long getKeepaliveDelay() {
        return _keepaliveDelay;
    }
    
    public KeepaliveExecutor getKeepaliveExecutor() {
        return _keepaliveExecutor;
    }
    
    public java.lang.Long getMaxConnectionAttempts() {
        return _maxConnectionAttempts;
    }
    
    public java.lang.String getPassword() {
        return _password;
    }
    
    public PortNumber getPort() {
        return _port;
    }
    
    public ProcessingExecutor getProcessingExecutor() {
        return _processingExecutor;
    }
    
    public BigDecimal getSleepFactor() {
        return _sleepFactor;
    }
    
    public java.lang.String getUsername() {
        return _username;
    }
    
    public YangModuleCapabilities getYangModuleCapabilities() {
        return _yangModuleCapabilities;
    }
    
    public java.lang.Boolean isReconnectOnChangedSchema() {
        return _reconnectOnChangedSchema;
    }
    
    public java.lang.Boolean isTcpOnly() {
        return _tcpOnly;
    }
    
    @SuppressWarnings("unchecked")
    public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> E getAugmentation(java.lang.Class<E> augmentationType) {
        if (augmentationType == null) {
            throw new IllegalArgumentException("Augmentation Type reference cannot be NULL!");
        }
        return (E) augmentation.get(augmentationType);
    }

    public SalNetconfConnectorBuilder setAddress(Host value) {
        if (value != null) {
        }
        this._address = value;
        return this;
    }
    
    private static void checkBetweenAttemptsTimeoutMillisRange(final int value) {
        if (value >= 0 && value <= 65535) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥65535]].", value));
    }
    
    public SalNetconfConnectorBuilder setBetweenAttemptsTimeoutMillis(java.lang.Integer value) {
        if (value != null) {
            checkBetweenAttemptsTimeoutMillisRange(value);
        }
        this._betweenAttemptsTimeoutMillis = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _betweenAttemptsTimeoutMillis_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(65535L)));
        return ret;
    }
    
    public SalNetconfConnectorBuilder setBindingRegistry(BindingRegistry value) {
        this._bindingRegistry = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setClientDispatcher(ClientDispatcher value) {
        this._clientDispatcher = value;
        return this;
    }
    
    private static void checkConnectionTimeoutMillisRange(final long value) {
        if (value >= 0L && value <= 4294967295L) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥4294967295]].", value));
    }
    
    public SalNetconfConnectorBuilder setConnectionTimeoutMillis(java.lang.Long value) {
        if (value != null) {
            checkConnectionTimeoutMillisRange(value);
        }
        this._connectionTimeoutMillis = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _connectionTimeoutMillis_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(4294967295L)));
        return ret;
    }
    
    private static void checkDefaultRequestTimeoutMillisRange(final long value) {
        if (value >= 0L && value <= 4294967295L) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥4294967295]].", value));
    }
    
    public SalNetconfConnectorBuilder setDefaultRequestTimeoutMillis(java.lang.Long value) {
        if (value != null) {
            checkDefaultRequestTimeoutMillisRange(value);
        }
        this._defaultRequestTimeoutMillis = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _defaultRequestTimeoutMillis_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(4294967295L)));
        return ret;
    }
    
    public SalNetconfConnectorBuilder setDomRegistry(DomRegistry value) {
        this._domRegistry = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setEventExecutor(EventExecutor value) {
        this._eventExecutor = value;
        return this;
    }
    
    private static void checkKeepaliveDelayRange(final long value) {
        if (value >= 0L && value <= 4294967295L) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥4294967295]].", value));
    }
    
    public SalNetconfConnectorBuilder setKeepaliveDelay(java.lang.Long value) {
        if (value != null) {
            checkKeepaliveDelayRange(value);
        }
        this._keepaliveDelay = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _keepaliveDelay_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(4294967295L)));
        return ret;
    }
    
    public SalNetconfConnectorBuilder setKeepaliveExecutor(KeepaliveExecutor value) {
        this._keepaliveExecutor = value;
        return this;
    }
    
    private static void checkMaxConnectionAttemptsRange(final long value) {
        if (value >= 0L && value <= 4294967295L) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥4294967295]].", value));
    }
    
    public SalNetconfConnectorBuilder setMaxConnectionAttempts(java.lang.Long value) {
        if (value != null) {
            checkMaxConnectionAttemptsRange(value);
        }
        this._maxConnectionAttempts = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _maxConnectionAttempts_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(4294967295L)));
        return ret;
    }
    
    public SalNetconfConnectorBuilder setPassword(java.lang.String value) {
        this._password = value;
        return this;
    }
    
    private static void checkPortRange(final int value) {
        if (value >= 0 && value <= 65535) {
            return;
        }
        throw new IllegalArgumentException(String.format("Invalid range: %s, expected: [[0‥65535]].", value));
    }
    
    public SalNetconfConnectorBuilder setPort(PortNumber value) {
        if (value != null) {
            checkPortRange(value.getValue());
        }
        this._port = value;
        return this;
    }
    /**
     * @deprecated This method is slated for removal in a future release. See BUG-1485 for details.
     */
    @Deprecated
    public static List<Range<BigInteger>> _port_range() {
        final List<Range<BigInteger>> ret = new java.util.ArrayList<>(1);
        ret.add(Range.closed(BigInteger.ZERO, BigInteger.valueOf(65535L)));
        return ret;
    }
    
    public SalNetconfConnectorBuilder setProcessingExecutor(ProcessingExecutor value) {
        this._processingExecutor = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setSleepFactor(BigDecimal value) {
        this._sleepFactor = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setUsername(java.lang.String value) {
        this._username = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setYangModuleCapabilities(YangModuleCapabilities value) {
        this._yangModuleCapabilities = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setReconnectOnChangedSchema(java.lang.Boolean value) {
        this._reconnectOnChangedSchema = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder setTcpOnly(java.lang.Boolean value) {
        this._tcpOnly = value;
        return this;
    }
    
    public SalNetconfConnectorBuilder addAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> augmentationType, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector> augmentation) {
        if (augmentation == null) {
            return removeAugmentation(augmentationType);
        }
    
        if (!(this.augmentation instanceof HashMap)) {
            this.augmentation = new HashMap<>();
        }
    
        this.augmentation.put(augmentationType, augmentation);
        return this;
    }
    
    public SalNetconfConnectorBuilder removeAugmentation(java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> augmentationType) {
        if (this.augmentation instanceof HashMap) {
            this.augmentation.remove(augmentationType);
        }
        return this;
    }

    public SalNetconfConnector build() {
        return new SalNetconfConnectorImpl(this);
    }

    private static final class SalNetconfConnectorImpl implements SalNetconfConnector {

        public java.lang.Class<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector> getImplementedInterface() {
            return org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector.class;
        }

        private final Host _address;
        private final java.lang.Integer _betweenAttemptsTimeoutMillis;
        private final BindingRegistry _bindingRegistry;
        private final ClientDispatcher _clientDispatcher;
        private final java.lang.Long _connectionTimeoutMillis;
        private final java.lang.Long _defaultRequestTimeoutMillis;
        private final DomRegistry _domRegistry;
        private final EventExecutor _eventExecutor;
        private final java.lang.Long _keepaliveDelay;
        private final KeepaliveExecutor _keepaliveExecutor;
        private final java.lang.Long _maxConnectionAttempts;
        private final java.lang.String _password;
        private final PortNumber _port;
        private final ProcessingExecutor _processingExecutor;
        private final BigDecimal _sleepFactor;
        private final java.lang.String _username;
        private final YangModuleCapabilities _yangModuleCapabilities;
        private final java.lang.Boolean _reconnectOnChangedSchema;
        private final java.lang.Boolean _tcpOnly;

        private Map<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> augmentation = Collections.emptyMap();

        private SalNetconfConnectorImpl(SalNetconfConnectorBuilder base) {
            this._address = base.getAddress();
            this._betweenAttemptsTimeoutMillis = base.getBetweenAttemptsTimeoutMillis();
            this._bindingRegistry = base.getBindingRegistry();
            this._clientDispatcher = base.getClientDispatcher();
            this._connectionTimeoutMillis = base.getConnectionTimeoutMillis();
            this._defaultRequestTimeoutMillis = base.getDefaultRequestTimeoutMillis();
            this._domRegistry = base.getDomRegistry();
            this._eventExecutor = base.getEventExecutor();
            this._keepaliveDelay = base.getKeepaliveDelay();
            this._keepaliveExecutor = base.getKeepaliveExecutor();
            this._maxConnectionAttempts = base.getMaxConnectionAttempts();
            this._password = base.getPassword();
            this._port = base.getPort();
            this._processingExecutor = base.getProcessingExecutor();
            this._sleepFactor = base.getSleepFactor();
            this._username = base.getUsername();
            this._yangModuleCapabilities = base.getYangModuleCapabilities();
            this._reconnectOnChangedSchema = base.isReconnectOnChangedSchema();
            this._tcpOnly = base.isTcpOnly();
            switch (base.augmentation.size()) {
            case 0:
                this.augmentation = Collections.emptyMap();
                break;
            case 1:
                final Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> e = base.augmentation.entrySet().iterator().next();
                this.augmentation = Collections.<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>>singletonMap(e.getKey(), e.getValue());
                break;
            default :
                this.augmentation = new HashMap<>(base.augmentation);
            }
        }

        @Override
        public Host getAddress() {
            return _address;
        }
        
        @Override
        public java.lang.Integer getBetweenAttemptsTimeoutMillis() {
            return _betweenAttemptsTimeoutMillis;
        }
        
        @Override
        public BindingRegistry getBindingRegistry() {
            return _bindingRegistry;
        }
        
        @Override
        public ClientDispatcher getClientDispatcher() {
            return _clientDispatcher;
        }
        
        @Override
        public java.lang.Long getConnectionTimeoutMillis() {
            return _connectionTimeoutMillis;
        }
        
        @Override
        public java.lang.Long getDefaultRequestTimeoutMillis() {
            return _defaultRequestTimeoutMillis;
        }
        
        @Override
        public DomRegistry getDomRegistry() {
            return _domRegistry;
        }
        
        @Override
        public EventExecutor getEventExecutor() {
            return _eventExecutor;
        }
        
        @Override
        public java.lang.Long getKeepaliveDelay() {
            return _keepaliveDelay;
        }
        
        @Override
        public KeepaliveExecutor getKeepaliveExecutor() {
            return _keepaliveExecutor;
        }
        
        @Override
        public java.lang.Long getMaxConnectionAttempts() {
            return _maxConnectionAttempts;
        }
        
        @Override
        public java.lang.String getPassword() {
            return _password;
        }
        
        @Override
        public PortNumber getPort() {
            return _port;
        }
        
        @Override
        public ProcessingExecutor getProcessingExecutor() {
            return _processingExecutor;
        }
        
        @Override
        public BigDecimal getSleepFactor() {
            return _sleepFactor;
        }
        
        @Override
        public java.lang.String getUsername() {
            return _username;
        }
        
        @Override
        public YangModuleCapabilities getYangModuleCapabilities() {
            return _yangModuleCapabilities;
        }
        
        @Override
        public java.lang.Boolean isReconnectOnChangedSchema() {
            return _reconnectOnChangedSchema;
        }
        
        @Override
        public java.lang.Boolean isTcpOnly() {
            return _tcpOnly;
        }
        
        @SuppressWarnings("unchecked")
        @Override
        public <E extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> E getAugmentation(java.lang.Class<E> augmentationType) {
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
            result = prime * result + ((_address == null) ? 0 : _address.hashCode());
            result = prime * result + ((_betweenAttemptsTimeoutMillis == null) ? 0 : _betweenAttemptsTimeoutMillis.hashCode());
            result = prime * result + ((_bindingRegistry == null) ? 0 : _bindingRegistry.hashCode());
            result = prime * result + ((_clientDispatcher == null) ? 0 : _clientDispatcher.hashCode());
            result = prime * result + ((_connectionTimeoutMillis == null) ? 0 : _connectionTimeoutMillis.hashCode());
            result = prime * result + ((_defaultRequestTimeoutMillis == null) ? 0 : _defaultRequestTimeoutMillis.hashCode());
            result = prime * result + ((_domRegistry == null) ? 0 : _domRegistry.hashCode());
            result = prime * result + ((_eventExecutor == null) ? 0 : _eventExecutor.hashCode());
            result = prime * result + ((_keepaliveDelay == null) ? 0 : _keepaliveDelay.hashCode());
            result = prime * result + ((_keepaliveExecutor == null) ? 0 : _keepaliveExecutor.hashCode());
            result = prime * result + ((_maxConnectionAttempts == null) ? 0 : _maxConnectionAttempts.hashCode());
            result = prime * result + ((_password == null) ? 0 : _password.hashCode());
            result = prime * result + ((_port == null) ? 0 : _port.hashCode());
            result = prime * result + ((_processingExecutor == null) ? 0 : _processingExecutor.hashCode());
            result = prime * result + ((_sleepFactor == null) ? 0 : _sleepFactor.hashCode());
            result = prime * result + ((_username == null) ? 0 : _username.hashCode());
            result = prime * result + ((_yangModuleCapabilities == null) ? 0 : _yangModuleCapabilities.hashCode());
            result = prime * result + ((_reconnectOnChangedSchema == null) ? 0 : _reconnectOnChangedSchema.hashCode());
            result = prime * result + ((_tcpOnly == null) ? 0 : _tcpOnly.hashCode());
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
            if (!org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector.class.equals(((DataObject)obj).getImplementedInterface())) {
                return false;
            }
            org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector other = (org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector)obj;
            if (_address == null) {
                if (other.getAddress() != null) {
                    return false;
                }
            } else if(!_address.equals(other.getAddress())) {
                return false;
            }
            if (_betweenAttemptsTimeoutMillis == null) {
                if (other.getBetweenAttemptsTimeoutMillis() != null) {
                    return false;
                }
            } else if(!_betweenAttemptsTimeoutMillis.equals(other.getBetweenAttemptsTimeoutMillis())) {
                return false;
            }
            if (_bindingRegistry == null) {
                if (other.getBindingRegistry() != null) {
                    return false;
                }
            } else if(!_bindingRegistry.equals(other.getBindingRegistry())) {
                return false;
            }
            if (_clientDispatcher == null) {
                if (other.getClientDispatcher() != null) {
                    return false;
                }
            } else if(!_clientDispatcher.equals(other.getClientDispatcher())) {
                return false;
            }
            if (_connectionTimeoutMillis == null) {
                if (other.getConnectionTimeoutMillis() != null) {
                    return false;
                }
            } else if(!_connectionTimeoutMillis.equals(other.getConnectionTimeoutMillis())) {
                return false;
            }
            if (_defaultRequestTimeoutMillis == null) {
                if (other.getDefaultRequestTimeoutMillis() != null) {
                    return false;
                }
            } else if(!_defaultRequestTimeoutMillis.equals(other.getDefaultRequestTimeoutMillis())) {
                return false;
            }
            if (_domRegistry == null) {
                if (other.getDomRegistry() != null) {
                    return false;
                }
            } else if(!_domRegistry.equals(other.getDomRegistry())) {
                return false;
            }
            if (_eventExecutor == null) {
                if (other.getEventExecutor() != null) {
                    return false;
                }
            } else if(!_eventExecutor.equals(other.getEventExecutor())) {
                return false;
            }
            if (_keepaliveDelay == null) {
                if (other.getKeepaliveDelay() != null) {
                    return false;
                }
            } else if(!_keepaliveDelay.equals(other.getKeepaliveDelay())) {
                return false;
            }
            if (_keepaliveExecutor == null) {
                if (other.getKeepaliveExecutor() != null) {
                    return false;
                }
            } else if(!_keepaliveExecutor.equals(other.getKeepaliveExecutor())) {
                return false;
            }
            if (_maxConnectionAttempts == null) {
                if (other.getMaxConnectionAttempts() != null) {
                    return false;
                }
            } else if(!_maxConnectionAttempts.equals(other.getMaxConnectionAttempts())) {
                return false;
            }
            if (_password == null) {
                if (other.getPassword() != null) {
                    return false;
                }
            } else if(!_password.equals(other.getPassword())) {
                return false;
            }
            if (_port == null) {
                if (other.getPort() != null) {
                    return false;
                }
            } else if(!_port.equals(other.getPort())) {
                return false;
            }
            if (_processingExecutor == null) {
                if (other.getProcessingExecutor() != null) {
                    return false;
                }
            } else if(!_processingExecutor.equals(other.getProcessingExecutor())) {
                return false;
            }
            if (_sleepFactor == null) {
                if (other.getSleepFactor() != null) {
                    return false;
                }
            } else if(!_sleepFactor.equals(other.getSleepFactor())) {
                return false;
            }
            if (_username == null) {
                if (other.getUsername() != null) {
                    return false;
                }
            } else if(!_username.equals(other.getUsername())) {
                return false;
            }
            if (_yangModuleCapabilities == null) {
                if (other.getYangModuleCapabilities() != null) {
                    return false;
                }
            } else if(!_yangModuleCapabilities.equals(other.getYangModuleCapabilities())) {
                return false;
            }
            if (_reconnectOnChangedSchema == null) {
                if (other.isReconnectOnChangedSchema() != null) {
                    return false;
                }
            } else if(!_reconnectOnChangedSchema.equals(other.isReconnectOnChangedSchema())) {
                return false;
            }
            if (_tcpOnly == null) {
                if (other.isTcpOnly() != null) {
                    return false;
                }
            } else if(!_tcpOnly.equals(other.isTcpOnly())) {
                return false;
            }
            if (getClass() == obj.getClass()) {
                // Simple case: we are comparing against self
                SalNetconfConnectorImpl otherImpl = (SalNetconfConnectorImpl) obj;
                if (augmentation == null) {
                    if (otherImpl.augmentation != null) {
                        return false;
                    }
                } else if(!augmentation.equals(otherImpl.augmentation)) {
                    return false;
                }
            } else {
                // Hard case: compare our augments with presence there...
                for (Map.Entry<java.lang.Class<? extends Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>>, Augmentation<org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.controller.md.sal.connector.netconf.rev131028.modules.module.configuration.SalNetconfConnector>> e : augmentation.entrySet()) {
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
            java.lang.StringBuilder builder = new java.lang.StringBuilder ("SalNetconfConnector [");
            boolean first = true;
        
            if (_address != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_address=");
                builder.append(_address);
             }
            if (_betweenAttemptsTimeoutMillis != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_betweenAttemptsTimeoutMillis=");
                builder.append(_betweenAttemptsTimeoutMillis);
             }
            if (_bindingRegistry != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_bindingRegistry=");
                builder.append(_bindingRegistry);
             }
            if (_clientDispatcher != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_clientDispatcher=");
                builder.append(_clientDispatcher);
             }
            if (_connectionTimeoutMillis != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_connectionTimeoutMillis=");
                builder.append(_connectionTimeoutMillis);
             }
            if (_defaultRequestTimeoutMillis != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_defaultRequestTimeoutMillis=");
                builder.append(_defaultRequestTimeoutMillis);
             }
            if (_domRegistry != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_domRegistry=");
                builder.append(_domRegistry);
             }
            if (_eventExecutor != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_eventExecutor=");
                builder.append(_eventExecutor);
             }
            if (_keepaliveDelay != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_keepaliveDelay=");
                builder.append(_keepaliveDelay);
             }
            if (_keepaliveExecutor != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_keepaliveExecutor=");
                builder.append(_keepaliveExecutor);
             }
            if (_maxConnectionAttempts != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_maxConnectionAttempts=");
                builder.append(_maxConnectionAttempts);
             }
            if (_password != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_password=");
                builder.append(_password);
             }
            if (_port != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_port=");
                builder.append(_port);
             }
            if (_processingExecutor != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_processingExecutor=");
                builder.append(_processingExecutor);
             }
            if (_sleepFactor != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_sleepFactor=");
                builder.append(_sleepFactor);
             }
            if (_username != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_username=");
                builder.append(_username);
             }
            if (_yangModuleCapabilities != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_yangModuleCapabilities=");
                builder.append(_yangModuleCapabilities);
             }
            if (_reconnectOnChangedSchema != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_reconnectOnChangedSchema=");
                builder.append(_reconnectOnChangedSchema);
             }
            if (_tcpOnly != null) {
                if (first) {
                    first = false;
                } else {
                    builder.append(", ");
                }
                builder.append("_tcpOnly=");
                builder.append(_tcpOnly);
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
