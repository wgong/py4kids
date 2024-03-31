import api_key_store

s = api_key_store.ApiKeyStore(store_path="../api_key_store/store.template.yaml")
print(f"API providers: {s.list_api_providers()}\n")

API_KEYS = {}
for p in s.api_providers:
    API_KEYS.update(s.get_api_key(p))
print(API_KEYS)
