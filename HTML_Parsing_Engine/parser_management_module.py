import requests
from bs4 import BeautifulSoup
from breadability.readable import Article
import logging
import time
import json
import random
import re

class ParserManagementModule:
    def __init__(self):
        pass
        #self.session = requests.Session()

    def fetch_text(self, url, query, pf_setting, date):
        try:
            time.sleep(random.randint(1, 3))
            response = requests.get(
                url,
                timeout=5
            )
            html = response.text
            html_as_text = Article(html).readable
            document = Article(html_as_text)
            sentences = [text for paragraph in document.main_text for text, _ in paragraph]

            result_print = "query={0:<20}|PF setting={1:<20}|url ={2:<40}|HTTP requests".format(
                str(query),
                str(pf_setting),
                str(url)
            )
            #print(result_print)
            logging.info(result_print)

            return ' '.join(sentences)
        except Exception as ex:
            logging.error(f"Error fetching text from {url}: {ex}")
            return 'Detail Content Not Found'
    
    def parse_search_results(self, response_dict, parser_types, query, pf_setting, date, os):
        # Try parsing with computer version first
        if os == 'pc':
            results = self.attempt_parse(response_dict, parser_types['pc'], query, pf_setting, date)
        elif os == 'mobile':
            results = self.attempt_parse(response_dict, parser_types['mobile'], query, pf_setting, date)
        return results

    def attempt_parse(self, response_dict, parser_type, query, pf_setting, date):
        soup = BeautifulSoup(response_dict['body'], 'html.parser')
        class_pattern = re.compile(parser_type['results_class'])
        results_list = soup.find_all(parser_type['results_tag'], class_=class_pattern)
        if not results_list:
            logging.info(f"{pf_setting} No results found for {parser_type['name']} : {soup}")
            return [], [], [], []
        return self.extract_search_data(results_list, parser_type, query, pf_setting, date)

    def extract_search_data(self, results_list, parser_type, query, pf_setting, date):
        titles, contents, detail_contents, urls = [], [], [], []

        for result in results_list:
            try:
                # Title extraction
                if 'title_selector' in parser_type:  # If title_selector is defined, use CSS selector
                    title_elements = result.select(parser_type['title_selector'])
                    title = title_elements[0].text.strip() if title_elements else 'Title Not Found'
                elif 'title_tag' in parser_type:  # Otherwise, use tag and class
                    class_pattern = re.compile(parser_type['title_class'])
                    div_element = result.find(parser_type['title_tag'], class_=class_pattern)
                    title = div_element.text.strip() if div_element else 'Title Not Found'

                # Content extraction
                class_pattern = re.compile(parser_type['content_class'])
                div_element = result.find(parser_type['content_tag'], class_=class_pattern)
                content = div_element.text.strip() if div_element else 'Content Not Found'

                if title == 'Title Not Found' and content == 'Content Not Found':
                    continue

                # URL extraction
                #url_elements = result.find(parser_type['url_tag'], class_=parser_type['url_class'])
                #url_elements = result.select(parser_type['url_selector'])
                # URL extraction
                if 'url_selector' in parser_type:  # If url_selector is defined, use CSS selector
                    url_elements = result.select(parser_type['url_selector'])
                    url = url_elements[0].get('href') if url_elements else 'URL Not Found'
                else:  # Otherwise, use tag and class
                    class_pattern = re.compile(parser_type['url_class'])
                    url_element = result.find(parser_type['url_tag'], class_=class_pattern)
                    url = url_element.get('href') if url_element else 'URL Not Found'

                # Fetch detail content if URL is found
                if url != 'URL Not Found':
                    detail_content = self.fetch_text(url, query, pf_setting, date)
                else:
                    url = 'URL Not Found'
                    detail_content = 'Detail Content Not Found'
            except Exception as ex:
                logging.info(f"Error parsing result: {ex}")
                continue

            titles.append(title)
            contents.append(content)
            detail_contents.append(detail_content)
            urls.append(url)

        return titles, contents, detail_contents, urls
    
    def google_search_parser(self, response, query, pf_setting, date, os):
        parser_type = {
            'pc': {
                'name': 'Google Search',
                'results_tag': 'div', 
                'results_class': 'MjjYud',  # Update this with the correct class for Google search results
                'title_tag': 'h3',
                'title_class': 'LC20lb MBeuO DKV0Md',
                'content_tag': 'div',
                'content_class': 'VwiC3b yXK7lf lyLwlc yDYNvb W8l4ac lEBKkf',
                'url_selector': 'div.kb0PBd.cvP2Ce.jGGQ5e > div > div > span > a',
            },
            'mobile': {
                'name': 'Google Search',
                'results_tag': 'div', 
                'results_class': 'MjjYud',
                'title_tag': 'div',
                'title_class': 'v7jaNc ynAwRc MBeuO q8U8x oewGkc LeUQr',
                'content_tag': 'div',
                'content_class': 'VwiC3b yDYNvb W8l4ac',
                'url_tag' : 'a',
                'url_class' : 'cz3goc BmP5tf',
            }
        }
        return self.parse_search_results(response, parser_type, query, pf_setting, date, os)

    def google_news_parser(self, response, query, pf_setting, date, os):
        parser_type = {
            'pc': {
                'name': 'Google News',
                'results_tag': 'div', 
                'results_class': 'SoaBEf',  # Update this with the correct class for Google News results
                'title_tag': 'div',
                'title_class': 'n0jPhd ynAwRc MBeuO nDgy9d',
                'content_tag': 'div',
                'content_class': 'GI74Re nDgy9d',
                'url_tag' : 'a',
                'url_class' : 'WlydOe',
                #'url_selector': 'div > div > a' WlydOe
            },
            'mobile': {
                'name': 'Google News',
                'results_tag': 'div', 
                'results_class': 'Ww4FFb vt6azd',  # Update this with the correct class for Google News results
                'title_tag': 'div',
                'title_class': 'n0jPhd ynAwRc',
                'content_tag': 'div',
                'content_class': 'GI74Re nDgy9d',
                'url_tag' : 'a',
                'url_class' : 'WlydOe',
                #'url_selector': 'div > div > a'
            }
        }
        return self.parse_search_results(response, parser_type, query, pf_setting, date, os)

    def bing_search_parser(self, response, query, pf_setting, date, os):
        parser_type = {
            'pc': {
                'name': 'Bing Search',
                'results_tag': 'li',  #
                'results_class': 'b_algo',  #
                'title_selector': 'h2 > a', #
                'content_tag': 'div', #
                'content_class': 'b_caption', #
                'url_selector': 'h2 > a' ###
            },
            'mobile': {
                'name': 'Bing Search',
                'results_tag': 'li', #
                'results_class': 'b_algo', # 
                'title_tag': 'div', #
                'title_class': 'b_algoheader', #
                'content_tag': 'div', #
                'content_class': 'b_caption', #
                'url_selector': 'div.b_algoheader > a' ###
            }
        }
        return self.parse_search_results(response, parser_type, query, pf_setting, date, os)

    def bing_news_parser(self, response):
        parser_type = {
            'name': 'Bing News',
            'results_class': 'news-card newsitem cardcommon',  # Update this with the correct class for Bing News results
            'title_tag': 'a',
            'title_class': 'title',
            'content_tag': 'div',
            'content_class': 'snippet',
            'url_selector': 'div > a'
        }
        return self.parse_search_results(response, parser_type, query, pf_setting, date)

    # ... [any additional parsers] ...
