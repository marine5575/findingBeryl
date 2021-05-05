from selenium import webdriver
from urllib.parse import quote_plus
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import os
import pandas as pd
import math

from . import check_files

class GetBerylCandidates:
    OPGG_SEARCH_TEMPLATE = 'https://euw.op.gg/ranking/ladder/page={}'       # op.gg EUW 서버 랭킹 검색할 템플릿
    SUMMONER_SEARCH_TEMPLATE = 'https://euw.op.gg/summoner/userName={}'     # EUW 서버 소환사 검색할 템플릿
    summoner_list = []  # 베릴 후보 소환사들
    tier_list = []      # 베릴 후보 티어들
    LP_list = []        # 베릴 후보 LP들
    level_list = []     # 베릴 후보 레벨들
    winRate_list = []   # 베릴 후보 승률들
    item1_list = []     # 베릴 후보 아이템창 1번
    item2_list = []     # 베릴 후보 아이템창 2번
    item3_list = []     # 베릴 후보 아이템창 3번
    
    def __init__(self, driver_path):
        # chrome driver 열기
        options = webdriver.ChromeOptions()
        options.add_argument('headless')    # 창을 띄우지 않고 실행
        options.add_argument('disable-gpu') # gpu 사용 x
        options.add_argument('lang=ko_KR')  # 언어 설정
        options.add_argument('--incognito') # 시크릿모드

        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
    

    def setting_file(self, dir_path, f_name):
        # 파일이 존재한다면 파일을 열고, 존재하지 않는다면 만듬        
        print('\n##### CHECKING FILE EXISTS #####')
        check_files.get(dir_path, f_name)
        self.file_path = os.path.join(dir_path, f_name)
        
        print('##### READING FILE #####')
        self.df = pd.read_csv(self.file_path)


    def getTotalCnt(self):
        self.driver.get(self.OPGG_SEARCH_TEMPLATE.format(1))    # 일단 첫번째 페이지 접속

        try:
            print('\n##### WAITING FOR WEB PAGE TO LOAD #####')
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'PageDescription'))
            )

            # 리더보드에 있는 소환사 총 수
            total = self.driver.find_element_by_xpath("//div[@class='PageDescription']/span[@class='Text']").text
            total = total.split('총 ')[1].split('명의')[0].split(',')   # 숫자만 뽑기 (배열)
            totalCnt = ''

            # 배열을 문자로 합치기
            for i in total:
                totalCnt += i

        except TimeoutException:
            print('\n※※※ TIMEOUT EXCEPTION OCCURRED ※※※')
            return -1
        except Exception:
            print('\n※※※ SOMETHING WENT WRONG!!! ※※※')
            return -2

        return math.ceil(int(totalCnt) / 100)   # 1페이지에 100명이 있음


    def searching(self, dir_path, startPage, endPage, maxLevel):
        # startPage부터 endPage까지 베릴 같은 사람을 찾음
        # << 조건 >>
        # 1. maxLevel 이하일 것
        # 2. F 점멸일 것
        # 3. 서폿템(와드)가 있다면 1번에 위치시켜놓을 것
        # 4. 제어와드가 있다면 3번에 위치시켜놓을 것
        for page in range(startPage, endPage + 1):
            self.driver.get(self.OPGG_SEARCH_TEMPLATE.format(page)) # 페이지로 이동

            try:
                print('\n##### WAITING FOR RANK PAGE TO LOAD #####')
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ranking-table'))
                )

                print('***** ', page, 'page *****')
                
                # 페이지에 있는 소환사들 정보 가져옴
                summoner_list = []
                tier_list = []
                LP_list = []
                level_list = []
                winRate_list = []

                summoners = self.driver.find_elements_by_xpath("//td[@class='ranking-table__cell ranking-table__cell--summoner']//span")
                tiers = self.driver.find_elements_by_xpath("//td[@class='ranking-table__cell ranking-table__cell--tier']")
                LPs = self.driver.find_elements_by_xpath("//td[@class='ranking-table__cell ranking-table__cell--lp']")
                levels = self.driver.find_elements_by_xpath("//td[@class='ranking-table__cell ranking-table__cell--level']")
                winRates = self.driver.find_elements_by_xpath("//td[@class='ranking-table__cell ranking-table__cell--winratio']//span")
                
                # 1. maxLevel 이하일 것
                for idx, k in enumerate(levels):
                    # maxLevel 이상알 때 통과
                    if int(k.text) > maxLevel: continue
                    # 스펠과 아이템 체크 결과 아니면 통과
                    if self.spellAndItemCheck(summoners[idx].text) != 0: continue
                    
                    summoner_list.append(summoners[idx].text)
                    tier_list.append(tiers[idx].text)
                    LP_list.append(LPs[idx].text)
                    level_list.append(int(levels[idx].text))
                    winRate_list.append(winRates[idx].text)

                # 최근 3경기 기준으로 아이템을 가져오므로 DataFrame에 담기 위해서는 각각 이름이 3번씩 들어가야됨
                self.summoner_list = self.summoner_list + 3 * summoner_list
                self.tier_list = self.tier_list + 3 * tier_list
                self.LP_list = self.LP_list + 3 * LP_list
                self.level_list = self.level_list + 3 * level_list
                self.winRate_list = self.winRate_list + 3 * winRate_list

            except TimeoutException:
                print('\n※※※ TIMEOUT EXCEPTION OCCURRED ※※※')
                return -1
            except Exception:
                print('\n※※※ SOMETHING WENT WRONG!!! ※※※')
                return -2
            
        print('\n###### INFORMATIONS ######')
        print(list(dict.fromkeys(self.summoner_list)))  # 중복 제거한 베릴 후보 소환사 이름들

        return 0    # 정상 종료


    def spellAndItemCheck(self, input):
        # 같은 페이지에서 페이지 이동을 하게 되면 이 함수 불리기 전에 연결해놨던 elements 연결이 끊김
        # (상대적 경로에 의한 dynamic web element라고 보면 쉬울 듯)
        # 그래서 새로운 탭을 열고 이동함
        self.driver.execute_script('window.open();')
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.get(self.SUMMONER_SEARCH_TEMPLATE.format(input))

        try:
            print('\n##### WAITING FOR SUMMONER PAGE TO LOAD #####')
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'SummonerSpell'))
            )

            spell_D = self.driver.find_elements_by_xpath("//div[@class='SummonerSpell']/div[1]/img")
            spell_F = self.driver.find_elements_by_xpath("//div[@class='SummonerSpell']/div[2]/img")
            item1 = self.driver.find_elements_by_xpath("//div[@class='ItemList']/div[1]/img")
            item2 = self.driver.find_elements_by_xpath("//div[@class='ItemList']/div[2]/img")
            item3 = self.driver.find_elements_by_xpath("//div[@class='ItemList']/div[3]/img")

            item1_list = []
            item2_list = []
            item3_list = []

            flag = 0    # 0: 베릴일지도? / 1: 베릴 아님

            # 최근 3경기만 참고함 -> rough한 경향성만 보기 위함
            for i in range(3):
                D = spell_D[i].get_attribute("alt")
                F = spell_F[i].get_attribute("alt")

                # 점멸 썼는데 F 점멸이 아닌가?
                if (D == "점멸" or F == "점멸") and F != "점멸":
                    flag = -1
                    break

                item1_explanation = ''
                item2_explanation = ''
                item3_explanation = ''
                ward = "너무 많은 미니언을 처치하면 미니언 처치 시 획득하는 골드가 감소합니다." # 서폿템 설명

                # 액티브 아이템일 때
                if "active" in item1[i].get_attribute("title"):
                    item1_explanation = item1[i].get_attribute("title")
                if "active" in item2[i].get_attribute("title"):
                    item2_explanation = item2[i].get_attribute("title")
                if "active" in item3[i].get_attribute("title"):
                    item3_explanation = item3[i].get_attribute("title")

                # 1번 템에 액티브 아이템이 왔는데 그게 제어와드다?
                if item1_explanation != '' and item1[i].get_attribute("alt") == "제어 와드":
                    flag = -1
                    break
                # 2번 템에 액티브 아이템이 왔는데 그게 제어와드 혹은 서폿템이다?
                if item2_explanation != '' and ((ward in item2_explanation) or (item2[i].get_attribute("alt") == "제어 와드")):
                    flag = -1
                    break
                # 3번 템에 액티브 아이템이 왔는데 그게 서폿템이다?
                if item3_explanation != '' and ward in item3_explanation:
                    flag = -1
                    break

                item1_list.append(item1[i].get_attribute("alt"))
                item2_list.append(item2[i].get_attribute("alt"))
                item3_list.append(item3[i].get_attribute("alt"))

            self.driver.close() # 탭 닫기
            self.driver.switch_to_window(self.driver.window_handles[0]) # 바라보는 탭 옮기기

            # 베릴 후보일 때
            if flag == 0:
                self.item1_list = self.item1_list + item1_list
                self.item2_list = self.item2_list + item2_list
                self.item3_list = self.item3_list + item3_list

            return flag

        except Exception:
            print('\n※※※ SOMETHING WENT WRONG!!! ※※※')
            return -2


    def close(self):
        # chrome driver 종료
        self.driver.close()
    

    def make_new_file(self):
        # csv 파일 update
        print('\n##### UPDATING #####')
        
        df = pd.DataFrame({
            '소환사명':self.summoner_list,
            '티어':self.tier_list,
            'LP':self.LP_list,
            '레벨':self.level_list,
            '승률':self.winRate_list,
            '아이템1':self.item1_list,
            '아이템2':self.item2_list,
            '아이템3':self.item3_list
        })

        df.to_csv(self.file_path, encoding='utf-8-sig', index=False)

        # 저장 실패
        if not os.path.exists(self.file_path):
            return -1
        # 저장 성공
        else: return 0