from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class Router(Node):  # Customized Node class representing a router.
    def config(self, **params):
        super(Router, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Router, self).terminate()


class NetworkTopo(Topo):

    def build(self, **_opts):
        # Subnet 1 = '7.7.7.0/24'
        ra = self.addNode('ra', cls=Router, ip='7.7.7.1/24')
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='7.7.7.100/24', defaultRoute='via 7.7.7.1')
        h2 = self.addHost('h2', ip='7.7.7.101/24', defaultRoute='via 7.7.7.1')

        # Subnet 2 = '1.1.1.0/24'
        rb = self.addNode('rb', cls=Router, ip='1.1.1.1/24')
        s2 = self.addSwitch('s2')
        h3 = self.addHost('h3', ip='1.1.1.100/24', defaultRoute='via 1.1.1.1')
        h4 = self.addHost('h4', ip='1.1.1.101/24', defaultRoute='via 1.1.1.1')

        # Subnet 3 = '2.2.2.0/24'
        rc = self.addNode('rc', cls=Router, ip='2.2.2.1/24')
        s3 = self.addSwitch('s3')
        h5 = self.addHost('h5', ip='2.2.2.100/24', defaultRoute='via 2.2.2.1')
        h6 = self.addHost('h6', ip='2.2.2.101/24', defaultRoute='via 2.2.2.1')

        # Connect subnets to routers
        self.addLink(s1, ra, intfName2='ra-eth1', params2={'ip': '7.7.7.1/24'})
        self.addLink(s2, rb, intfName2='rb-eth1', params2={'ip': '1.1.1.1/24'})
        self.addLink(s3, rc, intfName2='rc-eth1', params2={'ip': '2.2.2.1/24'})
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)
        # Add links between routers
        self.addLink(ra, rb, intfName1='l', intfName2='m', params1={
                     'ip': '3.3.1.1/24'}, params2={'ip': '3.3.1.2/24'})
        self.addLink(rb, rc, intfName1='n', intfName2='o', params1={
                     'ip': '3.3.2.1/24'}, params2={'ip': '3.3.2.2/24'})
        self.addLink(ra, rc, intfName1='p', intfName2='q', params1={
                     'ip': '3.3.3.1/24'}, params2={'ip': '3.3.3.2/24'})


if __name__ == '__main__':

    setLogLevel('info')
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    # Add static routes on ra
    # Route for subnet 2 via rb
    net['ra'].cmd('ip route add 1.1.1.0/24 via 3.3.1.2')
    # "via 3.3.1.2" for h1->ra->rb->rc->h6
    # "via 3.3.3.2" for h1->ra->rc->h6
    net['ra'].cmd('ip route add 2.2.2.0/24 via 3.3.3.2')
    # Add static routes on rb
    # Route for subnet 1 via ra
    net['rb'].cmd('ip route add 7.7.7.0/24 via 3.3.1.1')
    # Route for subnet 3 via rc
    net['rb'].cmd('ip route add 2.2.2.0/24 via 3.3.2.2')
    # Add static routes on rc
    # Route for subnet 1 via ra
    net['rc'].cmd('ip route add 7.7.7.0/24 via 3.3.3.1')
    # Route for subnet 2 via rb
    net['rc'].cmd('ip route add 1.1.1.0/24 via 3.3.2.1')

    net.start()
    info('*** Adding static routes on routers:\n')

    info('*** Routing Tables on Routers:\n')
    for router in ['ra', 'rb', 'rc']:
        info(net[router].cmd('route'))
    CLI(net)
    net.stop()
