import os
import argparse
from modules import findCandidates

parser = argparse.ArgumentParser()
parser.add_argument('--dir_path', default='.\\', help='파일을 저장할 위치')
parser.add_argument('--driver_path', default='.\\', help='브라우저 드라이버 위치')
parser.add_argument('--level', required=True, help='최대 레벨')
parser.add_argument('--start', default='1', help='시작페이지')
parser.add_argument('--end', default='0', help='마지막페이지')

args = parser.parse_args()


if __name__ == "__main__":
    print("##### STARTING #####\n")
    
    dir_path = args.dir_path
    maxLevel = int(args.level)
    start = int(args.start)
    end = int(args.end)
    f_name = '베릴 후보 리스트.csv'
    driver_path = os.path.join(args.driver_path, 'chromedriver.exe')
    
    get_list = findCandidates.GetBerylCandidates(driver_path)
    get_list.setting_file(dir_path, f_name)
    # flag = get_list.searching(dir_path, maxLevel) # 정상적으로 끝났다면 0 반환
    totalPage = get_list.getTotalCnt() # 정상적으로 끝났다면 0 반환

    if end == 0: end = totalPage

    flag = get_list.searching(dir_path, start, end, maxLevel) # 정상적으로 끝났다면 0 반환

    get_list.close()
    
    if totalPage < 0: exit(1)
    
    flag = get_list.make_new_file() # 파일 update
    
    # 정상 종료
    if flag == 0: print('\n##### SUCCESS! #####')
    # 비정상 종료 (저장 중 문제 발생)
    else: print('\n##### ERROR OCCURED DURING SAVING FILE #####')