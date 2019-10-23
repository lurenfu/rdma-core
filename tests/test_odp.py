from tests.base import RDMATestCase
from tests.utils import requires_odp, traffic
from tests.base import RCResources, UDResources
from pyverbs.mr import MR
import pyverbs.enums as e


class OdpUD(UDResources):
    @requires_odp('ud')
    def create_mr(self):
        self.mr = MR(self.pd, self.msg_size + self.GRH_SIZE ,
                     e.IBV_ACCESS_LOCAL_WRITE | e.IBV_ACCESS_ON_DEMAND)


class OdpRC(RCResources):
    @requires_odp('rc')
    def create_mr(self):
        self.mr = MR(self.pd, self.msg_size,
                     e.IBV_ACCESS_LOCAL_WRITE | e.IBV_ACCESS_ON_DEMAND)


class OdpTestCase(RDMATestCase):
    def setUp(self):
        super(OdpTestCase, self).setUp()
        self.iters = 100
        self.qp_dict = {'rc': OdpRC, 'ud': OdpUD}

    def create_players(self, qp_type):
        client = self.qp_dict[qp_type](self.dev_name, self.ib_port, self.gid_index)
        server = self.qp_dict[qp_type](self.dev_name, self.ib_port, self.gid_index)
        client.pre_run(server.psn, server.qpn)
        server.pre_run(client.psn, client.qpn)
        return client, server

    def test_odp_rc_traffic(self):
        client, server = self.create_players('rc')
        traffic(client, server, self.iters, self.gid_index, self.ib_port)

    def test_odp_ud_traffic(self):
        client, server = self.create_players('ud')
        traffic(client, server, self.iters, self.gid_index, self.ib_port)
