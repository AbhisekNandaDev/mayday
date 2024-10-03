import requests
import json

# Replace with your OpenAI API key
api_key = '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'
endpoint = 'https://api.openai.com/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

functions = [
    {
        "name": "emergency_response",
        "description": "Responds to emergency situations with service assignment, precautionary steps, and visual representation.",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {
                    "type": "string",
                    "description": "Category of the helper (Ambulance, Police, etc.)"
                },
                "precautionary_steps": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Safety instructions to follow while waiting for help and reply in same language."
                },
                "longitude": {
                    "type": "number",
                    "description": "Extracted longitude or null."
                },
                "latitude": {
                    "type": "number",
                    "description": "Extracted latitude or null."
                },
                "location": {
                    "type": "string",
                    "description": "Extracted general location or null."
                }
            },
            "required": ["service", "precautionary_steps", "longitude", "latitude", "location"]
        }
    }
]


user_query = "ମୋ ଗୋଡ଼ ଭାଙ୍ଗିଯାଇଛି back of mahima tower hanspal"  # Example user query

data = {
    'model': 'gpt-4o-mini',  # Use the appropriate model
    'messages': [
        {'role': 'user', 'content': user_query}
    ],
    'functions': functions,
    'function_call': {"name": "emergency_response"}  # Specify the function to call
}

response = requests.post(endpoint, headers=headers, json=data)

# Get the JSON response
json_response = response.json()

# Print the JSON output
print(json_response["choices"][0]["message"]["function_call"]["arguments"])
