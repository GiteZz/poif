from poif.base_classes import Parameters
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PneunomiaParameters:
    num_epochs: int
    batch_size: int
    lr: float


pneunomia_param = PneunomiaParameters(num_epochs=50,
                                      batch_size=4,
                                      lr=0.001
                                      )