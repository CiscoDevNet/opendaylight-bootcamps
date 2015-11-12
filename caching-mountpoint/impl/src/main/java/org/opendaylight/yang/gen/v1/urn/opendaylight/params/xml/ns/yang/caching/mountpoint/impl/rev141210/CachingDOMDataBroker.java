package org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.caching.mountpoint.impl.rev141210;

import com.google.common.base.Function;
import com.google.common.base.Optional;
import com.google.common.util.concurrent.CheckedFuture;
import com.google.common.util.concurrent.FutureCallback;
import com.google.common.util.concurrent.Futures;
import com.google.common.util.concurrent.ListenableFuture;
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
import org.opendaylight.controller.md.sal.dom.store.impl.InMemoryDOMDataStoreFactory;
import org.opendaylight.controller.sal.core.spi.data.DOMStoreReadTransaction;
import org.opendaylight.controller.sal.core.spi.data.DOMStoreWriteTransaction;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier;
import org.opendaylight.yangtools.yang.data.api.schema.NormalizedNode;
import org.opendaylight.yangtools.yang.model.api.SchemaContext;

/**
 * Created by mmarsale on 5.11.2015.
 */
public class CachingDOMDataBroker implements DOMDataBroker {

    private DOMDataBroker domDataBroker;
    private SchemaContext schemaContext;

    public CachingDOMDataBroker(final DOMDataBroker domDataBroker, final SchemaContext schemaContext) {
        this.domDataBroker = domDataBroker;
        this.schemaContext = schemaContext;
        initializeCache();
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

        Futures.addCallback(cfgDataFuture, new FutureCallback<Optional<NormalizedNode<?, ?>>>() {

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
        return new DOMDataReadOnlyTransaction() {

            @Override public void close() {

            }

            @Override public CheckedFuture<Optional<NormalizedNode<?, ?>>, ReadFailedException> read(
                final LogicalDatastoreType logicalDatastoreType, final YangInstanceIdentifier yangInstanceIdentifier) {
                // FIXME read from the right datastore
                final DOMStoreReadTransaction test = InMemoryDOMDataStoreFactory.create("test", null).newReadOnlyTransaction();
                return test.read(yangInstanceIdentifier);
            }

            @Override public CheckedFuture<Boolean, ReadFailedException> exists(
                final LogicalDatastoreType logicalDatastoreType, final YangInstanceIdentifier yangInstanceIdentifier) {
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

            @Override public Object getIdentifier() {
                return this;
            }
        };
    }

    @Override public DOMDataReadWriteTransaction newReadWriteTransaction() {
        return null;
    }

    @Override public DOMDataWriteTransaction newWriteOnlyTransaction() {
        return new DOMDataWriteTransaction() {

            @Override public void put(final LogicalDatastoreType logicalDatastoreType,
                final YangInstanceIdentifier yangInstanceIdentifier, final NormalizedNode<?, ?> normalizedNode) {

                // Store in device
                final DOMDataWriteTransaction realDeviceTx = domDataBroker.newWriteOnlyTransaction();
                realDeviceTx.put(logicalDatastoreType, yangInstanceIdentifier, normalizedNode);
                final CheckedFuture<Void, TransactionCommitFailedException> submit = realDeviceTx.submit();

                Futures.addCallback(submit, new FutureCallback<Void>() {

                    @Override public void onSuccess(@Nullable final Void result) {
                        // TODO Store in cache
                        final DOMStoreWriteTransaction test = InMemoryDOMDataStoreFactory.create("test", null)
                            .newWriteOnlyTransaction();
                        try {
                            test.write(yangInstanceIdentifier, normalizedNode);
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
                }


            }

            @Override public void merge(final LogicalDatastoreType logicalDatastoreType,
                final YangInstanceIdentifier yangInstanceIdentifier, final NormalizedNode<?, ?> normalizedNode) {

            }

            @Override public boolean cancel() {
                return false;
            }

            @Override public void delete(final LogicalDatastoreType store, final YangInstanceIdentifier path) {

            }

            @Override public CheckedFuture<Void, TransactionCommitFailedException> submit() {
//                if() {
//                    return Futures.immediateFailedCheckedFuture(new TransactionCommitFailedException("Already failed"));
//                }
                return null;
            }

            @Override public ListenableFuture<RpcResult<TransactionStatus>> commit() {
                return null;
            }

            @Override public Object getIdentifier() {
                return this;
            }
        };
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
