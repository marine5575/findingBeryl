## Finding Beryl

### 0. DEVELOPMENT ENVIRONMENT
- Windows 10 64bit
- Anaconda
- Python 3.8.1

### 1. INSTALLATION
- **SELENIUM**<br>
`$ pip install selenium`<br><br>
- **CHROMEDRIVER**<br>
<https://sites.google.com/a/chromium.org/chromedriver/><br>
Install the latest stable version regarding to your OS.<br><br>

▶ Highly inspired by → [here](https://teamlab.github.io/jekyllDecent/blog/crawling%20with%20python/Selenium%EC%9C%BC%EB%A1%9C-%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%97%B0%EA%B7%B9-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0-with-Python)

### 2. HOW TO RUN
1. Go to directory where main file exists
2. Execute like below<br>
`python main.py --dir_path=DIR_PATH --driver_path=DRIVER_DIR_PATH --level=MAX_LEVEL --start=START_PAGE_NUMBER --end=END_PAGE_NUMBER`<br>
Default value of arguments '--dir_path' and '--driver_path' is './'<br>
Default values of arguments '--start' and '--end' are '1' and '0', respectively.<br>
Argument '--level' is always required.<br>
e.g., `python main.py --level=35`
3. Output file is stored at home directory.<br>
e.g., ~/findingBeryl/베릴후보리스트_STARTNUM_ENDNUM.csv

### 3. CODE DESCRIPTION
##### PURPOSE
To find unknown Beryl's super account candidates in League of Legends EUW server.

#### **FINDING CANDIDATES**
##### CONDITION
1. Under max level
2. Flash button should be placed at 'F' position.
3. If a summoner has bought a Supporting item(Ward), it should be placed at '1' position.
4. If a summoner has bought a Control ward, it should be placed at '3' position.

##### MAIN LOGIC
Python Selenium automatically put given page number into OP.GG EUW server search engine. If a summoner have met conditions above, this program automatically fetch the summoner's current three item trees and saves the result. This process would be repeated from START_PAGE to END_PAGE. When the whole process is over, the total results will be recorded on a '베릴후보리스트_{START_PAGE}_{END_PAGE}.csv' file.

##### LIMITATION
Since it is merely collecting information, it is necessary to directly compare and filter whether it is Beryl or not. In addition, the accuracy is pretty low because informations I gathered is from only the last three matches. I'm planning to collect more information and conduct research through machine learning afterwards.

#### **CHECK_FILES**
##### MAIN LOGIC
Check wheter csv file or image directory exists or not. If csv file does not exists, create an empty csv file named with given file name. If image directory does not exists, make target directory including parent directory using os library.
