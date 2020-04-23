# 문장을 단어로 분리해줍니다.

import os
os.chdir('/path') # '/path' 부분에 경로를 입력해줍니다.

import pandas as pd

data_num = 20 # 데이터 개수를 변경해주세요.

for i in range(1, data_num):
  number = str(i)
  df = pd.read_csv("output_" + number + ".csv") # 데이터에 맞게 이름 설정을 해주세요.

  string = ""
  for i in df.index:
    string += str(df.loc[i,'col']) # 'col' 부분에 텍스트가 담긴 열의 이름을 적어주세요.
    string += " "

  string = string.split()
  output = pd.DataFrame(string)
  output.to_csv("word_" + number + ".csv") # output_num.csv 형태로 새로운 csv를 만듭니다.

  print("dataset", number, "completed")
