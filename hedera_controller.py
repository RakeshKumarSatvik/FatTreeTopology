from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.ip import ipv4_to_bin
import socket
from threading import Thread
import time

class Controller(app_manager.RyuApp):
    def client(threadname):
        s = socket.socket()         # Create a socket object
        host = '127.0.0.1'          # Get local machine name
        port = 6000                # Reserve a port for your service.
        flag = 1
        while flag == 1:
            try:
                s.connect((host, port))
                s.send('1024')
                s.close                     # Close the socket when done
                time.sleep(10)
                print 'Read information'
            except:
                #print 'Trying to Connect'
                flag = 1

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

                    if(src == (hostIp * 2) and dest == ((hostIp * 2) - 1)):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(1)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)
                    elif(dest == (hostIp * 2) and src == ((hostIp * 2) - 1)):
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
                        action = sw.ofproto_parser.OFPActionOutput(2)
                        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, [action])]
                        mod = sw.ofproto_parser.OFPFlowMod(
                                datapath=sw, match=match, cookie=0,
                                command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                priority=1000,
                                flags=ofproto.OFPFF_SEND_FLOW_REM, instructions=inst)
                        sw.send_msg(mod)                        
                        
                    if((dest == ((modHostIp * 2) - 3) or dest == ((modHostIp * 2) - 2)) and modHostIp % 2 == 0):
                        match = sw.ofproto_parser.OFPMatch(eth_type=0x800, ipv4_dst=((10 << 24) + dest))
                        action = sw.ofproto_parser.OFPActionOutput(1)
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

        self.prepareSwitch(ev.dp)
