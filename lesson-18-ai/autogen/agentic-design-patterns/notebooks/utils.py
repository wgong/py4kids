# Add your utilities or helper functions to this file.

# import os
# from dotenv import load_dotenv, find_dotenv

# # these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService                                                                                                                                     
# def load_env():
#     _ = load_dotenv(find_dotenv())

# def get_openai_api_key():
#     load_env()
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     return openai_api_key

def get_api_key(key_name="OPENAI/Yiwen"):
    from api_key_store import ApiKeyStore
    return ApiKeyStore().get_api_key(key_name)

if __name__ == "__main__":
    print(get_api_key())
    print(get_api_key("GROQ"))