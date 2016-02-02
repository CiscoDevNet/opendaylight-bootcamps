/*
  Author: Wuyang Zhang (qingshanyouyou@gmail.com)

  Target: Draw a time serial graph based on value getting out of XML of Kafka. Used for OpenDayLight Project

*/




package storm.winlab.odl;

import java.io.IOException;
import java.io.File;
import java.io.*;
import java.io.Writer;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import storm.kafka.BrokerHosts;
import storm.kafka.KafkaSpout;
import storm.kafka.SpoutConfig;
import storm.kafka.StringScheme;
import storm.kafka.ZkHosts;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.clients.producer.Callback;
import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.generated.AlreadyAliveException;
import backtype.storm.generated.InvalidTopologyException;
import backtype.storm.spout.SchemeAsMultiScheme;
import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

public class Kafka {

    public static class KafkaWordSplitter extends BaseRichBolt {

	private static final Log LOG = LogFactory.getLog(KafkaWordSplitter.class);
	private static final long serialVersionUID = 886149197481637894L;
	private OutputCollector collector;
	private String fileAddr = "/home/hadoop/spark/output.txt";
          @Override
          public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
	      this.collector = collector;              
          }

	 @Override
	 public void execute(Tuple input){
	      PrintWriter writer;
	      String line = input.getString(0);
	      //  LOG.info("RECV[kafka -> splitter] " + line);
	      String[] words = line.split("\\s+");

	      //Test. Write String out If receive any message.
	      for(String word : words) {
		  try{
		      writer = new PrintWriter(new BufferedWriter(new FileWriter(fileAddr,true)));
		      writer.println(word+"\n\n\n");
		      writer.close();

		  }catch (IOException e){

		      e.printStackTrace();
		      
		  }
		  LOG.info("EMIT[splitter -> counter] " + word);
		  collector.emit(input, new Values(word, 1));
 	      }
	      collector.ack(input);
          }

          @Override
          public void declareOutputFields(OutputFieldsDeclarer declarer) {
	      declarer.declare(new Fields("word", "count"));         
          }
         
    }
    
    public static class WordCounter extends BaseRichBolt {

	private static final Log LOG = LogFactory.getLog(WordCounter.class);
	private static final long serialVersionUID = 886149197481637894L;
	private OutputCollector collector;
	private Map<String, AtomicInteger> counterMap;
         
          @Override
          public void prepare(Map stormConf, TopologyContext context,
			      OutputCollector collector) {
	      this.collector = collector;    
	      this.counterMap = new HashMap<String, AtomicInteger>();
          }

          @Override
          public void execute(Tuple input) {
	      String word = input.getString(0);
	      int count = input.getInteger(1);
	      LOG.info("RECV[splitter -> counter] " + word + " : " + count);
	      AtomicInteger ai = this.counterMap.get(word);
	      if(ai == null) {
		  ai = new AtomicInteger();
		  this.counterMap.put(word, ai);
	      }
	      ai.addAndGet(count);
	      collector.ack(input);
	      LOG.info("CHECK statistics map: " + this.counterMap);
          }

          @Override
          public void cleanup() {
	      LOG.info("The final result:");
	      Iterator<Entry<String, AtomicInteger>> iter = this.counterMap.entrySet().iterator();
	      while(iter.hasNext()) {
		  Entry<String, AtomicInteger> entry = iter.next();
		  LOG.info(entry.getKey() + "\t:\t" + entry.getValue().get());
	      }
              
          }

          @Override
          public void declareOutputFields(OutputFieldsDeclarer declarer) {
	      declarer.declare(new Fields("word", "count"));         
          }
    }
    
    public static void main(String[] args) throws AlreadyAliveException, InvalidTopologyException, InterruptedException,IOException {
	//dynamic read from Zookeeper
	String zks = "Master:2181";
	//topic name
	String topic = "spark-topic";
	//Spout offset position
	String zkRoot = "/storm";
	String id = "word";
        
	//set read Broker of Kafka from Zookeeper
	BrokerHosts brokerHosts = new ZkHosts(zks);
	
	//Spout configuration
	SpoutConfig spoutConf = new SpoutConfig(brokerHosts, topic, zkRoot, id);
	spoutConf.scheme = new SchemeAsMultiScheme(new StringScheme());
	spoutConf.forceFromStart = false;
	spoutConf.zkServers = Arrays.asList(new String[] {"Master"});
	spoutConf.zkPort = 2181;
         
	//Topology Structure
	TopologyBuilder builder = new TopologyBuilder();
	builder.setSpout("kafka-reader", new KafkaSpout(spoutConf), 1); 
	builder.setBolt("word-splitter", new KafkaWordSplitter(), 2).shuffleGrouping("kafka-reader");
	builder.setBolt("word-counter", new WordCounter()).fieldsGrouping("word-splitter", new Fields("word"));
         
	Config conf = new Config();
         
	//	String name = MyKafkaTopology.class.getSimpleName();
	if (args != null && args.length > 0) {
	  
	    conf.setNumWorkers(3);
	    StormSubmitter.submitTopology(args[0],conf,builder.createTopology());

	} else {
	    conf.setMaxTaskParallelism(3);
	    LocalCluster cluster = new LocalCluster();
	    cluster.submitTopology("stormKafka", conf, builder.createTopology());
	    Thread.sleep(60000);
	    cluster.shutdown();
	}

    }//main end
}
