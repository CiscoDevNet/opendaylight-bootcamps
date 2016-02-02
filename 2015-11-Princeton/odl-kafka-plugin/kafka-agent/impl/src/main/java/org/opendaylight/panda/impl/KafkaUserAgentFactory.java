/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.opendaylight.panda.impl;

import com.google.common.base.Preconditions;
import java.util.Collection;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.DataTreeChangeListener;
import org.opendaylight.controller.md.sal.binding.api.DataTreeIdentifier;
import org.opendaylight.controller.md.sal.binding.api.DataTreeModification;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.dom.api.DOMNotificationService;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.kafka.agent.rev150922.KafkaProducerConfig;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 *
 * @author williscc
 */
public class KafkaUserAgentFactory implements DataTreeChangeListener<KafkaProducerConfig>, AutoCloseable {

    private static final Logger LOG = LoggerFactory.getLogger(KafkaUserAgentFactory.class);
    
    
    private final ListenerRegistration<KafkaUserAgentFactory> kafkaProducerConfigReg;
    
    private final InstanceIdentifier<KafkaProducerConfig> KAFKA_PRODUCER_CONFIG_IID = InstanceIdentifier.builder(KafkaProducerConfig.class).build();
    private final DataTreeIdentifier<KafkaProducerConfig> KAFKA_CONFIG_PATH = new DataTreeIdentifier<>(LogicalDatastoreType.CONFIGURATION, KAFKA_PRODUCER_CONFIG_IID);
    
    private DataBroker dataBroker; //SAL data broker service
    private DOMNotificationService notificationService; //notification service
    
    private KafkaUserAgentImpl kafkaUserAgent; //singleton kafka user agent
    
    /**
     * Constructor
     * @param broker
     * @param notifyService 
     */
    public KafkaUserAgentFactory (final DataBroker broker, final DOMNotificationService notifyService)
    {
        if (LOG.isDebugEnabled())
        {
            LOG.debug("in KafkaUserAgentFactory()");
        }
        this.dataBroker = Preconditions.checkNotNull(broker, "broker");
        
        this.notificationService = Preconditions.checkNotNull(notifyService, "notifyService");
        
        //register as data change listener to data broker
        kafkaProducerConfigReg = broker.registerDataTreeChangeListener(KAFKA_CONFIG_PATH, this);
    }
    
    @Override
    public void close() throws Exception {
        if (LOG.isDebugEnabled())
        {
            LOG.debug("in close()");
        }
        kafkaUserAgent.close();
        kafkaProducerConfigReg.close();
    }

    
    @Override
    public void onDataTreeChanged(final Collection<DataTreeModification<KafkaProducerConfig>> changed) {
        
        if (LOG.isDebugEnabled())
        {
            LOG.debug("in onDataTreeChanged()");
        }
        
        DataTreeModification<KafkaProducerConfig> changedConfig = changed.iterator().next();
        
        KafkaProducerConfig config = changedConfig.getRootNode().getDataAfter();
        
        createOrReset(config);
        
    }

    //Private methods --
    private synchronized void createOrReset (KafkaProducerConfig config)
    {
        if (LOG.isDebugEnabled())
        {
            LOG.debug("in createOrReset()");
        }
        try{
            
            if (kafkaUserAgent != null)
            {
                LOG.info("closing pre-existed kafka user agent...");
                kafkaUserAgent.close();
            }
            
            LOG.info("create a new kafka user agent using configuration...");
            
            kafkaUserAgent = KafkaUserAgentImpl.create(notificationService, config);
            LOG.info("user agent reset.");
            
            
        }catch(Exception ex)
        {
            LOG.error(ex.getMessage(), ex);
        }
    }
}
