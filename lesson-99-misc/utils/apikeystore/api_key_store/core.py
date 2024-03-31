"""
used at ~\projects\ai\langchain_crash_course

TODO:
=========
- add encryption
- add update key

"""

import yaml
from os.path import expanduser
from pathlib import Path

class ApiKeyStore():
    def __init__(self, store_path="~/.api_keys/stores.yaml"):
        file_path = expanduser(store_path) if "~" in store_path else store_path
        with open(Path(file_path), encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
            self.api_providers = self.cfg.keys()

    def list_api_providers(self):
        return self.api_providers

    def get_api_key(self, provider="OPENAI"):
        if provider not in self.api_providers:
            print(f"{provider} not found in {self.api_providers}")
            return { provider : "" }

        p = self.cfg.get(provider)
        if "API_KEY" in p.keys():
            return { f"{provider}_API_KEY" : p.get("API_KEY") }

        res = {}
        sub_cat = [i for i in p.keys() if i not in ["ORG_ID", "MODELS", "DESCRIPTION"]]
        if not sub_cat:
            return {}

        for kn in sub_cat:
            res.update({ f"{provider}_{kn}_API_KEY" : p[kn].get("API_KEY") })

        return res


if __name__ == "__main__":
    s = ApiKeyStore(store_path="./store.template.yaml")
    print(f"API Providers: {s.list_api_providers()}")

    API_KEYS = {}
    for p in s.api_providers:
        API_KEYS.update(s.get_api_key(p))
    print(API_KEYS)
