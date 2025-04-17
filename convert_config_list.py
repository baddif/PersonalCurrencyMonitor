# Copyright (c) [2025] [Yifu Ding]
from typing import Any
import json
import convert_config_class
from singleton_meta import SingletonMeta
    
class ConfigList(metaclass=SingletonMeta):

    def __init__(self, config_file_path) -> None:
        self.file_path = config_file_path
        self.config_list = []
        self.load_config()
    
    def save_config(self):
        with open( self.file_path, "w") as f:
            json.dump([obj.to_dict() for obj in self.config_list], f)

    def load_config(self):
        try:
            with open(self.file_path, "r") as f:
                loaded_obj_list = json.load(f)
                for obj in loaded_obj_list:
                    obj_conf = convert_config_class.ConvertConfig()
                    obj_conf.load_from_dict(obj)
                    self.config_list.append(obj_conf)
        except FileNotFoundError:
            print(f"Config file: {self.file_path} not found")
        except json.JSONDecodeError:
            print(f"{self.file_path} is empty or not valid")

    def update(self, uuid, **kwargs):
        for item in self.config_list:
            if item.uuid == uuid:
                vars(item).update(kwargs)
                break;
        self.save_config()

    def get_item(self, uuid):
        for item in self.config_list:
            if item.uuid == uuid:
                return item
        return None
    
    def add(self):
        config_item = convert_config_class.ConvertConfig();
        self.config_list.append(config_item)
        self.save_config()
        return config_item.uuid
    
    def remove(self, uuid):
        new_list = [item for item in self.config_list if item.uuid != uuid]
        self.config_list = new_list
        self.save_config()
    
    def is_empty(self):
        return len(self.config_list) == 0

config_list = ConfigList("config.json");