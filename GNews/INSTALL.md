
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

9. access Mysql database 

/usr/local/mysql/bin/mysql -ulodge -p
enter password: rabig!2109

mysql> use gnews
mysql> select id, title, url, hashed_url from articles; 
