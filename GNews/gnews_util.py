import logging
import urllib.request
import datetime
import inspect
import warnings

import feedparser
from bs4 import BeautifulSoup as Soup

import nltk
nltk.download("punk_tab")
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from gnews.utils.constants import AVAILABLE_COUNTRIES, AVAILABLE_LANGUAGES, TOPICS, BASE_URL, USER_AGENT
from gnews.utils.utils import process_url

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


class GNews:
    def __init__(self, language="en", country="US", site=None,max_results=100, period=None, start_date=None, end_date=None, exclude_websites=None, proxy=None):
        """
        (optional parameters)
        :param language: The language in which to return results, defaults to en (optional)
        :param country: The country code of the country you want to get headlines for, defaults to US
        :param max_results: The maximum number of results to return. The default is 100, defaults to 100
        :param period: The period of time from which you want the news
        :param start_date: Date after which results must have been published
        :param end_date: Date before which results must have been published
        :param exclude_websites: A list of strings that indicate websites to exclude from results
        :param proxy: The proxy parameter is a dictionary with a single key-value pair. The key is the
        protocol name and the value is the proxy address
        """
        self.countries = tuple(AVAILABLE_COUNTRIES),
        self.languages = tuple(AVAILABLE_LANGUAGES),
        self.site = site if site and isinstance(site, str) else ""
        self._language = language
        self._country = country
        self._max_results = max_results
        self._period = period
        self._end_date = None
        self._start_date = None
        self.end_date = self.end_date = end_date
        self._start_date = self.start_date = start_date
        self._exclude_websites = exclude_websites if exclude_websites and isinstance(exclude_websites, list) else []
        self._proxy = {'http': proxy, 'https': proxy} if proxy else None
    
    def _time_query(self):
        time_query = ''
        if self._start_date or self._end_date:
            if inspect.stack()[2][3] != 'get_news':
                warnings.warn(message=("Only searches using the function get_news support date ranges. Review the "
                                       f"documentation for {inspect.stack()[2][3]} for a partial workaround. \nStart "
                                       "date and end date will be ignored"), category=UserWarning, stacklevel=4)
                if self._period:
                    time_query += "when%3A".format(self._period)
            if self._period:
                warnings.warn(message=f'\nPeriod ({self.period}) will be ignored in favour of the start and end dates',
                              category=UserWarning, stacklevel=4)
            if self.end_date is not None:
                time_query += "%20before%3A{}".format(self.end_date)
            if self.start_date is not None:
                time_query += "%20after%3A{}".format(self.start_date)
        elif self._period:
            time_query += "%20when%3A{}".format(self._period)

        return time_query 
 
    def _ceid(self):
        return "&hl={}&gl={}&ceid={}:{}".format(self._language,
                                                             self._country,
                                                             self._country,
                                                             self._language,)

    def _site_query(self):
        if self.site:
            return "%20" + "site:" + self.site + "%20"
        else:
            return ""

    def _query(self):
        return self._site_query() + self._time_query() + self._ceid()

    #Need to improve or delete query expansion
    def query_expansion(self, query):
        OPENAI_API_QUERY_KEY = os.environ["OC_QUERY_KEY"]
        query_llm = ChatOpenAI(
            openai_api_key=OPENAI_API_QUERY_KEY,
            model_name="gpt-4o",
            temperature=0.0,
            streaming=True
        )

        request = PromptTemplate(
            template=
            """
            Give me a list of 5 keywords that are related to the query: {query}.

            Your output should be a list of words separated by spaces. Here is an example:

            User Query: Opioid Crisis

            Output:

            Narcotic Opiate Painkiller Fentanyl
            
            """,
            input_variables=["query"]
        ).format(query=self._query())

        response = query_llm.invoke(request)

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        """
        :param language: The language code for the language you want to use
        """
        self._language = AVAILABLE_LANGUAGES.get(language, language)

    @property
    def exclude_websites(self):
        return self._exclude_websites

    @exclude_websites.setter
    def exclude_websites(self, exclude_websites):
        """
        The function takes in a list of websites that you want to exclude
        :param exclude_websites: A list of strings that will be used to filter out websites
        """
        self._exclude_websites = exclude_websites

    @property
    def max_results(self):
        return self._max_results

    @max_results.setter
    def max_results(self, size):
        self._max_results = size

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period):
        self._period = period

    @property
    def start_date(self):
        """
        :return: string of start_date in form YYYY-MM-DD, or None if start_date is not set
        …NOTE this will reset period to None if start_date is not none
        """
        if self._start_date is None:
            return None
        self.period = None
        return self._start_date.strftime("%Y-%m-%d")

    @start_date.setter
    def start_date(self, start_date):
        """
        The function sets the start of the date range you want to search
        :param start_date: either a tuple in the form (YYYY, MM, DD) or a datetime
        """
        if type(start_date) is tuple:
            start_date = datetime.datetime(start_date[0], start_date[1], start_date[2])
        if self._end_date:
            if start_date - self._end_date == datetime.timedelta(days=0):
                warnings.warn("The start and end dates should be at least 1 day apart, or GNews will return no results")
            elif self._end_date < start_date:
                warnings.warn("End date should be after start date, or GNews will return no results")
        self._start_date = start_date

    @property
    def end_date(self):
        """
        :return: string of end_date in form YYYY-MM-DD, or None if end_date is not set
        …NOTE this will reset period to None if end date is not None
        """
        if self._end_date is None:
            return None
        self.period = None
        return self._end_date.strftime("%Y-%m-%d")

    @end_date.setter
    def end_date(self, end_date):
        """
        The function sets the end of the date range you want to search
        :param end_date: either a tuple in the form (YYYY, MM, DD) or a datetime
        …NOTE this will reset period to None
        """
        if type(end_date) is tuple:
            end_date = datetime.datetime(end_date[0], end_date[1], end_date[2])
        if self._start_date:
            if end_date - self._start_date == datetime.timedelta(days=0):
                warnings.warn("The start and end dates should be at least 1 day apart, or GNews will return no results")
            elif end_date < self._start_date:
                warnings.warn("End date should be after start date, or GNews will return no results")
        self._end_date = end_date

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = AVAILABLE_COUNTRIES.get(country, country)

    def get_full_article(self, url):
        """
        Download an article from the specified URL, parse it, and return an article object.
        :param url: The URL of the article you wish to summarize.
        :return: An `Article` object returned by the `newspaper4k` library if installed; otherwise, None.
        """
        try:
            import newspaper
            import requests
        except ImportError:
            print("\nget_full_article() requires the `newspaper4k` and `requests` libraries.")
            print("You can install them by running `pip3 install newspaper4k requests`, `pip3 install lxml_html_clean`, and `pip3 install typing_extensions` in your shell.")
            return None

        try:
            # Resolve the redirect URL to get the actual article URL
            # response = requests.get(url, allow_redirects=True, timeout=10)
            # final_url = response.url
            # print(f"Resolved URL: {final_url}")
            # print("URL: ", url)
            # Use the resolved URL to download the article
            article = newspaper.article(url=url)
            article.download()
            article.parse()
            article.nlp()
        except Exception as error:
            print(f"An error occurred while fetching the article: {error}")
            return None
        
        return article


    @staticmethod
    def _clean(html):
        soup = Soup(html, features="html.parser")
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def _process(self, item):
        # Initialize URL as empty
        url = ''
        
        # Try to extract URL from 'link' field
        if 'link' in item:
            url = item['link']
        
        # If the 'link' is a Google redirect URL, extract the actual URL from 'summary' field
        if 'news.google.com/rss/articles' in url or not url:
            summary = item.get('summary', '')
            soup = Soup(summary, 'html.parser')
            # Find the first hyperlink
            a_tag = soup.find('a', href=True)
            if a_tag:
                url = a_tag['href']
            else:
                url = ''
        
        # Exclude websites if necessary
        if url and self._exclude_websites:
            for site in self._exclude_websites:
                if site in url:
                    return None
        
        if url:
            title = item.get("title", "")
            # print("\nPublish Date: ", item.get("published", ""))
            # print("Publish Date Type: ", type(item.get("published","")))
            item = {
                'title': title,
                'description': self._clean(item.get("summary", "")),
                'published date': item.get("published", ""),
                'url': url,
                'publisher': item.get("source", {}).get("title", "")
            }
            return item
        else:
            return None

    def docstring_parameter(*sub):
        def dec(obj):
            obj.__doc__ = obj.__doc__.format(*sub)
            return obj

        return dec

    indent = '\n\t\t\t'
    indent2 = indent + '\t'
    standard_output = (indent + "{'title': Article Title," + indent + "'description': Google News summary of the "
                       "article," + indent + "'url': link to the news article," + indent + "'publisher':" + indent2 +
                       "{'href': link to publisher's website," + indent2 + "'title': name of the publisher}}")

    @docstring_parameter(standard_output)
    def get_news(self, key):
        """
        The function takes in a key and returns a list of news articles
        :param key: The query you want to search for. For example, if you want to search for news about
        the "Yahoo", you would get results from Google News according to your key i.e "yahoo"
        :return: A list of dictionaries with structure: {0}.
        """
        if key:
            key = "%20".join(key.split(" "))
            query = '/search?q={}'.format(key)
            return self._get_news(query)

    @docstring_parameter(standard_output)
    def get_top_news(self):
        """
        This function returns top news stories for the current time
        :return: A list of dictionaries with structure: {0}.
        ..To implement date range try get_news('?')
        """
        query = "?"
        return self._get_news(query)

    @docstring_parameter(standard_output)
    def get_news_by_location(self, location: str):
        """
        This function is used to get news from a specific location (city, state, and country)
        :param location: (type: str) The location for which you want to get headlines
        :return: A list of dictionaries with structure: {0}.
        ..To implement date range try get_news('location')
        """
        if location:
            query = '/headlines/section/geo/' + location + '?'
            return self._get_news(query)
        logger.warning("Enter a valid location.")
        return []

    def _get_news(self, query):
        # query = self.query_expansion(query)
        url = BASE_URL + query + self._query()
        print("\nFinal URL: ", url)
        try:
            if self._proxy:
                proxy_handler = urllib.request.ProxyHandler(self._proxy)
                feed_data = feedparser.parse(url, agent=USER_AGENT, handlers=[proxy_handler])
            else:
                feed_data = feedparser.parse(url, agent=USER_AGENT)

            return [item for item in
                    map(self._process, feed_data.entries[:self._max_results]) if item]
        except Exception as err:
            logger.error(err.args[0])
            return []