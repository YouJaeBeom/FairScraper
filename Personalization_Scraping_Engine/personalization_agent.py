import boto3
import pandas as pd
import json
import time
import random
import botocore
import os
import logging
import configparser
from HTML_Parsing_Engine.parser_management_module import ParserManagementModule
from Personalization_Scraping_Engine.date_range import DateRangeSetting
from Personalization_Scraping_Engine.Serverless_Function.google_search.aws_update import LambdaUpdater as google_search_lambda_updater
from Personalization_Scraping_Engine.Serverless_Function.google_news.aws_update import LambdaUpdater as google_news_lambda_updater
from Personalization_Scraping_Engine.Serverless_Function.bing_search.aws_update import LambdaUpdater as bing_search_lambda_updater
#from Personalization_Scraping_Engine.Serverless_Function.bing_news.aws_update import LambdaUpdater as bing_news_lambda_updater

# Constants
MAX_RETRIES = 3

# Read configuration from 'config.ini'
config = configparser.ConfigParser()
config.read('config.ini')

class PersonalizationAgent:
    def __init__(self, current_datetime, query, personalization_setting, personalization_option):
        self.setup_agent(current_datetime, query, personalization_setting, personalization_option)

    def setup_agent(self, current_datetime, query, personalization_setting, personalization_option):
        self.current_datetime = current_datetime
        self.query = query
        self.len_of_data = 0
        self.personalization_setting = personalization_setting
        self.personalization_option = personalization_option
        self.pf_setting = self.get_pf_setting()
        self.configure_aws()
        self.initialize_date_range_settings()
        self.parser = ParserManagementModule()

    def get_pf_setting(self):
        pf_setting_map = {
            'geo_information': 'region',
            'login_state': 'login_state',
            'os': 'os',
            'user_agent': 'user_agent_name',
            'accept_language': 'language'
        }
        
        return self.personalization_setting[pf_setting_map[self.personalization_option]]

    def configure_aws(self):
        session = boto3.session.Session()
        client_config = botocore.config.Config(read_timeout=100, connect_timeout=100, retries={"max_attempts": 3})
        self.client = session.client('lambda',
                                     aws_access_key_id=config['DEFAULT']['accessKey'],
                                     aws_secret_access_key=config['DEFAULT']['accessScretkey'],
                                     config=client_config,
                                     region_name=self.personalization_setting['region'])

    def initialize_date_range_settings(self):
        self.data_range = DateRangeSetting()
        self.convert_date_range_list, self.date_range_list = self.data_range.generate_date_range_list(self.personalization_setting['pir_system'])

    def aws_update(self):
        time.sleep(random.uniform(1, 10))
        lambda_updater_map = {
            'google_search': google_search_lambda_updater,
            'google_news': google_news_lambda_updater,
            'bing_search': bing_search_lambda_updater,
            'bing_news': bing_news_lambda_updater
        }
        if self.personalization_setting['pir_system'] in lambda_updater_map:
            updater = lambda_updater_map[self.personalization_setting['pir_system']]()
            updater.update_lambda_functions(specific_function_name=self.personalization_setting['functionName'])
        self.log_update_info()

    def log_update_info(self):
        result_print = f"query={self.query:<20}|PF setting={str(self.pf_setting):<30}|aws update ={self.personalization_setting['functionName']:<40}"
        print(result_print)
        logging.info(result_print)

    def scraping_requests(self):
        for idx, date_range in enumerate(self.convert_date_range_list):
            self.scrape_data_for_date_range(idx, date_range)

    def scrape_data_for_date_range(self, idx, date_range):
        page_number = 0
        start = 0
        retries = 0

        while retries < MAX_RETRIES:
            try:
                response_dict = self.invoke_lambda_function(idx, date_range, start, retries)
                success_flag = self.parse_response(response_dict, idx, date_range)
                if success_flag:
                    break
                else:
                    retries += 1
            except Exception as e:
                self.handle_exception(e, idx, date_range)
                self.aws_update()
                retries += 1

    def invoke_lambda_function(self, idx, date_range, start, retries):
        payload = json.dumps({
            "start": start,
            "query": self.query,
            "region": self.personalization_setting['region'],
            "accept_language": self.personalization_setting['accept_language'],
            "user_agent": self.personalization_setting['user_agent'],
            "login_state": self.personalization_setting['login_state'],
            "cookies": self.personalization_setting['cookies'],
            "date_range": date_range
        })
        response = self.client.invoke(FunctionName=self.personalization_setting['functionName'], Payload=payload, InvocationType="RequestResponse")
        response = response['Payload'].read().decode('utf-8')
        
        response_print = "query={0:<20}|PF setting={1:<30}|date={2:<20}|client StatusCode={3:<20}|retries={4}".format(
            self.query,
            str(self.pf_setting),
            str(self.date_range_list[idx]),
            str(json.loads(response)['statusCode']),
            str(retries)
        )
        print(response_print)
        logging.info(response_print)
        time.sleep(random.uniform(1, 3))
        
        return json.loads(response)

    def parse_response(self, response_dict, idx, date_range):
        if response_dict['statusCode'] != 200:
            raise Exception(response_dict['body'])
        parse_flag = self.parse_and_save_data(response_dict, idx, date_range)
        
        if parse_flag:
            return True
        else:
            return False

    def parse_and_save_data(self, response_dict, idx, date_range):
        parser_method = getattr(self.parser, f"{self.personalization_setting['pir_system']}_parser", None)
        if parser_method:
            self.titles, self.contents, self.detail_contents, self.urls = parser_method(response_dict, self.query, self.pf_setting, self.date_range_list[idx], self.personalization_setting['os'])
            self.len_of_data += len(self.titles)
        
        if not self.titles and not self.contents and not self.detail_contents and not self.urls:
            self.aws_update()
            return False
        else:
            self.save_data(idx, date_range)
            return True

    def save_data(self, idx, date_range):
        df = pd.DataFrame({'titles': self.titles, 'contents': self.contents, 'detail_content': self.detail_contents, 'urls': self.urls})
        output_file = self.get_output_file_path(idx, date_range)
        file_mode = 'a' if os.path.exists(output_file) else 'w'
        df.to_csv(output_file, mode=file_mode, index=False, header=not os.path.exists(output_file))
        self.log_result(idx, date_range)

    def get_output_file_path(self, idx, date_range):
        output_dir = f"./Data/PIR/{self.personalization_setting['pir_system']}/{self.personalization_option}/{self.query}/{self.current_datetime}/"
        os.makedirs(output_dir, exist_ok=True)
        return f"{output_dir}{self.personalization_setting['region']}_{self.personalization_setting['user_agent_name']}_{self.personalization_setting['accept_language']}_{self.personalization_setting['login_state']}_results.csv"

    def log_result(self, idx, date_range):
        result_print = f"query={self.query:<20}|PF setting={str(self.pf_setting):<30}|date={str(self.date_range_list[idx]):<20}|data length={self.len_of_data:<10}"
        print(result_print)
        logging.info(result_print)

    def handle_exception(self, e, idx, date_range):
        exception_print = f"query={self.query:<20}|PF setting={str(self.pf_setting):<30}|date={str(self.date_range_list[idx]):<20}|error={str(e):<40}"
        print(exception_print)
        logging.info(exception_print)
        time.sleep(random.uniform(3, 5))