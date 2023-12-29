import logging
import os
import sys
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from datetime import datetime
import configparser
from itertools import repeat

from Personalization_Scraping_Engine.personalization_management_module import PersonalizationManagementModule
from Personalization_Scraping_Engine.personalization_agent import PersonalizationAgent


def setup_logging(output_file):
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Set up new logging configuration
    logging.basicConfig(
        filename=output_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# Define a worker class for scraping tasks
class AgentGenerator(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        # Get task parameters from the queue
        current_datetime, query, personalization_setting, personalization_option = self.queue.get()
        print(current_datetime, query, personalization_setting)
        
        # Create a personalization agent and initiate scraping
        agent = PersonalizationAgent(current_datetime, query, personalization_setting, personalization_option)
        agent.scraping_requests()
        
        # Indicate that the task is done
        self.queue.task_done()

if __name__ == '__main__':
    start_time = time.time()

    # Read configuration from 'config.ini'
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extract configuration values
    query = config['DEFAULT']['QUERY'].split(',')
    personalization_option = config['DEFAULT']['PERSONZALIZATION_OPTION'].split(',')

    for p in personalization_option:
        for q in query:
            print("Start", q, p)

            pir_system = config['DEFAULT']['PIR_SYSTEM']
            current_datetime = datetime.now().strftime("%Y%m%d_%H%M")
            # Configure the output log file location
            output_dir = "./Log/{}/".format(pir_system)
            logfile = "{}_{}_{}".format(current_datetime, q, p)
            output_file = "{}{}.log".format(output_dir, logfile)

            # Create the output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Set up logging using the specified output file
            setup_logging(output_file)

            # Initialize the personalization management module
            personalization_management_module_instant = PersonalizationManagementModule(pir_system)
            
            # Get the number of threads to use based on personalization options
            num_of_thread = personalization_management_module_instant.numofthread(p)
            
            # Retrieve a list of personalization settings
            personalization_setting_list = personalization_management_module_instant.optionSetting(pir_system, p)

            # Create a queue for task distribution
            queue = Queue()

            # Create and start worker threads
            for _ in personalization_setting_list:
                worker = AgentGenerator(queue)
                worker.daemon = True
                worker.start()

            # Populate the queue with tasks
            for indx, personalization_setting in enumerate(personalization_setting_list):
                queue.put((current_datetime, q, personalization_setting, p))

            # Wait for all tasks in the queue to finish
            queue.join()

            end_time = time.time()
            print("Execution time:", end_time - start_time)
            print("End")