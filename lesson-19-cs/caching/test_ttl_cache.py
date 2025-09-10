from ttl_cache import download_data , cache 
from time import sleep


@cache(ttl=10)  # Cache for 10 seconds
def cached_call_10sec():
    """
    Simulates a function that takes time to execute.
    This function will be cached for 10 seconds.
    """
    return download_data() 

@cache(ttl=20)  # Cache for 10 seconds
def cached_call_20sec():
    """
    Simulates a function that takes time to execute.
    This function will be cached for 10 seconds.
    """
    return download_data() 


# First call
resp = cached_call_10sec()
print(resp['local_call_time'])  

resp2 = cached_call_20sec()
print(resp2['local_call_time'])  

sleep(5)  # Wait for 5 seconds
print("\nAfter 5 seconds...")

resp = cached_call_10sec()
print(resp['local_call_time'])  

resp2 = cached_call_20sec()
print(resp2['local_call_time'])  

sleep(6)  # Wait for 6 seconds
print("\nAfter another 6 seconds...")


resp = cached_call_10sec()
print(resp['local_call_time'])  

resp2 = cached_call_20sec()
print(resp2['local_call_time'])  

sleep(10)  # Wait for 6 seconds
print("\nAfter another 10 seconds...")


resp = cached_call_10sec()
print(resp['local_call_time'])  

resp2 = cached_call_20sec()
print(resp2['local_call_time'])  
