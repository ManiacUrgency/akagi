
## Install python packages 
pip3 install googlenewsdecoder
pip3 install newspaper4k
pip3 install punk_tab
pip3 install langchain_openai
pip3 install langchain
pip3 install newspaper4k requests
pip3 install lxml_html_clean
pip3 install typing_extensions


## Install MySQl Server

1. https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/macos-installation-pkg.html, this is an info page. Go to the next step

2. https://dev.mysql.com/downloads/mysql/

Choose:  macOS 14 (ARM, 64-bit), DMG Archive to download

3. install the dmg package after downloading it on your Macbook Pro

Select a root admin password

4. open a Terminal, and type the following to access the mysql server using your root account, with password you set above
/usr/local/mysql/bin/mysql -u root -p

5. set up the database 

// create a new user account in mysql 
mysql> create user 'lodge'@'localhost' identified by 'rabig!2109';

// create database to store data for the project 
mysql> create database gnews;

// grant the new user access to the database
mysql> GRANT ALL PRIVILEGES ON gnews.* TO 'lodge'@'localhost'; 

// create the table(s) 
mysql> use gnews;
mysql> CREATE TABLE articles (
    id VARCHAR(36) PRIMARY KEY,
    title TEXT,
    author JSON,  -- Using JSON type since authors appears to be a list
    text LONGTEXT,  -- Using LONGTEXT for potentially long article content
    publish_date DATETIME,
    keywords JSON,  -- Using JSON type since keywords appears to be a list
    summary TEXT,
    site VARCHAR(255),
    site_url VARCHAR(2048),  -- Common max length for URLs
    url VARCHAR(2048),
    hashed_url CHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_hashed_url(hashed_url) 
);

// (optional) create a test table
mysql> CREATE TABLE test (
    id VARCHAR(36) PRIMARY KEY, 
    title TEXT,
    number INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Next we need to install a few things to allow us to access mysql in Python script  

6. Install packages on your macbook pro 
brew install pkg-config
brew install mysql

7. Install python package for mysql client
python -m pip install mysqlclient

8. run test_mysql.py to test you can insert a row to the test database

9. set up logging 

// create log directory locally
sudo mkdir /var/log/gnews

// set up ownership -- replace "stephenjin:staff" with your <user>:<user group> 
sudo chown stephenjin:staff /var/log/gnews

10. access Mysql database 

/usr/local/mysql/bin/mysql -ulodge -p
enter password: rabig!2109

mysql> use gnews
mysql> select id, title, url, hashed_url from articles; 
mysql> select id, text,url, hashed_url from articles where url = '<some_url>' \G;


11. Run on Macbook Pro laptop in the background: 

cd .../akagi/GNews/
source .venv/bin/activate
caffeinate -i nohup /Users/stephenjin/Documents/Leonard/akagi/GNews/.venv/bin/python /Users/stephenjin/Documents/Leonard/akagi/GNews/gnews_crawler.py > output.log 2>&1 & 


Part II Use OpenAI's API to detect relevance and location for each news article and add the result to the database.

12. Add a few new columns to store these data 

ALTER TABLE articles
ADD COLUMN is_related BOOLEAN DEFAULT NULL,
ADD COLUMN is_national BOOLEAN DEFAULT NULL,
ADD COLUMN city VARCHAR(255) DEFAULT NULL,
ADD COLUMN state VARCHAR(255) DEFAULT NULL,
ADD COLUMN location JSON DEFAULT NULL;

caffeinate -i nohup /Users/stephenjin/Documents/Leonard/akagi/GNews/.venv/bin/python /Users/stephenjin/Documents/Leonard/akagi/GNews/gnews_location_ingestor.py > output_loc_ingest.log 2>&1 &

Part II Use OpenAI's API to extract and fill in publish_date for rows without it

For some reason, the extraction of the library failed for some articles to extract the publish dates. In some cases, there's no such date, so it's correct. We just do need to include the article in results.  In most of the cases, the extraction failed. So we directly fetch the article's web pages using the requests library, and clean the HTML content, then use OpenAI's API to extract the publish date.  We were able to extract it for more than 90% of the articles. 

Run this script:
/Users/stephenjin/Documents/Leonard/akagi/GNews/.venv/bin/python /Users/stephenjin/Documents/Leonard/akagi/GNews/gnews_publish_date_ingestor.py

13. Export the data to CVS

Run the script: 
/Users/stephenjin/Documents/Leonard/akagi/GNews/.venv/bin/python /Users/stephenjin/Documents/Leonard/akagi/GNews/export_articles_to_csv.py

Then new a Google Sheet and export the two CSV files as new sheets. 


## Notes
We first crawled articles from 2023/11/01 to 2024/10/29. This is about a year's data. The reason we stopped at 10/29 is because that the date before the day we started the crawling. 
Later, we decided to crawl for two more years. 
We started crawling for 2022/11/01 to 2023/10/31 after 2024-12-22 00:00:00. 
We started crawling for 2021/11/01 to 2022/10/31 at 2024-12-26 21:55:00. (However, some of the artiles are crawled before this time.)

We have now roughly about three years of articles by the search query "Opioid Crisis" from Google News. 
