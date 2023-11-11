import signal
from time import sleep
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCIntf
from argparse import ArgumentParser


class MyTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        # loss = 1 or loss = 3 in d part
        self.addLink(s1, s2)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--config', default=None, choices=[None, 'b', 'c'])
    args = parser.parse_args()
    setLogLevel('info')
    topo = MyTopo()
    net = Mininet(topo=topo, waitConnected=True, intf=TCIntf)
    net.start()
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    if args.config == 'b':
        for c in ['cubic', 'vegas', 'reno', 'bbr']:
            h4.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={c}')
            h1.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={c}')
            # Q2_b_cvrb for part b
            # Q2_d_cvrb_1 for part d 1%
            # Q2_d_cvrb_3 for part d 3%
            h4.cmd(f'iperf -s -i 1 >> Q2_b_cvrb.txt &')
            h1.cmd(f'iperf -c 10.0.0.4 -t 30')

    elif args.config == 'c':
        for c in ['cubic', 'vegas', 'reno', 'bbr']:
            h1.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={c}')
            h2.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={c}')
            h3.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={c}')
            h4.cmd(f'sysctl -w net.ipv4.tcp_congestion_control={c}')
            h4.cmd(f'iperf -s -i 1 >> Q2_c_cvrb.txt &')
            h1.cmd(f'iperf -c 10.0.0.4 -t 30 &')
            h2.cmd(f'iperf -c 10.0.0.4 -t 30 &')
            h3.cmd(f'iperf -c 10.0.0.4 -t 30')

    CLI(net)
    net.stop()
