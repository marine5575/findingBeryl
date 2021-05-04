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

class UpToDateError(Exception):
    pass

class ResultNotFoundError(Exception):
    pass

class GetBerylCandidates:
    OPGG_SEARCH_TEMPLATE = 'https://euw.op.gg/ranking/ladder/page={}'
    SUMMONER_SEARCH_TEMPLATE = 'https://euw.op.gg/summoner/userName={}'
    summoner_list = []
    tier_list = []
    LP_list = []
    level_list = []
    winRate_list = []
    item1_list = []
    item2_list = []
    item3_list = []
    
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
        self.driver.get(self.OPGG_SEARCH_TEMPLATE.format(1))

        try:
            print('\n##### WAITING WEB PAGE LOADS #####')
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'PageDescription'))
            )

            total = self.driver.find_element_by_xpath("//div[@class='PageDescription']/span[@class='Text']").text
            total = total.split('총 ')[1].split('명의')[0].split(',')
            totalCnt = ''

            for i in total:
                totalCnt += i

            # return math.ceil(int(totalCnt) / 100)

        except TimeoutException:
            print('\n※※※ TIMEOUT EXCEPTION OCCURRED ※※※')
            return -1
        except Exception:
            print('\n※※※ SOMETHING WENT WRONG!!! ※※※')
            return -4

        return math.ceil(int(totalCnt) / 100)

    def searching(self, dir_path, startPage, endPage, maxLevel):
        # INPUT을 검색해서 나온 결과를 list up
        # user_input = quote_plus(input)
        for page in range(startPage, endPage + 1):
            self.driver.get(self.OPGG_SEARCH_TEMPLATE.format(page))

            try:
                print('\n##### WAITING RANK PAGE LOADS #####')
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'ranking-table'))
                )

                print(page, 'page')
                
                # 검색결과 문구 따옴
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
                
                for idx, k in enumerate(levels):
                    if int(k.text) > maxLevel: continue
                    if self.spellCheck(summoners[idx].text) != 0: continue
                    
                    summoner_list.append(summoners[idx].text)
                    tier_list.append(tiers[idx].text)
                    LP_list.append(LPs[idx].text)
                    level_list.append(int(levels[idx].text))
                    winRate_list.append(winRates[idx].text)

                self.summoner_list = self.summoner_list + 3 * summoner_list
                self.tier_list = self.tier_list + 3 * tier_list
                self.LP_list = self.LP_list + 3 * LP_list
                self.level_list = self.level_list + 3 * level_list
                self.winRate_list = self.winRate_list + 3 * winRate_list

            except TimeoutException:
                print('\n※※※ TIMEOUT EXCEPTION OCCURRED ※※※')
                return -1
            except ResultNotFoundError:
                print('\n※※※ RESULT NOT FOUND ※※※')
                os.remove(self.file_path)   # 검색결과가 없으므로 만들었던 파일 필요 없음
                return -3
            except Exception:
                print('\n※※※ SOMETHING WENT WRONG!!! ※※※')
                return -4
        
        print('\n###### INFORMATIONS ######')
        print(list(dict.fromkeys(self.summoner_list)))
        # print(self.tier_list)
        # print(self.LP_list)
        # print(self.level_list)
        # print(self.winRate_list)

        return 0    # 정상 종료

    def spellCheck(self, input):
        self.driver.execute_script('window.open();')
        self.driver.switch_to_window(self.driver.window_handles[-1])
        self.driver.get(self.SUMMONER_SEARCH_TEMPLATE.format(input))

        try:
            print('\n##### WAITING SUMMONER PAGE LOADS #####')
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'SummonerSpell'))
            )

            spell_F = self.driver.find_elements_by_xpath("//div[@class='SummonerSpell']/div[2]/img")
            item1 = self.driver.find_elements_by_xpath("//div[@class='ItemList']/div[1]/img")
            item2 = self.driver.find_elements_by_xpath("//div[@class='ItemList']/div[2]/img")
            item3 = self.driver.find_elements_by_xpath("//div[@class='ItemList']/div[3]/img")

            item1_list = []
            item2_list = []
            item3_list = []

            flag = 0

            for i in range(3):
                if spell_F[i].get_attribute("alt") != "점멸":
                    flag = -1
                    break

                item1_explanation = ''
                item2_explanation = ''
                item3_explanation = ''
                ward = "너무 많은 미니언을 처치하면 미니언 처치 시 획득하는 골드가 감소합니다."

                if "active" in item1[i].get_attribute("title"):
                    item1_explanation = item1[i].get_attribute("title")
                if "active" in item2[i].get_attribute("title"):
                    item2_explanation = item2[i].get_attribute("title")
                if "active" in item3[i].get_attribute("title"):
                    item3_explanation = item3[i].get_attribute("title")

                if item1_explanation != '' and item1[i].get_attribute("alt") == "제어 와드":
                    flag = -1
                    break
                if item2_explanation != '' and ((ward in item2_explanation) or (item2[i].get_attribute("alt") == "제어 와드")):
                    flag = -1
                    break
                if item3_explanation != '' and ward in item3_explanation:
                    flag = -1
                    break

                item1_list.append(item1[i].get_attribute("alt"))
                item2_list.append(item2[i].get_attribute("alt"))
                item3_list.append(item3[i].get_attribute("alt"))

            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])

            if flag == 0:
                self.item1_list = self.item1_list + item1_list
                self.item2_list = self.item2_list + item2_list
                self.item3_list = self.item3_list + item3_list

            return flag

        except Exception:
            print('\n※※※ SOMETHING WENT WRONG!!! ※※※')
            return -4

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