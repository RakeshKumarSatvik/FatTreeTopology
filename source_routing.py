from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.ip import ipv4_to_bin

class Controller(app_manager.RyuApp):

    def prepareSwitch(self, sw):
        hostIp = int(sw.id)
        ofproto = sw.ofproto
        # Send the ARP/IP packets to the proper host
        if(hostIp < 9):
            for port in range(1,5):
                for dest in range(16):
                    for src in range(16):
                        if((dest < ((hostIp * 2) - 2) or dest > ((hostIp * 2) - 1)) and port > 2):
                           continue
                        
                        if((src < ((hostIp * 2) - 2) or src > ((hostIp * 2) - 1)) and port < 3):
                           continue                        

                        if(src == dest):
                            continue
                        
                        vlan = src * 1000 + dest
                        
                        if(src == ((hostIp * 2) - 2) and dest == ((hostIp * 2) - 1)):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(2)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=1000,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)

                        if(dest == ((hostIp * 2) - 2) and src == ((hostIp * 2) - 1)):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(1)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=1000,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)
                            
                        if(port < 5 and port > 2):
                            if((dest % 2 == 0) and ((dest >= ((hostIp * 2) - 2)) and (dest <= ((hostIp * 2) - 1)))):
                                match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                                action = sw.ofproto_parser.OFPActionOutput(1)
                                mod = sw.ofproto_parser.OFPFlowMod(
                                        datapath=sw, match=match, cookie=0,
                                        command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                        priority=100,
                                        flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                                sw.send_msg(mod)
                            elif((dest % 2 == 1) and ((dest >= ((hostIp * 2) - 2)) and (dest <= ((hostIp * 2) - 1)))):
                                match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                                action = sw.ofproto_parser.OFPActionOutput(2)
                                mod = sw.ofproto_parser.OFPFlowMod(
                                        datapath=sw, match=match, cookie=0,
                                        command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                        priority=1000,
                                        flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                                sw.send_msg(mod)
                        
                        if(port < 3):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(3)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)
                        
        elif (hostIp < 17):
            modHostIp = hostIp % 8;
            for port in range(1,5):
                for dest in range(16):
                    for src in range(16):
                        if((((modHostIp * 2) - 2) > dest or ((modHostIp * 2) + 1) < dest) and port > 2):
                            continue

                        if((((modHostIp * 2) - 2) > src or ((modHostIp * 2) + 1) < src) and port < 3):
                            continue
                            
                        if (src == dest):
                            continue
                        
                        vlan = src * 1000 + dest

                        if(port < 5 and port > 2):
                            if(dest >= ((modHostIp * 2) - 2) and dest <= ((modHostIp * 2) - 1)):
                                match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                                action = sw.ofproto_parser.OFPActionOutput(1)
                                mod = sw.ofproto_parser.OFPFlowMod(
                                        datapath=sw, match=match, cookie=0,
                                        command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                        priority=1000,
                                        flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                                sw.send_msg(mod)
                            elif(dest >= (modHostIp * 2) and dest <= ((modHostIp * 2) + 1)):
                                match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                                action = sw.ofproto_parser.OFPActionOutput(2)
                                mod = sw.ofproto_parser.OFPFlowMod(
                                        datapath=sw, match=match, cookie=0,
                                        command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                        priority=1000,
                                        flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                                sw.send_msg(mod)
                            
                        if(port < 3 and (dest < ((modHostIp * 2) - 2) or (dest > (modHostIp * 2) + 1))):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(3)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)
                        elif(port < 3 and ((dest >= ((modHostIp * 2) - 2)) and (dest <= ((modHostIp * 2) - 1)))):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(1)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)                        
                        elif(port < 3 and ((dest >= (modHostIp * 2)) and (dest <= ((modHostIp * 2) + 1)))):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(2)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)                                                    
        else:
            for port in range(1,5):
                for dest in range(16):
                    for src in range(16):
                        if (src == dest):
                            continue
                        
                        vlan = src * 1000 + dest
                        
                        if (dest >= 0 and dest < 4):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(1)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)                        
                        elif (dest >= 4 and dest < 8):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(2)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)                        
                        elif (dest >= 8 and dest < 12):
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(3)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)
                        else:
                            match = sw.ofproto_parser.OFPMatch(in_port=port, dl_vlan=vlan)
                            action = sw.ofproto_parser.OFPActionOutput(4)
                            mod = sw.ofproto_parser.OFPFlowMod(
                                    datapath=sw, match=match, cookie=0,
                                    command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
                                    priority=100,
                                    flags=ofproto.OFPFF_SEND_FLOW_REM, actions=[action])
                            sw.send_msg(mod)                                                    
                    
    # the rest of the code
    @set_ev_cls(dpset.EventDP)
    def switchStatus(self, ev):
        print("Switch %s: %s!" %
                (ev.dp.id, "connected" if ev.enter else "disconnected"))

        self.prepareSwitch(ev.dp)
