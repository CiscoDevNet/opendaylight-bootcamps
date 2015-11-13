package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.caching.mountpoint.impl.rev141210;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import javax.annotation.Nullable;

import org.opendaylight.controller.md.sal.common.api.TransactionStatus;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.common.api.data.ReadFailedException;
import org.opendaylight.controller.md.sal.common.api.data.TransactionCommitFailedException;
import org.opendaylight.controller.md.sal.dom.api.DOMDataBroker;
import org.opendaylight.controller.md.sal.dom.api.DOMDataReadOnlyTransaction;
import org.opendaylight.controller.md.sal.dom.api.DOMDataReadWriteTransaction;
import org.opendaylight.controller.md.sal.dom.api.DOMDataWriteTransaction;
import org.opendaylight.controller.md.sal.dom.store.impl.InMemoryDOMDataStore;
import org.opendaylight.controller.sal.core.spi.data.DOMStoreReadTransaction;
import org.opendaylight.controller.sal.core.spi.data.DOMStoreWriteTransaction;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier;
import org.opendaylight.yangtools.yang.data.api.schema.NormalizedNode;
import org.opendaylight.yangtools.yang.model.api.SchemaContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.common.base.Function;
import com.google.common.base.Optional;
import com.google.common.util.concurrent.CheckedFuture;
import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;

public class CachedDOMTransaction implements DOMDataReadWriteTransaction,DOMDataReadOnlyTransaction , DOMDataWriteTransaction{

	private static final Logger LOG = LoggerFactory.getLogger(CachedDOMTransaction.class);

	private DOMDataBroker domDataBroker;
    private SchemaContext schemaContext;
    InMemoryDeviceDOMDataStorePool pool;


    DOMDataWriteTransaction realDeviceTx;
    DOMDataReadOnlyTransaction domDataReadOnlyTransaction ;



	 public CachedDOMTransaction(final DOMDataBroker domDataBroker, final SchemaContext schemaContext,InMemoryDeviceDOMDataStorePool pool) {
	        this.domDataBroker = domDataBroker;
	        this.schemaContext = schemaContext;
	        this.pool=pool;
	        //initializeCache();
	    }

	@Override
	public CheckedFuture<Boolean, ReadFailedException> exists(final LogicalDatastoreType logicalDatastoreType, final YangInstanceIdentifier yangInstanceIdentifier) {
        final CheckedFuture<Optional<NormalizedNode<?, ?>>, ReadFailedException> read = read(
                logicalDatastoreType, yangInstanceIdentifier);

            final ListenableFuture<Boolean> transform = Futures
                .transform(read, new Function<Optional<NormalizedNode<?, ?>>, Boolean>() {
                    @Nullable @Override public Boolean apply(final Optional<NormalizedNode<?, ?>> input) {
                        return input.isPresent();
                    }
                });

            return Futures.makeChecked(transform, new Function<Exception, ReadFailedException>() {
                @Nullable @Override public ReadFailedException apply(final Exception e) {
                    return new ReadFailedException("Unable to read from cache", e);
                }
            });
        }

	@Override
	public CheckedFuture<Optional<NormalizedNode<?, ?>>, ReadFailedException> read(final LogicalDatastoreType logicalDatastoreType,
			final YangInstanceIdentifier yangInstanceIdentifier) {
    	// FIXME read from the right datastore

    	LOG.info("calling CachingDOMDataBroker.read for id ={}",yangInstanceIdentifier);
    	final InMemoryDOMDataStore dbStore;
    	CheckedFuture<Optional<NormalizedNode<?,?>>, ReadFailedException> dataFromMemory = null;
    	DOMStoreReadTransaction tr=null;
    	try {

    		dbStore = pool.getInMemoryDOMDataStore(yangInstanceIdentifier, schemaContext, logicalDatastoreType);

    		tr= dbStore.newReadOnlyTransaction();

    		dataFromMemory=tr.read(yangInstanceIdentifier);

    		LOG.info("data from the InMemoryDOMDataStore={}",dataFromMemory);

    		if(dataFromMemory==null){
    			final DOMDataReadOnlyTransaction domDataReadOnlyTransaction = domDataBroker.newReadOnlyTransaction();


    			final CheckedFuture<Optional<NormalizedNode<?, ?>>, ReadFailedException> cfgDataFuture = domDataReadOnlyTransaction
    					.read(logicalDatastoreType, yangInstanceIdentifier);

    			Futures.addCallback(cfgDataFuture, new FutureCallback<Optional<NormalizedNode<?, ?>>>() {

    				@Override public void onSuccess(final Optional<NormalizedNode<?, ?>> result) {
    					if(result.isPresent()) {
    						//     			                    LOG.
    						final NormalizedNode<?, ?> normalizedNode = result.get();
    						final DOMStoreWriteTransaction tx = dbStore.newWriteOnlyTransaction();
    						tx.write(yangInstanceIdentifier, normalizedNode);
    						tx.close();
    						LOG.info("added data in the newReadOnlyTransaction  to the InMemoryDOMDataStore for id={}",yangInstanceIdentifier);

    					}
    				}

    				@Override public void onFailure(final Throwable t) {
    					//     			                LOG.
    				}
    			});

    		}


    	} catch (Exception e) {
    		// TODO Auto-generated catch block
    		e.printStackTrace();
    	}

    	return tr.read(yangInstanceIdentifier);
    }

