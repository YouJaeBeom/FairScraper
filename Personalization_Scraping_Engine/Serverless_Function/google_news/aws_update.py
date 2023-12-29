import boto3
import botocore
import configparser
import json
import os
import time
import zipfile
from queue import Queue
from threading import Thread
import logging

class LambdaUpdater:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # Read configuration
        config = configparser.ConfigParser()
        config_file_path = os.path.join(self.current_dir, '../../../config.ini')
        config.read(config_file_path)

        self.file_to_zip = os.path.join(self.current_dir, './lambda_function.py')
        self.output_zip_name = os.path.join(self.current_dir, 'lambda_function.zip')
        self.serverless_function_file = config['DEFAULT']['SERVERLESS_FUNCTION_SETTING_FILE']
        self.region_file = config['DEFAULT']['SERVERLESS_FUNCTION_SETTING_FILE']

        self._zip_lambda_function()
        serverless_function_file_path = os.path.join(self.current_dir, f"../../../{self.serverless_function_file}")
        region_file_path = os.path.join(self.current_dir, f"../../../{self.region_file}")
        self.serverless_function_json = json.load(open(serverless_function_file_path, 'r'))
        self.region_json = json.load(open(region_file_path, 'r'))


    def _zip_lambda_function(self):
        with zipfile.ZipFile(self.output_zip_name, 'w') as zipf:
            zipf.write(self.file_to_zip, arcname=os.path.basename(self.file_to_zip))
    
    def update_lambda_functions(self, specific_function_name=None):
        start = time.time()

        serverless_function_list = [sf['arn'] for sf in self.serverless_function_json['google_news']]
        region_list = [region['region'] for region in self.region_json['google_news']]

        queue = Queue()

        if specific_function_name:
            # Find the index and region of the specific function
            for index, arn in enumerate(serverless_function_list):
                if specific_function_name in arn:
                    region = region_list[index]
                    queue.put((index, region, arn))
                    break
        else:
            # If no specific function name is given, enqueue all functions
            for index, region in enumerate(region_list):
                queue.put((index, region, serverless_function_list[index]))

        # Start worker threads
        for _ in region_list:
            worker = ScrapingWorker(queue)
            worker.daemon = True
            worker.start()

        queue.join()

        end = time.time()
        #print("Execution time:", end - start)

    """def update_lambda_functions(self):
        start = time.time()

        serverless_function_list = [sf['arn'] for sf in self.serverless_function_json['google_search']]
        region_list = [region['region'] for region in self.region_json['google_search']]

        queue = Queue()

        for _ in region_list:
            worker = ScrapingWorker(queue)
            worker.daemon = True
            worker.start()

        for index, region in enumerate(region_list):
            queue.put((index, region, serverless_function_list[index]))

        queue.join()

        end = time.time()
        print("Execution time:", end - start)"""

class ScrapingWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.queue = queue
        config = configparser.ConfigParser()
        config_file_path = os.path.join(self.current_dir, '../../../config.ini')
        config.read(config_file_path)

        self.accessKey = config['DEFAULT']['accessKey']
        self.accessScretkey = config['DEFAULT']['accessScretkey']

        zipped_code_path = os.path.join(self.current_dir, 'lambda_function.zip')
        with open(zipped_code_path, 'rb') as f:
            self.zipped_code = f.read()
        
    
    def run(self):
        index, region, functionName = self.queue.get()

        session = boto3.session.Session()
        client = session.client('lambda',
                                aws_access_key_id=self.accessKey,
                                aws_secret_access_key=self.accessScretkey,
                                region_name=region)
        
        # Retry logic
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = client.update_function_code(
                    FunctionName=functionName,
                    ZipFile=self.zipped_code
                )
                # Wait for update to be successful
                while True:
                    time.sleep(1)
                    response = client.get_function(FunctionName=functionName)
                    if response['Configuration']['LastUpdateStatus'] == 'Successful':
                        break
                break  # Exit the retry loop if successful
            except Exception as e:
                if e.response['Error']['Code'] == 'ResourceConflictException' and attempt < max_retries - 1:
                    logging.warning(f"Update in progress, retrying {functionName} (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(10)  # Wait before retrying
                else:
                    logging.error(f"Failed to update {functionName}: {e}")
                    break
        #print("COMPELETE ", index, region, functionName)
        self.queue.task_done()

# Example usage
if __name__ == '__main__':
    lambda_updater = LambdaUpdater()
    lambda_updater.update_lambda_functions()
