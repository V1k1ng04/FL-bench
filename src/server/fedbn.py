from copy import deepcopy

from src.client.fedbn import FedBNClient
from src.server.fedavg import FedAvgServer
from src.utils.tools import NestedNamespace


class FedBNServer(FedAvgServer):
    def __init__(
        self,
        args: NestedNamespace,
        algo: str = "FedBN",
        unique_model=False,
        use_fedavg_client_cls=False,
        return_diff=False,
    ):
        super().__init__(args, algo, unique_model, use_fedavg_client_cls, return_diff)
        init_bn_params = dict(
            (key, param)
            for key, param in self.model.state_dict().items()
            if "bn" in key
        )
        for params_dict in self.clients_personal_model_params.values():
            params_dict.update(deepcopy(init_bn_params))
        self.init_trainer(FedBNClient)
