# 카카오톡 데이터 텍스트에 대해 띄어쓰기를 해줍니다.
# 이는 후에 문장을 단어로 분리할 때 정확성을 높이기 위함입니다.

import torch
import re
import os
import pandas as pd
import numpy as np
from chatspace import ChatSpace

# chatspace 사용
!git clone https://github.com/pingpong-ai/chatspace

os.chdir('chatspace')
!python3 setup.py install

spacer = ChatSpace()
# 띄어쓰기 함수

def spacing(string):
  new_string = spacer.space(string)
  return new_string

# test
test_str = "지금갑니당!!"
test_str = spacing(test_str)
print(test_str)

os.chdir('path') # 'path' 부분에 채팅 데이터 폴더 경로를 입력해주세요.

df_check = pd.read_csv("1.csv") # 데이터 확인
df_check.head()

data_num = 20 # 데이터 개수를 변경해주세요.

for i in range(1,data_num):
  number = str(i)
  df = pd.read_csv(number + ".csv") # 데이터에 맞게 이름 설정을 해주세요.

  for i in df.index:
    string = df.loc[i,'col']) # 'col' 부분에 텍스트가 담긴 열의 이름을 적어주세요.
    new_string = spacing(new_string)
    df.loc[i, 'text'] = new_string

  df.to_csv("output_" + number + ".csv")
  
  print("dataset", number, "completed")
