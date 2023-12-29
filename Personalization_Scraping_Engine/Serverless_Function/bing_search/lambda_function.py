import json
import requests
from requests.exceptions import RequestException

def lambda_handler(event, context):
    try:
        start = event['start']
        query = event['query']
        date_range = event['date_range']

        accept_language = event['accept_language']
        user_agent = event['user_agent']
        login_state = event['login_state']
        cookies = event['cookies']
        
        # Headers
        headers = {
            'User-Agent': str(user_agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': str(accept_language),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        
        # Parameters separated into a dictionary
        params = {
            'q': str(query),
            'filters': 'ex1:"{}"'.format(str(date_range)),
            'FORM': '000017',
            'setlang': 'en',
            'search': 'Submit Query'
        }
        
        response = requests.get('https://www.bing.com/search', 
                                params=params, 
                                cookies=cookies, 
                                headers=headers)
        # Check if response is successful
        if response.status_code == 200:
            return {
                'statusCode': 200,
                'body': response.text
            }
        else:
            # Handle non-200 responses
            return {
                'statusCode': response.status_code,
                'body': f"Error: Received status code {response.status_code}"
            }
    except RequestException as e:
        # Handle exceptions raised by requests.get
        return {'statusCode': 500, 'body': f"Error: {str(e)}"}