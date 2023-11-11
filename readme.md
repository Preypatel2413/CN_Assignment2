mytopo.py
    a.  In the Terminal: `sudo python3 mytopo.py`
        In the Mininet CLI: `pingall`
    b.  In the Terminal: `sudo python3 mytopo.py`
        In the Mininet CLI: `xterm ra`
        In the 'Node: ra' Terminal: `wireshark`
        Do the needful in the Wireshark window that pops up. Output in file 'Q1_b.pcap'
        In the Mininet CLI: `pingall`
    c.  Make necessary change in line 69 indicated by the comments in lines 67 and 68
        In the Terminal: `sudo python3 mytopo.py`
        In the Mininet CLI: `xterm h1 h6`
        In the 'Node: h1' Terminal: `ping 2.2.2.101`
        In the 'Node: h6' Terminal: `iperf -s -u -i 1`
        In the 'Node: h1' Terminal: `iperf -c 2.2.2.101 -u -b`
    d.  Make necessary change in line 69 indicated by the comments in lines 67 and 68
        In the Terminal: `sudo python3 mytopo.py`

mytopo2.py
    cvrb = cubic-vegas-reno-bbr
    a.  In the Terminal: `sudo python3 mytopo2.py`
        In the Mininet CLI: `pingall`
    b.  In the Terminal: `sudo python3 mytopo2.py --config=b`
        Output file: 'Q2_b_cvrb.txt'
    c.  In the Terminal: `sudo python3 mytopo2.py --config=c`
        Output file: 'Q2_c_cvrb.txt'
    d.  Make necessary change in line 26 indicated by the comment in line 25
        Make necessary change in line 48 indicated by the comment in line 45, 46, and 47
        In the Terminal: `sudo python3 mytopo2.py --config=b`
        Output file: 'Q2_d_cvrb_1.txt' or
                     'Q2_d_cvrb_3.txt'

Note: ~ If an error occurs saying that the network can not be created, then run `sudo fuser -k 6653/tcp`
      ~ If an error occurs saying that a file already exists, then run `sudo mn -c`
      ~ After running the above two commands in the terminal, if there is any error, then your computer might be depressed, as it might have become sentient and realised that its owner is such a scumbag.
      ~ If the PC does not pass the Turing test, then lol, skill issue, get rekt, nerd!