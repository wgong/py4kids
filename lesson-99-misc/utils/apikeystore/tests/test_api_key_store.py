import api_key_store as aks

s = aks.ApiKeyStore()
print(f"API providers: {s.list_api_providers()}\n")

for p in s.api_providers:
    if p == "HUGGING_FACE":
        for k in ["HF_READ", "HF_WRITE"]:
            api_key = s.get_api_key(p, key_name=k)
            print(f"{p}/{k} API Key : {api_key}")
    else:
        api_key = s.get_api_key(p)
        print(f"{p} API Key : {api_key}")