# from django.shortcuts import render

# # Create your views here.
# from django.http import JsonResponse
# from .ollama_service import generate_response
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response = generate_response(user_input)
#             return JsonResponse({'response': ai_response})
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.http import JsonResponse
from .ollama_service import generate_response
from django.views.decorators.csrf import csrf_exempt
import json
from asgiref.sync import sync_to_async

# for excel sheet read
import pandas as pd
import os
# for excel sheet read

# for train input 
import re
from difflib import SequenceMatcher
# for train input 

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response = generate_response(user_input)
#             return JsonResponse({'response': ai_response})  # Return the full response
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response, response_time = generate_response(user_input)
#             return JsonResponse({
#                 'response': ai_response,
#                 'response_time': response_time  # Include the response time in the JSON response
#             })
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)




# @csrf_exempt
# async def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')
#         if user_input:
#             ai_response = await generate_response(user_input)
#             return JsonResponse({'response': ai_response[0]})
#         return JsonResponse({'error': 'No message provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)





# for excel sheet read
# Get the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_excel_data():
    # Construct the file path
    file_path = os.path.join(BASE_DIR, 'chat', 'dataset', 'answers.xlsx')    
    try:
        # Load the Excel file
        df = pd.read_excel(file_path)
        print("Excel Data Loaded Successfully.")
        print(df)  # Print the entire DataFrame content to the console
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
# Load data and print it to the console
excel_data = load_excel_data()
# for excel sheet read


# for save 
# Save updated data back to the Excel sheet
def save_excel_data(df):
    file_path = os.path.join(BASE_DIR, 'chat', 'dataset', 'answers.xlsx')
    df.to_excel(file_path, index=False)
# for save 


# Function to search for the response in the Excel sheet
# def search_response(user_input, excel_data):
#     # Search for the row where the 'message' column matches the user_input
#     matching_rows = excel_data[excel_data['message'].str.lower() == user_input.lower()]
#     if not matching_rows.empty:
#         return matching_rows['answer'].values[0]  # Return the 'answer' if found
#     return None  # Return None if no match is found

# def search_response(user_input, excel_data):
#     # Normalize the user input to lowercase and tokenize (split into words)
#     user_input_tokens = user_input.lower().split()
    
#     for _, row in excel_data.iterrows():
#         stored_message = row['message']

#         # Check if stored_message is a string and normalize it
#         if isinstance(stored_message, str):
#             stored_message_tokens = stored_message.lower().split()

#             # Sort both token lists to ignore order
#             if sorted(user_input_tokens) == sorted(stored_message_tokens):
#                 return row['answer']  # Return the answer if found

#     return None  # Return None if no match is found



# Function to search for the response in the Excel sheet
def search_response(user_input, excel_data):
    # Normalize the user input to lowercase and tokenize (split into words)
    user_input_tokens = set(user_input.lower().split())
    
    for _, row in excel_data.iterrows():
        stored_message = row['message']

        # Check if stored_message is a string and normalize it
        if isinstance(stored_message, str):
            stored_message_tokens = set(stored_message.lower().split())

            # Check if all user input tokens are in the stored message tokens
            if user_input_tokens.issubset(stored_message_tokens):
                return row['answer']  # Return the answer if found

    return None  # Return None if no match is found


@csrf_exempt
async def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message')

        if user_input:
            # Load the Excel data
            excel_data = load_excel_data()
            if excel_data is not None:
                # Search for a response in the Excel sheet
                response_from_excel = search_response(user_input, excel_data)
                
                if response_from_excel:
                    return JsonResponse({'response': response_from_excel})

            # If no response found in Excel, generate response using AI model
            ai_response = await generate_response(user_input)
            generated_response = ai_response[0]

            # Append new message and response to the Excel data if it's not already there
            if excel_data is not None:
                # Check if the message already exists in the Excel data
                if not excel_data[excel_data['message'].str.lower() == user_input.lower()].empty:
                    # If the message already exists, do not append it again
                    return JsonResponse({'response': generated_response})

                # Create a new row with the user message and AI response
                new_row = {'message': user_input, 'answer': generated_response}
                
                # Append the new row to the existing Excel data
                updated_excel_data = excel_data._append(new_row, ignore_index=True)
                
                # Save the updated data back to the Excel sheet
                save_excel_data(updated_excel_data)
            
            return JsonResponse({'response': generated_response})
        
        return JsonResponse({'error': 'No message provided'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)








# Function to search for a response in the Excel sheet
# def search_response(user_input, excel_data):
#     user_input_words = set(user_input.lower().split())
#     best_match = None
#     highest_match_count = 0
    
#     # Iterate through each message in the excel_data
#     for index, row in excel_data.iterrows():
#         message_words = set(str(row['message']).lower().split())
#         common_words = user_input_words.intersection(message_words)
        
#         if len(common_words) > highest_match_count:
#             highest_match_count = len(common_words)
#             best_match = row['answer']
    
#     return best_match if best_match else None


# @csrf_exempt
# async def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_input = data.get('message')

#         if user_input:
#             # Load the Excel data
#             excel_data = load_excel_data()
#             if excel_data is not None:
#                 # First, search for a response in the Excel sheet
#                 response_from_excel = search_response(user_input, excel_data)
#                 if response_from_excel:
#                     return JsonResponse({'response': response_from_excel})
#             # If no response found in the Excel, generate response using AI model
#         ai_response = await generate_response(user_input)
#         return JsonResponse({'response': ai_response[0]})
        
#         return JsonResponse({'error': 'No message provided'}, status=400)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)





