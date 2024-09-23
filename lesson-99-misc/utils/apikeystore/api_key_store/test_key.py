from api_key_store import *
s = ApiKeyStore()
open_api_key = s.get_api_key("OPENAI/Wen")
serp_api_key = s.get_api_key("SerpApi")

if __name__ == "__main__":
    print(f"open_api_key : {open_api_key}")
    print(f"serp_api_key : {serp_api_key}")
