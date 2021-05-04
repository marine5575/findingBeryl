import os
import pandas as pd

def get(dir_path, f_name):
    file_path = os.path.join(dir_path, f_name)

    # 존재하지 않을 때
    if not os.path.exists(file_path):
        print('##### CREATE NEW FILE #####')
        df = pd.DataFrame(columns=['소환사명', '티어', 'LP', '레벨', '승률',
                                    '아이템1', '아이템2', '아이템3'])
        df.to_csv(f_name, mode='w', encoding='utf-8-sig', index=False)
        
# def img_Dir_Exists(dir_path, input):
#     dir_path = os.path.join(dir_path, 'img')
#     img_path = os.path.join(dir_path, input)
    
#     # 존재하지 않음
#     if not os.path.exists(img_path):
#         print('##### CREATE NEW IMG DIR #####')
#         os.makedirs(img_path)
        
#     return img_path