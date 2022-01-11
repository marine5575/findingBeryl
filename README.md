## Finding Beryl

### 0. 개발 환경
- Windows 10 64bit
- Anaconda
- Python 3.8.1

### 1. 설치
- **SELENIUM**<br>
`$ pip install selenium`<br><br>
- **CHROMEDRIVER**<br>
<https://sites.google.com/a/chromium.org/chromedriver/><br>
OS에 맞는 가장 최신 stable driver 설치<br><br>

▶ 참고 [here](https://teamlab.github.io/jekyllDecent/blog/crawling%20with%20python/Selenium%EC%9C%BC%EB%A1%9C-%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%97%B0%EA%B7%B9-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0-with-Python)

### 2. 동작 방법
1. Main file 있는 곳으로 가기
2. 아래처럼 실행<br>
`python main.py --dir_path=DIR_PATH --driver_path=DRIVER_DIR_PATH --level=MAX_LEVEL --start=START_PAGE_NUMBER --end=END_PAGE_NUMBER`<br>
'--dir_path'랑 '--driver_path'의 기본값은 => './'<br>
'--start'랑 '--end'의 기본값은 각각 '1', '0'<br>
'--level' 입력은 필수<br>
e.g., `python main.py --level=35`
3. 결과 파일은 home에 만들어짐<br>
e.g., ~/findingBeryl/베릴후보리스트_STARTNUM_ENDNUM.csv

### 3. 코드 설명
#### 목적
EUW 서버에서 사라진 BeryL의 슈퍼계정 찾기...^^ㅠ
To find unknown Beryl's super account candidates in League of Legends EUW server.

#### **베릴을 찾아라**
##### 조건
1. 내가 생각하는 가능한 최대 레벨 이하일 것
2. F점멸
3. 와드 같은 서폿템 살 때는 항상 1번 자리
4. 제어 와드 살 때는 항상 3번 자리

##### Main Logic
Selenium이 페이지 번호 세팅해서 OP.GG EUW 서버 주소를 검색창에 세팅함. 아까 말한 베릴 특징에 모두 부합하는 소환사를 발견하면 최근 3개의 게임의 템트리를 불러와서 저장함. 
이 작업을 START_PAGE부터 ENDPAGE까지 반복함. 전체 과정이 끝나면 '베릴후보리스트_{START_PAGE}_{END_PAGE}.csv' 양식으로 저장함.

##### 보완할 점
사실 많은 정보를 모으는게 아니다보니 저장한 후에 일일이 육안으로 확인하는 작업이 필수로 요구된다. 그리고 최근 3게임만 봐서 그런지 정확도가 상당히 떨어지는 것 같다. (아직 BeryL 못 찾았다는 뜻^^ㅠ) 나중에 또 담원기아가 국제대회 나가면 그때 ML 같은거 적용해서 보강해봐야겠다...

#### **CHECK_FILES**
##### Main Logic
csv 파일이 있는지 확인. 없으면 빈 csv 파일 만들어주고 이름을 아까 정한대로 지어줌.
