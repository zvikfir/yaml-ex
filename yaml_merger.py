from abc import ABC, abstractmethod

import yaml


class YamlMerger(ABC):
    @abstractmethod
    def merge(self, yml: str, yml_config: str):
        pass


class YamlMergerImpl(YamlMerger):

    def __extend_dict(self, extend_me, extend_by):
        for k, v in extend_me.items():
            if isinstance(v, list) and isinstance(extend_by, list):
                if v[0].keys() == extend_by[0].keys():
                    v.extend(extend_by)
                else:
                    for e in v:
                        self.__extend_dict(e, extend_by)
            elif isinstance(v, dict) and isinstance(extend_by, list):
                if v.keys() == extend_by[0].keys():
                    extend_me[k] = [v] + extend_by
                else:
                    self.__extend_dict(v, extend_by)
            elif isinstance(v, list) and isinstance(extend_by, dict):
                if v[0].keys() == extend_by.keys():
                    v.append(extend_by)
                else:
                    for e in v:
                        self.__extend_dict(e, extend_by)
            elif isinstance(v, dict) and isinstance(extend_by, dict):
                if v.keys() == extend_by.keys():
                    extend_me[k] = [v, extend_by]
                else:
                    self.__extend_dict(v, extend_by)

    def merge(self, yml: str, yml_config: str):
        yml_dict = yaml.full_load(yml)
        self.__extend_dict(yml_dict, yaml.full_load(yml_config))

        return yaml.safe_dump(yml_dict, sort_keys=False)
