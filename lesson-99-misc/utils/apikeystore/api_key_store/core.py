"""
used at ~\projects\ai\langchain_crash_course

this file was called "secrets.py", 
then get following error reported in:
https://stackoverflow.com/questions/73055157/what-does-importerror-cannot-import-name-randbits-mean

TODO:
=========
- add encryption
- add update key
- create a python pkg

"""

import yaml
from os.path import expanduser
from pathlib import Path

class ApiKeyStore():
    def __init__(self, store_path="~/api_keys/stores.yaml"):
        file_path = expanduser(store_path) if "~" in store_path else store_path
        with open(Path(file_path), encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
            self.api_providers = self.cfg.keys()
            
    def list_api_providers(self):
        return self.api_providers
        
    def get_api_key(self, provider="OPENAI"):
        sub_cat = ""
        if "/" in provider:
            x = provider.split("/")
            if len(x) > 0:
                provider = x[0]
            sub_cat = x[1] if len(x) > 1 else ""
        elif "." in provider:
            x = provider.split(".")
            if len(x) > 0:
                provider = x[0]
            sub_cat = x[1] if len(x) > 1 else ""

        if provider not in self.api_providers:
            print(f"{provider} not found in {self.api_providers}")
            return None
        
        cfg = self.cfg.get(provider)
        if "API_KEY" in cfg.keys():
            return cfg.get("API_KEY", None)
        else:
            return cfg[sub_cat].get("API_KEY") if sub_cat else None

            
if __name__ == "__main__":
    s = ApiKeyStore()
    # print(f"API Providers: {s.list_api_providers()}")
        
    API_KEYS = {}
    for p in s.api_providers:
        cfg = s.cfg[p]
        if "API_KEY" in cfg:
            API_KEYS[f"{p}_API_KEY"] = s.get_api_key(p)
        else:
            for sub_cat in [k for k in cfg.keys() if k not in ["ORG_ID", "MODELS", "DESCRIPTION", "Chat_URL"]]:
                API_KEYS[f"{p}_API_KEY_{sub_cat}"] = s.get_api_key(f"{p}/{sub_cat}")

    print(API_KEYS)

