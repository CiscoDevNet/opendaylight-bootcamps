控制器运行在本机，mininet模拟器运行在虚拟机

# 安装控制器，下载 #
由于总所周知的原因ODL官方网站下载比较慢，所以我特意在服务器上下载了一个，猛击这里下载
http://61.152.234.152:81/distribution-karaf-0.4.1-Beryllium-SR1.tar.gz

下载之后解压，切换到shell或者cmd下，执行bin/karaf
默认情况下ODL没有开启任何feature，所以它没有任何功能，我们的实验环境需要开启两个feature
执行
feature:install odl-openflowplugin-all
feature:install odl-l2switch-all
执行完毕之后控制器的安装就完成了
提示：ODL的shell可以用help命令查看帮助，通过tab可以实现自动补全

# 安装模拟器 #
http://mininet.org/download/

下载 Mininet VM image
通过vmware导入为一个虚拟机，然后启动
启动成功之后用户名是mininet，密码是mininet

后续所有操作都可以通过SSH进行

我们的代码库中tools/mytopo.py是环境需要的拓扑，注意代码中ip=172.16.62.1
这一句，这个IP地址是我笔记本的IP地址（ODL所在的机器）
执行 python mytopo.py 自动生成拓扑结构

**Mininet拓扑发现**
c0 ping c1 -c1
c0 ping c2 -c1
t1_h0 ping t1_h1 -c1
t2_h0 ping t2_h1 -c1

# ODL配置 #
我们的实验环境中需要设置:
is-proactive-flood-mode=false
is-learning-only-mode=true
完成以上设置之后每台OF交换机接入到ODL中都会被自动下发三个流表分别是:
Cookie流表
ARP流表,收到ARP之后发给Controller
LLDP流表,收到LLDP之后发给Controller


# odl-l2switch-all关键配置 #
ODL的配置文件都在${ODL_BASE_DIR}/etc/opendaylight/karaf下面
Arp Handler (54-arphandler.xml)
is-proactive-flood-mode 碰到不认识的包是否执行泛洪
`
"true" means that flood flows will be installed on each switch. With this flood flow, each switch will flood a packet that doesn't match any other flows.
Advantage: Fewer packets are sent to the controller because those packets are flooded to the network.
Disadvantage: A lot of network traffic is generated.
`
`
"false" means the previously mentioned flood flows will not be installed. Instead an ARP flow will be installed on each switch that sends all ARP packets to the controller.
Advantage: Less network traffic is generated. **
Disadvantage: The controller handles more packets (ARP requests & replies) and the ARP process takes longer than if there were flood flows. **
`

L2Switch Main (58-l2switchmain.xml)
is-install-dropall-flow 暂时不清楚
`
"true" means a drop-all flow will be installed on each switch, so the default action will be to drop a packet instead of sending it to the controller
`
`
"false" means this flow will not be installed
`

is-learning-only-mode L2会生成一些MAC到MAC的流表作为优化
`
"true" means that the L2Switch will only be learning addresses. No additional flows to optimize network traffic will be installed.
`
`
"false" means that the L2Switch will react to network traffic and install flows on the switches to optimize traffic. Currently, MAC-to-MAC flows are installed.
`

