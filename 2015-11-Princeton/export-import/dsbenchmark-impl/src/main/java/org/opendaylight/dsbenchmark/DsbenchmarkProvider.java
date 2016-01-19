/*
 * Copyright (c) 2015 Cisco Systems and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.dsbenchmark;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicReference;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.stream.FactoryConfigurationError;
import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

import com.google.common.base.Optional;
import com.google.common.base.Throwables;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.WriteTransaction;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.common.api.data.ReadFailedException;
import org.opendaylight.controller.md.sal.common.api.data.TransactionCommitFailedException;
import org.opendaylight.controller.md.sal.dom.api.DOMDataBroker;
import org.opendaylight.controller.md.sal.dom.api.DOMDataReadOnlyTransaction;
import org.opendaylight.controller.md.sal.dom.api.DOMDataWriteTransaction;
import org.opendaylight.controller.sal.binding.api.BindingAwareBroker.ProviderContext;
import org.opendaylight.controller.sal.binding.api.BindingAwareBroker.RpcRegistration;
import org.opendaylight.controller.sal.binding.api.BindingAwareProvider;
import org.opendaylight.controller.sal.core.api.model.SchemaService;
import org.opendaylight.dsbenchmark.simpletx.SimpletxBaDelete;
import org.opendaylight.dsbenchmark.simpletx.SimpletxBaRead;
import org.opendaylight.dsbenchmark.simpletx.SimpletxBaWrite;
import org.opendaylight.dsbenchmark.simpletx.SimpletxDomDelete;
import org.opendaylight.dsbenchmark.simpletx.SimpletxDomRead;
import org.opendaylight.dsbenchmark.simpletx.SimpletxDomWrite;
import org.opendaylight.dsbenchmark.txchain.TxchainBaDelete;
import org.opendaylight.dsbenchmark.txchain.TxchainBaRead;
import org.opendaylight.dsbenchmark.txchain.TxchainBaWrite;
import org.opendaylight.dsbenchmark.txchain.TxchainDomDelete;
import org.opendaylight.dsbenchmark.txchain.TxchainDomRead;
import org.opendaylight.dsbenchmark.txchain.TxchainDomWrite;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.DsbenchmarkService;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.ExportStoreInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.ImportStoreInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.StartTestInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.StartTestOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.StartTestOutputBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.TestExec;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.TestExecBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.TestStatus;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.TestStatus.ExecStatus;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.TestStatusBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.dsbenchmark.rev150105.test.exec.OuterList;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.opendaylight.yangtools.yang.common.QName;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.opendaylight.yangtools.yang.common.RpcResultBuilder;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier;
import org.opendaylight.yangtools.yang.data.api.YangInstanceIdentifier.NodeIdentifierWithPredicates;
import org.opendaylight.yangtools.yang.data.api.schema.ContainerNode;
import org.opendaylight.yangtools.yang.data.api.schema.MapEntryNode;
import org.opendaylight.yangtools.yang.data.api.schema.NormalizedNode;
import org.opendaylight.yangtools.yang.data.api.schema.stream.NormalizedNodeStreamWriter;
import org.opendaylight.yangtools.yang.data.api.schema.stream.NormalizedNodeWriter;
import org.opendaylight.yangtools.yang.data.impl.codec.xml.XMLStreamNormalizedNodeStreamWriter;
import org.opendaylight.yangtools.yang.data.impl.codec.xml.XmlUtils;
import org.opendaylight.yangtools.yang.data.impl.schema.ImmutableNodes;
import org.opendaylight.yangtools.yang.data.impl.schema.transform.dom.parser.DomToNormalizedNodeParserFactory;
import org.opendaylight.yangtools.yang.model.api.RpcDefinition;
import org.opendaylight.yangtools.yang.model.api.SchemaContext;
import org.opendaylight.yangtools.yang.model.api.SchemaPath;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

import javanet.staxutils.IndentingXMLStreamWriter;

import org.opendaylight.netconf.sal.rest.api.Draft02;
import org.opendaylight.netconf.sal.rest.api.RestconfNormalizedNodeWriter;
import org.opendaylight.netconf.sal.rest.api.RestconfService;
import org.opendaylight.netconf.sal.restconf.impl.InstanceIdentifierContext;
import org.opendaylight.netconf.sal.restconf.impl.NormalizedNodeContext;

import com.google.common.base.Optional;
import com.google.common.util.concurrent.CheckedFuture;
import com.google.common.util.concurrent.Futures;

public class DsbenchmarkProvider implements BindingAwareProvider, DsbenchmarkService, AutoCloseable {

    private static final Logger LOG = LoggerFactory.getLogger(DsbenchmarkProvider.class);
    private final AtomicReference<ExecStatus> execStatus = new AtomicReference<ExecStatus>( ExecStatus.Idle );

    private static final InstanceIdentifier<TestExec> TEST_EXEC_IID = InstanceIdentifier.builder(TestExec.class).build();
    private static final InstanceIdentifier<TestStatus> TEST_STATUS_IID = InstanceIdentifier.builder(TestStatus.class).build();
    private final DOMDataBroker domDataBroker;
    private final DataBroker bindingDataBroker;
    private final SchemaService schemaService;
    private RpcRegistration<DsbenchmarkService> dstReg;
    private DataBroker dataBroker;

    private long testsCompleted = 0;
    
    private static final XMLOutputFactory XML_FACTORY;

    static {
        XML_FACTORY = XMLOutputFactory.newFactory();
        XML_FACTORY.setProperty(XMLOutputFactory.IS_REPAIRING_NAMESPACES, true);
    }

    public DsbenchmarkProvider(DOMDataBroker domDataBroker, DataBroker bindingDataBroker, SchemaService schemaService) {
        // We have to get the DOMDataBroker via the constructor,
        // since we can't get it from the session
        this.domDataBroker = domDataBroker;
        this.bindingDataBroker = bindingDataBroker;
        this.schemaService =schemaService;
//        schemaService.registerSchemaContextListener(arg0)
    }

    @Override
    public void onSessionInitiated(ProviderContext session) {
        this.dataBroker = session.getSALService(DataBroker.class);
        this.dstReg = session.addRpcImplementation( DsbenchmarkService.class, this );
        setTestOperData(this.execStatus.get(), testsCompleted);

        LOG.info("DsbenchmarkProvider Session Initiated");
    }

    @Override
    public void close() throws Exception {
        dstReg.close();
        LOG.info("DsbenchmarkProvider Closed");
    }

    @Override
    public Future<RpcResult<Void>> cleanupStore() {
        cleanupTestStore();
        LOG.info("Data Store cleaned up");
        return Futures.immediateFuture( RpcResultBuilder.<Void> success().build() );
    }

    @Override
    public Future<RpcResult<StartTestOutput>> startTest(StartTestInput input) {
        LOG.info("Starting the data store benchmark test, input: {}", input);

        // Check if there is a test in progress
        if ( execStatus.compareAndSet(ExecStatus.Idle, ExecStatus.Executing) == false ) {
            LOG.info("Test in progress");
            return RpcResultBuilder.success(new StartTestOutputBuilder()
                    .setStatus(StartTestOutput.Status.TESTINPROGRESS)
                    .build()).buildFuture();
        }

        // Cleanup data that may be left over from a previous test run
        cleanupTestStore();

        // Get the appropriate writer based on operation type and data format
        DatastoreAbstractWriter dsWriter = getDatastoreWriter(input);

        long startTime, endTime, listCreateTime, execTime;

        startTime = System.nanoTime();
        dsWriter.createList();
        endTime = System.nanoTime();
        listCreateTime = (endTime - startTime) / 1000;

        // Run the test and measure the execution time
        try {
            startTime = System.nanoTime();
            dsWriter.executeList();
            endTime = System.nanoTime();
            execTime = (endTime - startTime) / 1000;

            this.testsCompleted++;

        } catch ( Exception e ) {
            LOG.error( "Test error: {}", e.toString());
            execStatus.set( ExecStatus.Idle );
            return RpcResultBuilder.success(new StartTestOutputBuilder()
                    .setStatus(StartTestOutput.Status.FAILED)
                    .build()).buildFuture();
        }

        LOG.info("Test finished");
        setTestOperData( ExecStatus.Idle, testsCompleted);
        execStatus.set(ExecStatus.Idle);

        StartTestOutput output = new StartTestOutputBuilder()
                .setStatus(StartTestOutput.Status.OK)
                .setListBuildTime(listCreateTime)
                .setExecTime(execTime)
                .setTxOk((long)dsWriter.getTxOk())
                .setTxError((long)dsWriter.getTxError())
                .build();

        return RpcResultBuilder.success(output).buildFuture();
    }

    private void setTestOperData( ExecStatus sts, long tstCompl ) {
        TestStatus status = new TestStatusBuilder()
                .setExecStatus(sts)
                .setTestsCompleted(tstCompl)
                .build();

        WriteTransaction tx = dataBroker.newWriteOnlyTransaction();
        tx.put(LogicalDatastoreType.OPERATIONAL, TEST_STATUS_IID, status);

        try {
            tx.submit().checkedGet();
        } catch (TransactionCommitFailedException e) {
            throw new IllegalStateException(e);
        }

        LOG.info("DataStore test oper status populated: {}", status);
    }

    private void cleanupTestStore() {
        TestExec data = new TestExecBuilder()
                .setOuterList(Collections.<OuterList>emptyList())
                .build();

        WriteTransaction tx = dataBroker.newWriteOnlyTransaction();
        tx.put(LogicalDatastoreType.CONFIGURATION, TEST_EXEC_IID, data);
        try {
            tx.submit().checkedGet();
            LOG.info("DataStore test data cleaned up");
        } catch (TransactionCommitFailedException e) {
            LOG.info("Failed to cleanup DataStore test data");
            throw new IllegalStateException(e);
        }

    }

    private DatastoreAbstractWriter getDatastoreWriter(StartTestInput input) {

        final DatastoreAbstractWriter retVal;

        StartTestInput.TransactionType txType = input.getTransactionType();
        StartTestInput.Operation oper = input.getOperation();
        StartTestInput.DataFormat dataFormat = input.getDataFormat();
        int outerListElem = input.getOuterElements().intValue();
        int innerListElem = input.getInnerElements().intValue();
        int writesPerTx = input.getPutsPerTx().intValue();

        try {
            if (txType == StartTestInput.TransactionType.SIMPLETX) {
                if (dataFormat == StartTestInput.DataFormat.BINDINGAWARE) {
                    if (StartTestInput.Operation.DELETE == oper) {
                        retVal = new SimpletxBaDelete(this.dataBroker, outerListElem,
                                innerListElem,writesPerTx);
                    } else if (StartTestInput.Operation.READ == oper) {
                        retVal = new SimpletxBaRead(this.dataBroker, outerListElem,
                                innerListElem,writesPerTx);
                    } else {
                        retVal = new SimpletxBaWrite(this.dataBroker, oper, outerListElem,
                                innerListElem,writesPerTx);
                    }
                } else {
                    if (StartTestInput.Operation.DELETE == oper) {
                        retVal = new SimpletxDomDelete(this.domDataBroker, outerListElem,
                                innerListElem, writesPerTx);
                    } else if (StartTestInput.Operation.READ == oper) {
                        retVal = new SimpletxDomRead(this.domDataBroker, outerListElem,
                                innerListElem, writesPerTx);
                    } else {
                        retVal = new SimpletxDomWrite(this.domDataBroker, oper, outerListElem,
                                innerListElem,writesPerTx);
                    }
                }
            } else {
                if (dataFormat == StartTestInput.DataFormat.BINDINGAWARE) {
                    if (StartTestInput.Operation.DELETE == oper) {
                        retVal = new TxchainBaDelete(this.bindingDataBroker, outerListElem,
                                innerListElem, writesPerTx);
                    } else if (StartTestInput.Operation.READ == oper) {
                        retVal = new TxchainBaRead(this.bindingDataBroker,outerListElem,
                                innerListElem,writesPerTx);
                    } else {
                        retVal = new TxchainBaWrite(this.bindingDataBroker, oper, outerListElem,
                                innerListElem,writesPerTx);
                    }
                } else {
                    if (StartTestInput.Operation.DELETE == oper) {
                        retVal = new TxchainDomDelete(this.domDataBroker, outerListElem,
                                innerListElem, writesPerTx);
                    } else if (StartTestInput.Operation.READ == oper) {
                        retVal = new TxchainDomRead(this.domDataBroker, outerListElem,
                                innerListElem, writesPerTx);

                    } else {
                        retVal = new TxchainDomWrite(this.domDataBroker, oper, outerListElem,
                                innerListElem,writesPerTx);
                    }
                }
            }
        } finally {
            execStatus.set(ExecStatus.Idle);
        }
        return retVal;
    }

	@Override
	public Future<RpcResult<Void>> exportStore(ExportStoreInput input) {
        org.opendaylight.yangtools.yang.common.QName OL_ID = QName.create(OuterList.QNAME, "id");
        DOMDataReadOnlyTransaction tx = domDataBroker.newReadOnlyTransaction();
        

            NormalizedNode<?,?> ret = null;

            YangInstanceIdentifier yid = YangInstanceIdentifier.EMPTY;
            Optional<NormalizedNode<?,?>> optionalDataObject;
            CheckedFuture<Optional<NormalizedNode<?,?>>, ReadFailedException> submitFuture = tx.read(LogicalDatastoreType.CONFIGURATION, yid);
            try {
                optionalDataObject = submitFuture.checkedGet();
                if (optionalDataObject != null && optionalDataObject.isPresent()) {
                    ret = optionalDataObject.get();
                    LOG.info("/n" + String.valueOf(ret));

                    XMLStreamWriter xmlWriter;
                    try {
                    	OutputStream entityStream = null;
                        xmlWriter = XML_FACTORY.createXMLStreamWriter(entityStream);
                    } catch (final XMLStreamException e) {
                        throw new IllegalStateException(e);
                    } catch (final FactoryConfigurationError e) {
                        throw new IllegalStateException(e);
                    }

                    SchemaContext schemaCtx = schemaService.getSessionContext(); // FIXME: get this oe
                    try {
						writeNormalizedNode(xmlWriter, schemaCtx, ret);
					} catch (IOException e) {
						throw new IllegalStateException("Failed to write data", e);
					}
                }

            } catch (ReadFailedException e) {
                LOG.warn("failed to ....", e);

            }

            return Futures.immediateFuture(RpcResultBuilder.<Void> success().build());
	}

	@Override
	public Future<RpcResult<Void>> importStore(ImportStoreInput input) {
		try { 
			String fileName = input.getFileName(); 
			DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance(); 
			DocumentBuilder db = dbf.newDocumentBuilder(); 
			Element root = db.parse(new File(fileName)).getDocumentElement(); 
 
			DomToNormalizedNodeParserFactory parserFactory = DomToNormalizedNodeParserFactory.getInstance(XmlUtils.DEFAULT_XML_CODEC_PROVIDER, schemaService.getSessionContext());
			ContainerNode rootNode = parserFactory.getContainerNodeParser().parse(Collections.singleton(root), schemaService.getSessionContext());
 
			DOMDataWriteTransaction tx = domDataBroker.newWriteOnlyTransaction(); 
            YangInstanceIdentifier yid = YangInstanceIdentifier.EMPTY; 
			tx.put(LogicalDatastoreType.CONFIGURATION, yid, rootNode); 
			tx.submit().checkedGet(); 
 
		} catch (Exception e) { 
			LOG.error("Import failed:", e); 
			return Futures.immediateFailedCheckedFuture(e); 
		}
		
		


        return Futures.immediateFuture(RpcResultBuilder.<Void> success().build());
	}
	
	private void writeNormalizedNode(XMLStreamWriter xmlWriter, SchemaContext schemaCtx, NormalizedNode<?, ?> data)
					throws IOException {
		final NormalizedNodeStreamWriter nnWriter;
		nnWriter = XMLStreamNormalizedNodeStreamWriter.create(xmlWriter,
					schemaCtx, SchemaPath.ROOT);
			 
		writeElements(xmlWriter, NormalizedNodeWriter.forStreamWriter(nnWriter), (ContainerNode) data);
		
		nnWriter.flush();
	}
	
	private void writeElements(final XMLStreamWriter xmlWriter, final NormalizedNodeWriter nnWriter,
			final ContainerNode data) throws IOException {
		try {
			final QName name = data.getNodeType();
			xmlWriter.writeStartElement(XMLConstants.DEFAULT_NS_PREFIX, name.getLocalName(),
					name.getNamespace().toString());
			xmlWriter.writeDefaultNamespace(name.getNamespace().toString());
			for (NormalizedNode<?, ?> child : data.getValue()) {
				nnWriter.write(child);
			}
			nnWriter.flush();
			xmlWriter.writeEndElement();
			xmlWriter.flush();
		} catch (final XMLStreamException e) {
			Throwables.propagate(e);
		}
	}
	
}
