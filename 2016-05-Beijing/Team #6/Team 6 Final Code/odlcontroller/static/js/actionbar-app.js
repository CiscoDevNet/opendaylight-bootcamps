// This class realizes two buttons and their behavior
(function (nx) {
	nx.define('ActionBar', nx.ui.Component, {
		properties: {
			'topology': null, // this prop will be actually initialized by this.assignTopology()
			'exportedData': ''
		},
		view: {
			content: [
				{
					tag: 'div',
					content: [
						{
							// create the button and bind it to the event onAdd
							tag: 'button',
							content: 'Update Routes',
							events: {
								'click': '{#updateTopology}'
							}
						}
					]
				}
			]
		},
		methods: {
			'updateTopology': function () {
					var topo = this.topology();
					// use ajax to fetch an updated topology object
					$.ajax({
						type: 'GET',
						url: '/add/',
						dataType: 'json',
						success: function (data) {
							topo.data(data); 
							topo.fit();
						}
					});
				},
			
			// assign topology instance (by ref) to the actionbar instance
			'assignTopology': function (topo) {
				this.topology(topo);
			}
		}
	});
})(nx);