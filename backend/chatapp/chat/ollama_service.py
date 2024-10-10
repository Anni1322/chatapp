# import ollama
# def generate_response(user_input):
#     response = ollama.generate(model="llama3", prompt=user_input)
#     print(response)  # Print the response to inspect the structure
#     return response  # Temporarily return the whole response to debug



# import time
# import ollama
# def generate_response(user_input):
#     start_time = time.time()  # Capture the start time
#     # Send the request to the Ollama model
#     response = ollama.generate(model="llama3", prompt=user_input)
#     end_time = time.time()  # Capture the end time
#     response_time = end_time - start_time  # Calculate the duration
#     print(f"Response Time: {response_time:.2f} seconds")  # Print or log the response time
#     return response['response'], response_time  # Return the response text and response time



from django.core.cache import cache  # Import Django's cache framework
import ollama
import time
from asgiref.sync import sync_to_async

@sync_to_async
def generate_response(user_input):
    # Create a unique cache key based on the user's input
    safe_input = user_input.replace(':', '_').replace(' ', '_')
    cache_key = f"response_{safe_input}"
    # Check if the response is already cached
    cached_response = cache.get(cache_key)
    if cached_response:
        print("Returning cached response.")
        return cached_response['response'], cached_response['response_time']  # Return cached data
    start_time = time.time()  # Capture the start time
    # Send the request to the Ollama model
    response = ollama.generate(model="llama3", prompt=user_input)
    end_time = time.time()  # Capture the end time
    response_time = end_time - start_time  # Calculate the duration
    

    # Save the response and response time in the cache for faster retrieval
    cache.set(cache_key, {'response': response['response'], 'response_time': response_time}, timeout=300)  # Cache for 5 minutes
    print(f"Response Time: {response_time:.2f} seconds")
    return response['response'], response_time  # Return the response
