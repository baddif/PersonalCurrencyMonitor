# Copyright (c) [2025] [Yifu Ding]
import uuid


class ConvertConfig:

    def __init__(self) -> None:
        super().__init__()
        self.uuid = str(uuid.uuid4())
        self.from_currency = ""
        self.to_currency = ""
        self.from_paid_period_idx = -1
        self.from_amount = 0

    def to_dict(self):
        return {"uuid": self.uuid, "from_currency": self.from_currency, "to_currency": self.to_currency,
                "from_paid_period_idx": self.from_paid_period_idx, "from_amount": self.from_amount}
    
    def load_from_dict(self, dict):
        vars(self).update(dict)
        # self.uuid = dict["uuid"]
        # self.from_currency = dict["from_currency"]
        # self.to_currency = dict["to_currency"]
        # self.from_paid_period_idx = dict["from_paid_period_idx"]
        # self.from_amount = dict["from_amount"]
