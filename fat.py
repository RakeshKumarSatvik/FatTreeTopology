from mininet.topo import Topo

class FatTopo(Topo):
    def __init__(self, count):
        Topo.__init__(self)
        vertexCount = count

        self.hosts_ = [
                self.addHost('h%d' % hostId, ip='10.0.%d/27' % hostId)
                for hostId in range(((vertexCount/2)**2) * vertexCount)]

        self.switches_ = [
                self.addSwitch('Edge%d' % switchId, dpid=("%0.2X" % (switchId+1)))
                for switchId in range(vertexCount * vertexCount / 2)]

        self.switches_ = [
                self.addSwitch('Aggr%d' % switchId, dpid=("%0.2X" % ((vertexCount * vertexCount / 2) + switchId+1)))
                for switchId in range(vertexCount * vertexCount / 2)]
				
        self.switches_ = [
                self.addSwitch('Core%d' % switchId, dpid=("%0.2X" % ((vertexCount * vertexCount) + switchId+1)))
                for switchId in range((vertexCount/2)**2)]
        
        for loop in range(vertexCount/2):
            self.hostLinks_ = [
                    self.addLink('h%d' % eId, 'Edge%d' % (eId / (vertexCount / 2)))
                    for eId in xrange(loop, (((vertexCount/2)**2) * vertexCount), vertexCount / 2)]

        for loop in range(vertexCount/2):
            self.switchLinks_ = [
                    self.addLink('Edge%d' % (loop + (eId / (vertexCount / 2)) * (vertexCount / 2)), 'Aggr%d' % eId)
                    for eId in xrange(0, vertexCount * vertexCount / 2, 1)]                

        self.switchLinks_ = [
                self.addLink('Core%d' % (eId % ((vertexCount/2)**2)), 'Aggr%d' % (eId / (vertexCount / 2)))
                for eId in xrange(0, ((vertexCount/2)**2) * vertexCount, 1)]                

    @classmethod
    def create(cls, count=4):
        return cls(count)

topos = {'fattopo': FatTopo.create}
