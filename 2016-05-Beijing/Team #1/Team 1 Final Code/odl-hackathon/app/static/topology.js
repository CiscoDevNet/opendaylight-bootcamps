function drawTopo(topologyData) {
    console.log(topologyData);
    var topoColors = {
        switch: '#449dd7',
        host: '#464646'
    };
    var collapseLinks = function (topoToCollapse) {
        topoToCollapse.getLayer('linkSet').eachLinkSet(function (l) {
            l.collapsedRule(true);
            l.updateLinkSet();
        });
    };

    topo = new nx.graphic.Topology({
        adaptive: true,
        // scalable: true,
        nodeConfig: {
            label: 'model.label',
            iconType: 'model.group',
            color: function (node, model) {
                return topoColors[model._iconType];
            }
        },
        linkConfig: {
            color: function (link, model) {
                var isHost = link._linkKey.split('_').some(function (n) {
                    return topologyData.nodes.some(function (tn) {
                        return tn.id === n && tn.group === 'host';
                    });
                });

                return isHost ? topoColors['host'] : topoColors['switch'];
            },
            linkType: 'curve'
        },
        dataProcessor: 'force',
        identityKey: 'id',
        showIcon: true,
        theme: 'blue',
        enableSmartNode: false,
        tooltipManagerConfig: {
            nodeTooltipContentClass: 'CustomTooltip'
        }
    });

    topo.tooltipManager().showNodeTooltip(false);
    topo.tooltipManager().showLinkSetTooltip(false);

    topo.on('ready', function (sender, event) {
        topo.data(topologyData);

        collapseLinks(topo);
    });

    var app = new nx.ui.Application();
    app.container(document.getElementById('graph-container'));
    app.on('resize', function () {
        topo.adaptToContainer();
    });

    topo.attach(app);
}