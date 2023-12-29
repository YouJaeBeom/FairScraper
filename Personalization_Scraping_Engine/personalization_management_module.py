import random
import json
from itertools import product
import configparser

# Read configuration from 'config.ini'
config = configparser.ConfigParser()
config.read('config.ini')

class PersonalizationManagementModule:
    def __init__(self, pir_system):
        # Serverless function setting
        self.serverless_function_file = config['DEFAULT']['SERVERLESS_FUNCTION_SETTING_FILE']
        self.serverless_function_json = json.load(open(self.serverless_function_file, 'r'))
        self.default_serverless_function = [self.serverless_function_json[pir_system][2]]

        # Region setting
        self.region_file = config['DEFAULT']['SERVERLESS_FUNCTION_SETTING_FILE']
        self.region_json = json.load(open(self.region_file, 'r'))
        self.region_list = [region['region'] for region in self.region_json['google_search']]
        self.default_region = [self.region_json[pir_system][0]]

        # User agent setting
        self.user_agent_file = config['DEFAULT']['USER_AGENT_SETTING_FILE']
        self.user_agent_json = json.load(open(self.user_agent_file, 'r'))
        self.user_agent_list = [user_agent for user_agent in self.user_agent_json]
        self.default_user_agent = [self.user_agent_json[0]] 

        # Accept language setting
        self.accept_language_file = config['DEFAULT']['ACCEPT_LANGUAGE_SETTING_FILE']
        self.accept_language_json = json.load(open(self.accept_language_file, 'r'))
        self.accept_language_list = [accept_language for accept_language in self.accept_language_json]
        self.default_accept_language = [self.accept_language_json[0]]

        # Login/logout notusecookies setting
        self.login_state_file = config['DEFAULT']['LOGIN_STATE_SETTING_FILE']
        self.login_state = json.load(open(self.login_state_file, 'r'))
        self.default_login_state = ['not_use_cookies']

    def numofthread(self, option_list):
        # Calculate the number of threads based on selected options
        self.option_list = option_list
        self.num_of_thread = 1
        for option in option_list:
            if option == "geo_information":
                self.num_of_thread *= len(self.region_list)
            elif option == "login_state":
                self.num_of_thread *= len(self.login_state)
            elif option == "user_agent":
                self.num_of_thread *= len(self.user_agent_list)
            elif option == "accept_language":
                self.num_of_thread *= len(self.accept_language_list)
        return self.num_of_thread

    def optionSetting(self, pir_system, option_list):
        self.pir_system = pir_system
        self.option_list = option_list

        # Default settings
        self.functionName_list = [function for function in self.serverless_function_json[pir_system]]
        self.function_name_set = (self.functionName_list) if 'geo_information' in self.option_list else self.default_serverless_function 
        self.region_set = set(self.region_list) if 'geo_information' in self.option_list else self.default_region
        self.user_agent_set = (self.user_agent_list) if 'user_agent' in self.option_list else self.default_user_agent
        self.accept_language_set = (self.accept_language_list) if 'accept_language' in self.option_list else self.default_accept_language
        self.login_state_set = set(self.login_state) if 'login_state' in self.option_list else self.default_login_state

        # Setting options
        self.setting_options = []
        self.setting_options.append(self.function_name_set)
        self.setting_options.append(self.user_agent_set)
        self.setting_options.append(self.accept_language_set)
        self.setting_options.append(self.login_state_set)

        # Generate option combinations
        option_combinations = list(product(*self.setting_options))
        self.personalization_setting = []

        for option_combination in option_combinations:
            setting = {}
            setting['pir_system'] = pir_system 
            setting['functionName'] = option_combination[0]['arn']
            setting['region'] = option_combination[0]['region']
            setting['os'] = option_combination[1]['OS']
            setting['user_agent'] = option_combination[1]['User-Agent']
            setting['user_agent_name'] = option_combination[1]['Environment']
            setting['accept_language'] = option_combination[2]['accept_language']
            setting['language'] = option_combination[2]['language']
            setting['login_state'] = option_combination[3]
            setting['cookies'] = self.login_state[option_combination[3]][pir_system]
            self.personalization_setting.append(setting)
        
        return self.personalization_setting