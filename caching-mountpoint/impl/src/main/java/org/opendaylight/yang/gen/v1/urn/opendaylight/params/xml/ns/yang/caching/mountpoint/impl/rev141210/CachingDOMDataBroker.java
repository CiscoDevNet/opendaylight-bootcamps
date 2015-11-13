package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.caching.mountpoint.impl.rev141210;

import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

import javax.annotation.Nonnull;
import javax.annotation.Nullable;

import org.opendaylight.controller.md.sal.common.api.TransactionStatus;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.common.api.data.ReadFailedException;
import org.opendaylight.controller.md.sal.common.api.data.TransactionChainListener;
import org.opendaylight.controller.md.sal.common.api.data.TransactionCommitFailedException;
import org.opendaylight.controller.md.sal.dom.api.DOMDataBroker;
import org.opendaylight.controller.md.sal.dom.api.DOMDataBrokerExtension;
import org.opendaylight.controller.md.sal.dom.api.DOMDataChangeListener;
import org.opendaylight.controller.md.sal.dom.api.DOMDataReadOnlyTransaction;
import org.opendaylight.controller.md.sal.dom.api.DOMDataReadWriteTransaction;
import org.opendaylight.controller.md.sal.dom.api.DOMDataWriteTransaction;
import org.opendaylight.controller.md.sal.dom.api.DOMTransactionChain;
import org.opendaylight.controller.md.sal.dom.store.impl.InMemoryDOMDataStore;
import org.opendaylight.controller.md.sal.dom.store.impl.InMemoryDOMDataStoreFactory;
import org.opendaylight.controller.sal.core.spi.data.DOMStoreReadTransaction;
import org.opendaylight.controller.sal.core.spi.data.DOMStoreWriteTransaction;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
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

/**
 * Created by mmarsale on 5.11.2015.
 */
public class CachingDOMDataBroker implements DOMDataBroker {

	private static final Logger LOG = LoggerFactory.getLogger(CachingDOMDataBroker.class);

    private DOMDataBroker domDataBroker;
    private SchemaContext schemaContext;
    InMemoryDeviceDOMDataStorePool pool;
    private CachedDOMTransaction cachedtrx;

    public CachingDOMDataBroker(final DOMDataBroker domDataBroker, final SchemaContext schemaContext) {
        this.domDataBroker = domDataBroker;
        this.schemaContext = schemaContext;
        pool=new InMemoryDeviceDOMDataStorePool();
        //initializeCache();
    }

    private void initializeCache() {
        final DOMDataReadOnlyTransaction domDataReadOnlyTransaction = domDataBroker.newReadOnlyTransaction();

        // fill the datastores
        final CheckedFuture<Optional<NormalizedNode<?, ?>>, ReadFailedException> cfgDataFuture = domDataReadOnlyTransaction
            .read(LogicalDatastoreType.CONFIGURATION, YangInstanceIdentifier.EMPTY);

        final CheckedFuture<Optional<NormalizedNode<?, ?>>, ReadFailedException> operDataFuture = domDataReadOnlyTransaction
            .read(LogicalDatastoreType.OPERATIONAL, YangInstanceIdentifier.EMPTY);

        Futures.addCallback(cfgDataFuture, new FutureCallback<Optional<NormalizedNode<?, ?>>>() {

            @Override public void onSuccess(final Optional<NormalizedNode<?, ?>> result) {
                if(result.isPresent()) {
//                    LOG.
                    final NormalizedNode<?, ?> normalizedNode = result.get();
                    final DOMStoreWriteTransaction test = InMemoryDOMDataStoreFactory.create("test", null)
                        .newWriteOnlyTransaction();
                    // store data in inmemory DS
                    test.write(YangInstanceIdentifier.EMPTY, normalizedNode);
                    test.close();
                    // check Oper
                }
            }

            @Override public void onFailure(final Throwable t) {
//                LOG.
            }
        });

        Futures.addCallback(operDataFuture, new FutureCallback<Optional<NormalizedNode<?, ?>>>() {

            @Override public void onSuccess(final Optional<NormalizedNode<?, ?>> result) {
                if(result.isPresent()) {
                    final NormalizedNode<?, ?> normalizedNode = result.get();
                    // store data in inmemory oper DS
                }
            }

            @Override public void onFailure(final Throwable t) {
//                LOG.
            }
        });

        domDataReadOnlyTransaction.close();
    }

    @Override public DOMDataReadOnlyTransaction newReadOnlyTransaction() {
        return new CachedDOMTransaction(domDataBroker, schemaContext,pool);
    }

    @Override public DOMDataReadWriteTransaction newReadWriteTransaction() {
    	return new CachedDOMTransaction(domDataBroker, schemaContext,pool);
    }

    @Override public DOMDataWriteTransaction newWriteOnlyTransaction() {
    	return new CachedDOMTransaction(domDataBroker, schemaContext,pool);
    }

    @Override public ListenerRegistration<DOMDataChangeListener> registerDataChangeListener(
        final LogicalDatastoreType store, final YangInstanceIdentifier path, final DOMDataChangeListener listener,
        final DataChangeScope triggeringScope) {
        return null;
    }

    @Override public DOMTransactionChain createTransactionChain(
        final TransactionChainListener transactionChainListener) {
        return null;
    }

    @Nonnull @Override public Map<Class<? extends DOMDataBrokerExtension>, DOMDataBrokerExtension> getSupportedExtensions() {
        return null;
    }
}
