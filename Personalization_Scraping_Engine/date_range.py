from datetime import datetime, timedelta
import configparser

# Read configuration from 'config.ini'
config = configparser.ConfigParser()
config.read('config.ini')

class DateRangeSetting():
    def generate_tbs(self, date):
        # Format start and end date strings
        start_date = date.strftime("%m/%d/%Y")
        end_date = date.strftime("%m/%d/%Y")
        return f"cdr:1,cd_min:{start_date},cd_max:{end_date}"

    def generate_ez_item(self, date):
        # Convert date to an integer representation
        date1 = self.date_to_integer(date)
        date2 = self.date_to_integer(date)
        return f"ez5_{date1}_{date2}"

    def date_to_integer(self, date):
        # Calculate the number of days from a fixed start date
        start_of_year = datetime(2022, 1, 1)
        delta = date - start_of_year
        return delta.days + 18993

    def date_range(self, start_date, end_date):
        # Generate a range of dates from start_date to end_date
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += timedelta(days=1)

    def generate_date_range_list(self, pir_system):
        # Parse start and end dates from configuration
        start_date = datetime.strptime(config['DEFAULT']['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(config['DEFAULT']['end_date'], "%Y-%m-%d")
        self.date_range_list = [date for date in self.date_range(start_date, end_date)]

        if pir_system in ['google_search', 'google_news']:
            # Generate date range list with tbs format
            self.convert_date_range_list = [self.generate_tbs(date) for date in self.date_range(start_date, end_date)]
        elif pir_system == 'bing_search':
            # Generate date range list with ez_item format
            self.convert_date_range_list = [self.generate_ez_item(date) for date in self.date_range(start_date, end_date)]
        return self.convert_date_range_list, self.date_range_list

if __name__ == '__main__':
    date_range = DateRangeSetting()
    convert_date_range_list, date_range_list = date_range.generate_date_range_list('google_search')
    print(convert_date_range_list)
    print(date_range_list)
    convert_date_range_list, date_range_list = date_range.generate_date_range_list('google_news')
    print(convert_date_range_list)
    print(date_range_list)
    convert_date_range_list, date_range_list = date_range.generate_date_range_list('bing_search')
    print(convert_date_range_list)
    print(date_range_list)
    convert_date_range_list, date_range_list = date_range.generate_date_range_list('bing_news')
    print(convert_date_range_list)
    print(date_range_list)