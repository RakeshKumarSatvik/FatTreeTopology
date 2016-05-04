# I have referred this website for sockets basic in python http://www.tutorialspoint.com/python/python_networking.htm
from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.ip import ipv4_to_bin
import socket
from threading import Thread
import time
import re
msleep = lambda x: time.sleep(x/1000.0)

g_switch = []

topo_link = {}
topo_link = {"e%da%d" %(x,x) : 0 for x in range(0,8)}
z = {"e%da%d" %(x,x+1) : 0 for x in range(0,8,2)}
topo_link.update(z)
z = {"e%da%d" %(x,x-1) : 0 for x in range(1,8,2)}
topo_link.update(z)
z = {"a%dc%d" %(x,x%2) : 0 for x in range(0,8,2)}
topo_link.update(z)
z = {"a%dc%d" %(x,(x%2)+1) : 0 for x in range(0,8,2)}
topo_link.update(z)
z = {"a%dc%d" %(x,2) : 0 for x in range(1,8,2)}
topo_link.update(z)
z = {"a%dc%d" %(x,3) : 0 for x in range(1,8,2)}
topo_link.update(z)

class Controller(app_manager.RyuApp):
    def path_population(self, source):
        global topo_link
        path_chosen = 'nothing'
        if (source % 4 < 3 and source % 4 != 0):
            #e0a0->a0c0 or e0a0->a0c1
            straight_one = topo_link["e%da%d"%((source - 1)/2,((source - 1)/2))] + topo_link["a%dc%d"%((source - 1)/2, 0)]
            straight_two = topo_link["e%da%d"%((source - 1)/2,((source - 1)/2))] + topo_link["a%dc%d"%((source - 1)/2, 1)]
            
            #e0a1->a1c2 or e0a1->a1c3
            cross_one = topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) + 1)] + topo_link["a%dc%d"%(((source - 1)/2) + 1, 2)]
            cross_two = topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) + 1)] + topo_link["a%dc%d"%(((source - 1)/2) + 1, 3)]
            
            value = min(straight_one, straight_two, cross_one, cross_two)
            
            if value == straight_one:
                path_chosen = 'straight_one'
                topo_link["e%da%d"%((source - 1)/2,((source - 1)/2))] += 1
                topo_link["a%dc%d"%((source - 1)/2, 0)] += 1
            elif value == straight_two:
                path_chosen = 'straight_two'
                topo_link["e%da%d"%((source - 1)/2,((source - 1)/2))] += 1
                topo_link["a%dc%d"%((source - 1)/2, 1)] += 1
            elif value == cross_one:
                path_chosen = 'cross_one'
                topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) + 1)] += 1
                topo_link["a%dc%d"%(((source - 1)/2) + 1, 2)] += 1
            elif value == cross_two:
                path_chosen = 'cross_two'
                topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) + 1)] +=1
                topo_link["a%dc%d"%(((source - 1)/2) + 1, 3)] += 1
            else:
                print 'Something terribly is wrong'
            #min(e0a0,e0a1)
            #min(topo_link["e%da%d"%((source - 1)/2,((source - 1)/2))], topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) + 1)])
            #min(a0c0,a0c1,a1c2,a1c3)
            #min(topo_link["a%dc%d"%((source - 1)/2, 0)], topo_link["a%dc%d"%((source - 1)/2, 1)], topo_link["a%dc%d"%(((source - 1)/2) + 1, 2)],  topo_link["a%dc%d"%(((source - 1)/2) + 1, 3)])
        else:
            #e1a1->a1c2 or e1a1->a1c3
            straight_one = topo_link["e%da%d"%((source - 1)/2,(source - 1)/2)] + topo_link["a%dc%d"%(((source - 3)/2) + 1, 2)]
            straight_two = topo_link["e%da%d"%((source - 1)/2,(source - 1)/2)] + topo_link["a%dc%d"%(((source - 3)/2) + 1, 3)]
            
            #e1a0->a0c0 or e1a0->a0c1
            cross_one = topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) - 1)] + topo_link["a%dc%d"%((source - 3)/2, 0)]
            cross_two = topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) - 1)] + topo_link["a%dc%d"%((source - 3)/2, 1)]
            
            value = min(straight_one, straight_two, cross_one, cross_two)
            
            if value == straight_one:
                path_chosen = 'straight_one'
                topo_link["e%da%d"%((source - 1)/2,(source - 1)/2)] += 1
                topo_link["a%dc%d"%(((source - 3)/2) + 1, 2)] += 1
            elif value == straight_two:
                path_chosen = 'straight_two'
                topo_link["e%da%d"%((source - 1)/2,(source - 1)/2)] += 1
                topo_link["a%dc%d"%(((source - 3)/2) + 1, 3)] += 1
            elif value == cross_one:
                path_chosen = 'cross_one'
                topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) - 1)] +=1
                topo_link["a%dc%d"%((source - 3)/2, 0)] += 1
            elif value == cross_two:
                path_chosen = 'cross_two'
                topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) - 1)] += 1
                topo_link["a%dc%d"%((source - 3)/2, 1)] += 1
            #min(e1a0,e1a1)
            #min(topo_link["e%da%d"%((source - 1)/2,((source - 1)/2) - 1)], topo_link["e%da%d"%((source - 1)/2,(source - 1)/2)])
            #min(a0c0,a0c1,a1c2,a1c3)
            #min(topo_link["a%dc%d"%((source - 3)/2, 0)], topo_link["a%dc%d"%((source - 3)/2, 1)], topo_link["a%dc%d"%(((source - 3)/2) + 1, 2)],  topo_link["a%dc%d"%(((source - 3)/2) + 1, 3)])
        return path_chosen

    def modify_path(self, path_chosen, source):
        if path_chosen == 'straight_one':
            if (source % 4 < 3 and source / 4 != 1):
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 8, 17]
                else:
                    value = source / 2
                    switches_changed = [value, value + 8, 17]
            else:
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 8, 19]
                else:
                    value = source / 2
                    switches_changed = [value, value + 8, 19]
        elif path_chosen == 'straight_two':
            if (source % 4 < 3 and source / 4 != 1):
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 8, 18]
                else:
                    value = source / 2
                    switches_changed = [value, value + 8, 18]
            else:
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 8, 20]
                else:
                    value = source / 2
                    switches_changed = [value, value + 8, 20]
        elif path_chosen == 'cross_one':
            if (source % 4 < 3 and source / 4 != 1):
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 9, 19]
                else:
                    value = source / 2
                    switches_changed = [value, value + 9, 19]
            else:
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 7, 17]
                else:
                    value = source / 2
                    switches_changed = [value, value + 7, 17]
        elif path_chosen == 'cross_two':
            if (source % 4 < 3 and source / 4 != 1):
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 9, 20]
                else:
                    value = source / 2
                    switches_changed = [value, value + 9, 20]
            else:
                if source % 2 == 1:
                    value = (source / 2) + 1
                    switches_changed = [value, value + 7, 18]
                else:
                    value = source / 2
                    switches_changed = [value, value + 7, 18]
        else:
            print 'Something terribly is wrong'
        return switches_changed
    
    def add_rules(self, switches_changed, dest, path_chosen):
        global g_switch
        for id in switches_changed:
            for sw in g_switch:
                if sw.id != id:
                    continue
                ofproto = sw.ofproto
                ofp_parser = sw.ofproto_parser
                ofp = ofproto
                
                if(id < 9):
                    if path_chosen == 'straight_one' or path_chosen == 'straight_two':
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(3)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=15,
                                priority=1100,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif path_chosen == 'cross_one' or path_chosen == 'cross_two':
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(4)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=15,
                                priority=1100,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                elif id < 17:
                    if path_chosen == 'straight_one' or path_chosen == 'cross_one':
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(3)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=15,
                                priority=1100,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif path_chosen == 'straight_two' or path_chosen == 'cross_two':
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(4)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=15,
                                priority=1100,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                elif id < 21:
                    dummy = None
                    # match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                    # action = sw.ofproto_parser.OFPActionOutput(1)
                    # inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                    # mod = sw.ofproto_parser.OFPFlowMod(
                            # datapath=sw, match=match, cookie=0,
                            # command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=5,
                            # priority=1100,
                            # flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                    # sw.send_msg(mod)            
        return 1
        
    def client(self):
        global g_switch
        hostall = ["20.0.0.%d" % x for x in range(1,17)]
        sendBuff = "sending"
        #host = socket.gethostname()
        port = 5000                # Reserve a port for your service.
        flag = 1
        unique = {}
        count = 0
        while (1):
            for host in hostall:
                s = socket.socket()         # Create a socket object
                try:
                    s.connect((host, port))
                except:
                    if flag==1:
                        print 'Trying to Connect '+ host
                        flag=0;
                    break;
                flag=1;
                try:
                    s.send(sendBuff)
                    text = ''
                    text += s.recv(1024)
                except:
                    print 'send failed '+ host
                    dummy = 1

                find_text = re.findall(r'\d+',text)
                find_host = re.findall(r'\d+',host)
                if find_text == []:
                    continue
                if find_host == []:
                    continue
                
                if len(find_text) == 6:
                    destination = int(find_text[4])
                    source = int(find_host[3])
                    flow_id = source * 100 + int(find_text[5])
                    
                    if not unique.has_key(flow_id):
                        unique[flow_id] = 0
                    # if count == 100:
                        # count = 0
                        # unique = unique.fromkeys(unique, 0)
                    
                    if int(find_text[0]) > 65536 and unique[flow_id] == 0:
                        path_chosen = self.path_population(source)
                        switches_changed = self.modify_path(path_chosen, source)
                        final = self.add_rules(switches_changed, destination, path_chosen)
                        unique[flow_id] = 1
                        #print path_chosen, switches_changed
                        #print  source, ' to ', destination
                        #print 'Sent query to ' + host
                        print 'Elephant flow ' + find_text[0] + ' from ', source , ' to ' , destination
                    s.close# Close the socket when done
            msleep(100)
            count += 1
        client.exit();

    def __init__(self):
        super(Controller, self).__init__()
        thread = Thread(target = self.client)
        thread.start()

    def prepareSwitch(self, sw):
        hostIp = int(sw.id)
        ofproto = sw.ofproto
        ofp_parser = sw.ofproto_parser
        ofp = ofproto
        
        # Send the ARP/IP packets to the proper host
        if(hostIp < 9):
            for dest in range(1,17):
                for src in range(1,17):
                    if((dest < ((hostIp * 2) - 1) or dest > (hostIp * 2)) and (src < ((hostIp * 2) - 1) or src > (hostIp * 2))):
                       continue

                    if(src == dest):
                        continue

                    if(dest == ((hostIp * 2) - 1)):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(1)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif(dest == (hostIp * 2)):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(2)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    else:
                        action1 = sw.ofproto_parser.OFPActionOutput(3)
                        action2 = sw.ofproto_parser.OFPActionOutput(4)

                        bucket1 = sw.ofproto_parser.OFPBucket(weight=1, actions=[action1])
                        bucket2 = sw.ofproto_parser.OFPBucket(weight=1, actions=[action2])

                        group_id = 12
                        group_mod = sw.ofproto_parser.OFPGroupMod(
                                datapath=sw, command=ofproto.OFPGC_ADD,
                                type_=ofproto.OFPGT_SELECT, group_id=group_id,
                                buckets=[bucket1, bucket2])
                        sw.send_msg(group_mod)

                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        group_action = sw.ofproto_parser.OFPActionGroup(group_id)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [group_action])]

                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=100,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
        elif (hostIp < 17):
            modHostIp = hostIp % 8;
            for dest in range(1,17):
                for src in range(1,17):
                    if((dest < ((modHostIp * 2) - 1) or (dest > (modHostIp * 2) + 2)) and ((src < ((modHostIp * 2) - 1) or src > ((modHostIp * 2) + 1)))):
                        continue

                    if (src == dest):
                        continue

                    if modHostIp % 8 == 0:
                        modHostIp = 8;
                    if((dest == ((modHostIp * 2) - 1) or dest == (modHostIp * 2)) and modHostIp % 2 == 1):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(1)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)

                    if((dest == ((modHostIp * 2) + 1) or dest == ((modHostIp * 2) + 2)) and modHostIp % 2 == 1):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(2)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)

                    if((dest == ((modHostIp * 2) - 1) or dest == (modHostIp * 2)) and modHostIp % 2 == 0):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(1)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)

                    if((dest == ((modHostIp * 2) - 3) or dest == ((modHostIp * 2) - 2)) and modHostIp % 2 == 0):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(2)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)

                    action1 = sw.ofproto_parser.OFPActionOutput(3)
                    action2 = sw.ofproto_parser.OFPActionOutput(4)

                    bucket1 = sw.ofproto_parser.OFPBucket(weight=1, actions=[action1])
                    bucket2 = sw.ofproto_parser.OFPBucket(weight=1, actions=[action2])

                    group_id = 13
                    group_mod = sw.ofproto_parser.OFPGroupMod(
                            datapath=sw, command=ofproto.OFPGC_ADD,
                            type_=ofproto.OFPGT_SELECT, group_id=group_id,
                            buckets=[bucket1, bucket2])
                    sw.send_msg(group_mod)

                    match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                    group_action = sw.ofproto_parser.OFPActionGroup(group_id)
                    inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [group_action])]

                    mod = sw.ofproto_parser.OFPFlowMod(
                            datapath=sw, match=match, cookie=0,
                            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                            priority=100,
                            flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                    sw.send_msg(mod)
        elif(hostIp < 21):
            for dest in range(1,17):
                for src in range(1,17):
                    if (src == dest):
                        continue

                    if (dest > 0 and dest < 5):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(1)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif (dest > 4 and dest < 9):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(2)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif (dest > 8 and dest < 13):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(3)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif (dest > 12 and dest < 17):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(4)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
    # the rest of the code
    @set_ev_cls(dpset.EventDP)
    def switchStatus(self, ev):
        print("Switch %s: %s!" %
                (ev.dp.id, "connected" if ev.enter else "disconnected"))
        global g_switch
        g_switch.append(ev.dp)

        self.prepareSwitch(ev.dp)