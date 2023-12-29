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
        
        headers = {
            'User-Agent': str(user_agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': str(accept_language),
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'Alt-Used': 'www.google.com',
            'Connection': 'keep-alive',
            # 'Cookie': '1P_JAR=2023-07-27-17; AEC=Ad49MVG_ccMAPEzRQE8DkRmC3pAL-EZglBiEzRUpP-Mb2vscaSsy-Eu2JA; NID=511=hXdVZyVD5m8CBiC7WacKkAjiymyWaVirOAvRQzesXY1pEY5TX1I5Yy7U2X1OoZBLeTbl6KgacytoGwBHYpEKW0cTtNCKSHsyB3SDXI_hNucfAHLih17TGHiKO08LJZFeChAtViIk4mfdNOKGyGjaS0dJ45ggoTG39qr8Ta2N7n2mCRLHF0pSQE3dGPcVr0LTZONCcU7zpstwER1mAI2UFFD9ksMb37_La0_DayBLjya6FBpGHRRovlPIljJ9zxOwJ0yYudAKZeI; ANID=AHWqTUlIgXpfE1nWyqrXDvp1rtnvRoE-jDie8nkq-dRDsOkLYUxQBAnf9aiJHv0L; SEARCH_SAMESITE=CgQI7JgB; DV=Y5wX197puzErYH8oIYu_J3hZlwKGmVh_Hk7tc0SfCwIAAAA',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        
        url = 'https://www.google.com/search'
        params = {
            'q': str(query),
            'tbm': 'nws',
            #'start': str(start),
            #'filter' : '0',
            'tbs' : str(date_range)
        }
        
        response = requests.get(
            url,
            cookies=cookies,
            params=params,
            headers=headers,
        )
    
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