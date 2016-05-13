(function (nx) {
    /**
     * define application
     */
    var Shell = nx.define(nx.ui.Application, {
        methods: {
            start: function () {
                //your application main entry

                // initialize a topology
                var topo = new nx.graphic.Topology({
                    // set the topology view's with and height
                    width: 900,
                    height: 500,
                    // node config
                    nodeConfig: {
                        // label display name from of node's model, could change to 'model.id' to show id
                        label: 'model.name',
                        iconType: 'router'
                    },
                    // link config
                    linkConfig: {
                        // multiple link type is curve, could change to 'parallel' to use parallel link
                        linkType: 'curve'
                        
                    },
                    // show node's icon, could change to false to show dot
                    showIcon: true
                });
                var app = new nx.ui.Application();
				app.container(document.getElementById('app'));
				topo.attach(app);

                //set data to topology
                topo.data(topologyData);
                //attach topology to document
                //topo.attach(this);
                topo.on('topologyGenerated', function(){
                	var links1 = [topo.getLink(0),topo.getLink(2),topo.getLink(5),topo.getLink(6),topo.getLink(11)];
                	var path1 = new nx.graphic.Topology.Path({
                		links: links1,
                		arrow: 'cap',
                		//pathStyle: {'fill':'green'}
                		
                	});
                	var pathLayer = topo.getLayer("paths");
                	pathLayer.addPath(path1);
                	
                	//var links = topo.getLayer('links').links();
                	//var link = links[8];
                	//link.enable(false);
                	//link.update();
                	topo.getNode(2).enable(false);
                });
            }
        }
    });

    /**
     * create application instance
     */
    var shell = new Shell();
	
    /**
     * invoke start method
     */
    shell.start();
})(nx);