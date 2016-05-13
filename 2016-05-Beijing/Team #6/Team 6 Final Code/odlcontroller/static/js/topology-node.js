// See README.md to understand why we use TopologyContainer (class that inherits nx.ui.Component) instead of
// nx.graphic.Topology
(function (nx) {
	nx.define('TopologyContainer', nx.ui.Component, {
		// we use this trick to use this object as a nx.ui.Component and display topology at the same time
		properties: {
			topology: {
				get: function () {
					return this.view('topology');
				}
			}
		},
		// define view
		view: {
			content: [
				{
					'name': 'topology', // object name
					'type': 'nx.graphic.Topology', // object type
					// this defines properties of a nx.graphic.Topology instance
					// see full specifications online
					// https://developer.cisco.com/site/neXt/document/api-reference-manual/
					'props': {
						'adaptive': true, // width 100% if true
						'showIcon': true,
						'nodeConfig': {
							'label': 'model.name',
							'iconType': 'router',
							'color': '#0how00'
						},
						'linkConfig': {
							'linkType': 'curve' // also: parallel
						},
						'identityKey': 'id', // helps to link source and target
						'width': 800,
						'height': 400,
						'dataProcessor': 'force', // arrange nodes positions if not set
						'enableSmartLabel': true, // moves the labels in order to avoid overlay of them
						'enableGradualScaling': true, // may slow down, if true
						'supportMultipleLink': true // if true, two nodes can have more than one link
					},
					events: {
                    	'topologyGenerated': '{#_path}'
                	}
				}
			]
		},
		methods: {
            _path: function(sender, events) {
                var pathLayer = sender.getLayer("paths");
                var links1 = [sender.getLink(8),sender.getLink(7),sender.getLink(11),sender.getLink(9)];
                var path1 = new nx.graphic.Topology.Path({
                    links: links1,
                    arrow: 'cap'
                    
                });
                pathLayer.addPath(path1);
                var links = sender.getLayer('links').links();
                var i = 0;
                while(i<5){
                	links[i].enable(false);
                	links[i].update;
                	i=i+1;
                }
                //link.enable(false);
                //link.update();
                sender.getNode(8).enable(false);
                
            }
        }
	});
})(nx);