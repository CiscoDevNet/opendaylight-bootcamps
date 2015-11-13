package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.caching.mountpoint.impl.rev141210;

import java.util.concurrent.ConcurrentHashMap;

import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.dom.store.impl.InMemoryDOMDataStore;
import org.opendaylight.controller.md.sal.dom.store.impl.InMemoryDOMDataStoreFactory;
import org.opendaylight.controller.sal.core.api.model.SchemaService;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier;
import org.opendaylight.yangtools.yang.model.api.Module;
import org.opendaylight.yangtools.yang.model.api.SchemaContext;
import org.opendaylight.yangtools.yang.model.api.SchemaContextListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InMemoryDeviceDOMDataStorePool {
	
	private static final Logger LOG = LoggerFactory.getLogger(InMemoryDeviceDOMDataStorePool.class);

	public static final int noOfDevice = 5;

	private ConcurrentHashMap<YangInstanceIdentifier, InMemoryDOMDataStore> pool;
	private int maxSize;
	private ConcurrentHashMap<YangInstanceIdentifier, Integer> lruCache;

	private InMemoryDOMDataStore configInMemoryDOMDataStore;
	private InMemoryDOMDataStore operationalMemoryDOMDataStore;

	public InMemoryDeviceDOMDataStorePool() {

		LOG.info("InMemoryDeviceDOMDataStorePool is created");
		this.maxSize = noOfDevice;
		this.pool = new ConcurrentHashMap<YangInstanceIdentifier, InMemoryDOMDataStore>();
		this.lruCache = new ConcurrentHashMap<YangInstanceIdentifier, Integer>();
	}

	public InMemoryDOMDataStore getInMemoryDOMDataStore(YangInstanceIdentifier piddd,SchemaContext schemaContext, final LogicalDatastoreType store) throws Exception {

		InMemoryDOMDataStore inMemoryDOMDataStore = this.pool.get(piddd);
		if (inMemoryDOMDataStore != null) {
			LOG.info("Get datasource from memory for device="+piddd.toString());
			for (YangInstanceIdentifier pid : this.lruCache.keySet()) {
				int times = this.lruCache.get(pid);
				this.lruCache.replace(pid, times + 1);
			}
			this.lruCache.replace(piddd, 1);
			return inMemoryDOMDataStore;
		} else {
			LOG.info("datasource from memory for device="+piddd.toString()+"  is not there. so adding it in the pool");
			SchemaService schemaService= createSchemaService(schemaContext);
			inMemoryDOMDataStore = initCache(piddd, schemaService, store);
			if (this.pool.size() == this.maxSize) {
				this.evictInMemoryDOMDataStore();

			}

			for (YangInstanceIdentifier pid : this.lruCache.keySet()) {
				int times = this.lruCache.get(pid);
				this.lruCache.replace(pid, times + 1);
			}

			this.lruCache.put(piddd, 1);
			this.pool.put(piddd, inMemoryDOMDataStore);
			return inMemoryDOMDataStore;
		}
	}

	private synchronized void evictInMemoryDOMDataStore() throws Exception {
		YangInstanceIdentifier temppid = null;
		int tempmax = 1;
		for (YangInstanceIdentifier pid : this.lruCache.keySet()) {
			int v = this.lruCache.get(pid);
			if (v >= tempmax) {
				temppid = pid;
				tempmax = v;
			}
		}
		if (temppid == null) {
			throw new Exception("Should exist victim page!\n");
		} else {
			for (YangInstanceIdentifier pid : this.lruCache.keySet()) {
				int times = this.lruCache.get(pid);
				this.lruCache.replace(pid, times + 1);
			}
			this.lruCache.remove(temppid);
			this.pool.remove(temppid);
		}
	}

	private InMemoryDOMDataStore initCache(YangInstanceIdentifier pid, SchemaService schemaService, final LogicalDatastoreType store) {

		switch (store) {
			case CONFIGURATION: {
				operationalMemoryDOMDataStore = InMemoryDOMDataStoreFactory.create(pid.toString() + "-DOM-OPER",
						schemaService);
				return operationalMemoryDOMDataStore;
			}
			case OPERATIONAL: {
				configInMemoryDOMDataStore = InMemoryDOMDataStoreFactory.create(pid.toString() + "-DOM-CFG", schemaService);
				return configInMemoryDOMDataStore;
			}
			}
		return null;

	}
	
	 private SchemaService createSchemaService(final SchemaContext schemaContext) {
	        return new SchemaService() {

	            @Override
	            public void addModule(Module module) {
	            }

	            @Override
	            public void removeModule(Module module) {

	            }

	            @Override
	            public SchemaContext getSessionContext() {
	                return schemaContext;
	            }

	            @Override
	            public SchemaContext getGlobalContext() {
	                return schemaContext;
	            }

	            @Override
	            public ListenerRegistration<SchemaContextListener> registerSchemaContextListener(final SchemaContextListener listener) {
	                listener.onGlobalContextUpdated(getGlobalContext());
	                return new ListenerRegistration<SchemaContextListener>() {
	                    @Override
	                    public void close() {

	                    }

	                    @Override
	                    public SchemaContextListener getInstance() {
	                        return listener;
	                    }
	                };
	            }
	        };
	    }


}