	@Override
	public Object getIdentifier() {
		// TODO Auto-generated method stub
		return this;
	}

	@Override
	public void merge(final LogicalDatastoreType logicalDatastoreType, final YangInstanceIdentifier yangInstanceIdentifier, final NormalizedNode<?, ?> normalizedNode) {

    	LOG.info("calling CachingDOMDataBroker.put for id ={}",yangInstanceIdentifier);

    	final InMemoryDOMDataStore dbStore;
    	try {
			dbStore = pool.getInMemoryDOMDataStore(yangInstanceIdentifier, schemaContext, logicalDatastoreType);

			realDeviceTx = domDataBroker.newWriteOnlyTransaction();
			realDeviceTx.merge(logicalDatastoreType, yangInstanceIdentifier, normalizedNode);

			final DOMStoreWriteTransaction txWrite = dbStore.newWriteOnlyTransaction();
            try {
            	txWrite.write(yangInstanceIdentifier, normalizedNode);
            	txWrite.close();
            	LOG.info("added data in the DOMDataWriteTransaction  to the InMemoryDOMDataStore for id={}",yangInstanceIdentifier);
            } catch (Exception e) {
                // TODO handle somehow: data is in device but not in cache!
            }


        // TODO block on edit to check state
      /*  try {
            final Void aVoid = submit.checkedGet(2, TimeUnit.MINUTES);
        } catch (TimeoutException | TransactionCommitFailedException e) {
            throw new RuntimeException(e);
        }*/

    	} catch (Exception e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}


    }

	@Override
	public void put(final LogicalDatastoreType logicalDatastoreType, final YangInstanceIdentifier yangInstanceIdentifier, final NormalizedNode<?, ?> normalizedNode) {

    	LOG.info("calling CachingDOMDataBroker.put for id ={}",yangInstanceIdentifier);

    	final InMemoryDOMDataStore dbStore;
    	try {
			dbStore = pool.getInMemoryDOMDataStore(yangInstanceIdentifier, schemaContext, logicalDatastoreType);

       realDeviceTx = domDataBroker.newWriteOnlyTransaction();
        realDeviceTx.put(logicalDatastoreType, yangInstanceIdentifier, normalizedNode);
        final DOMStoreWriteTransaction txWrite = dbStore.newWriteOnlyTransaction();
        try {
        	txWrite.write(yangInstanceIdentifier, normalizedNode);
        	txWrite.close();
        	LOG.info("added data in the DOMDataWriteTransaction  to the InMemoryDOMDataStore for id={}",yangInstanceIdentifier);
        } catch (Exception e) {
            // TODO handle somehow: data is in device but not in cache!
        }
        /*final CheckedFuture<Void, TransactionCommitFailedException> submit = realDeviceTx.submit();

        Futures.addCallback(submit, new FutureCallback<Void>() {

            @Override public void onSuccess(@Nullable final Void result) {
                // TODO Store in cache

                final DOMStoreWriteTransaction txWrite = dbStore.newWriteOnlyTransaction();
                try {
                	txWrite.write(yangInstanceIdentifier, normalizedNode);
                	txWrite.close();
                	LOG.info("added data in the DOMDataWriteTransaction  to the InMemoryDOMDataStore for id={}",yangInstanceIdentifier);
                } catch (Exception e) {
                    // TODO handle somehow: data is in device but not in cache!
                }

            }

            @Override public void onFailure(final Throwable t) {
                // LOG.
            }
        });

        // TODO block on edit to check state
        try {
            final Void aVoid = submit.checkedGet(2, TimeUnit.MINUTES);
        } catch (TimeoutException | TransactionCommitFailedException e) {
            throw new RuntimeException(e);
        }*/

    	} catch (Exception e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}


    }

	@Override
	public boolean cancel() {
		// TODO Auto-generated method stub
		return realDeviceTx.cancel();
	}

	@Override
	public ListenableFuture<RpcResult<TransactionStatus>> commit() {
		// TODO Auto-generated method stub
		return realDeviceTx.commit();
	}

	@Override
	public void delete(LogicalDatastoreType arg0, YangInstanceIdentifier arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public CheckedFuture<Void, TransactionCommitFailedException> submit() {
		// TODO Auto-generated method stub
		 final CheckedFuture<Void, TransactionCommitFailedException> submit = realDeviceTx.submit();
		return submit;
	}

	@Override
	public void close() {
		LOG.info("Close the connection");

	}

}
