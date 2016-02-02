


case $1 in

make)
      mvn clean package -DskipTest
      ;;

start)
	echo "now start the storm program"
	~/zkServer.sh start
	storm nimbus >/dev/null 2>&1 &
	storm ui >/dev/null 2>&1 &
	storm supervisor >/dev/null 2>&1 &
	;;
run)
     storm jar target/storm-winlab-odl-0.9.5-jar-with-dependencies.jar storm.winlab.odl.Kafka kafka
     ;;
local)
	storm jar target/storm-winlab-odl-0.9.5-jar-with-dependencies.jar storm. winlab.odl.Kafka
     ;;
kill)
    storm kill kafka
    ;;

stop)
    echo "now kill all storm processes"
        jps -l | grep core | cut -d ' ' -f 1 | xargs -rn1 kill
        jps -l | grep nimbus | cut -d ' ' -f 1 | xargs -rn1 kill
        jps -l | grep QuorumPeerMain | cut -d ' ' -f 1 | xargs -rn1 kill
        jps -l | grep supervisor | cut -d ' ' -f 1 | xargs -rn1 kill
       
	;;
esac
