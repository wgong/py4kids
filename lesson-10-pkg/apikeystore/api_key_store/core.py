"""
TODO:
- add encryption
- add update key

"""

import yaml
from os.path import expanduser
from pathlib import Path

class ApiKeyStore():
    def __init__(self, store_path="./store.template.yaml"):
        file_path = expanduser(store_path) if "~" in store_path else store_path
        with open(Path(file_path), encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
            self.api_providers = self.cfg.keys()
            
    def get_api_key(self, provider="OPENAI", key_name=""):
        if provider not in self.api_providers:
            raise Exception(f"{provider} not found in {self.api_providers}")
        p = self.cfg.get(provider)
        
        if provider != "HUGGING_FACE":
            return p.get("API_KEY", "HF_WRITE")

        # provider has multiple keys, must provide key_name
        if not key_name:
            key_name="HF_READ"

        k = p.get("API_KEY", {})
        if key_name not in k.keys():
            raise Exception(f"{provider} API Key {key_name} not found")
        return k.get(key_name, "")

if __name__ == "__main__":
    if True:  # False:  # 
        s = ApiKeyStore()
        for p in s.api_providers:
            if p == "HUGGING_FACE":
                for k in ["HF_READ", "HF_WRITE"]:
                    api_key = s.get_api_key(p, key_name=k)
                    print(f"{p}/{k} API Key : {api_key}")
            else:
                api_key = s.get_api_key(p)
                print(f"{p} API Key : {api_key}")