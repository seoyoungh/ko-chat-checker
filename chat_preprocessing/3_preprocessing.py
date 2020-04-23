# 특수문자, 이모지, 영어, 단일 자음(e.g. ㅋㅋ), 단일 모음(e.g. ㅠㅠ)을 제거합니다.
# 출처: https://jokergt.tistory.com/52

import re
import pandas as pd
import numpy as np

def remove_except_ko(word):
  w = word
  hangul = re.compile('[^ 가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자

  # ㅋㅋ, ㅎㅎ와 같은 텍스트도 분석을 원하시면 아래 코드로 대체해주세요.
  # hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글(단일 자모포함))과 띄어쓰기를 제외한 모든 글자

  result = hangul.sub('', w) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
  # removed = hangul.findall(s) # 체크용 - 정규식에 일치되는 부분을 리스트 형태로 저장
  # print(removed)

  return result

# test
test = "안뇽 ㅎㅎ 🤔 How was your day 🙈? Have a nice weekend! 💕👭"
print(remove_except_ko(test)) ## 안뇽

os.chdir('path') # 'path' 부분에 채팅 데이터 폴더 경로를 입력해주세요.

df_check = pd.read_csv("word_1.csv")
df_check.head()

data_num = 20 # 데이터 개수를 변경해주세요.

for i in range(1, data_num):
  number = str(i)
  df = pd.read_csv("word_" + number + ".csv") # 데이터에 맞게 이름 설정을 해주세요.

  for i in df.index:
    string = str(df.loc[i,'0'])
    new_string = remove_except_ko(string)

    # "나", "악"과 같은 length가 1인 단어는 제외합니다.
    if len(new_string) == 1:
      new_string = ""

    # 카카오톡 텍스트 추출할 때 생기는 사진, 이모티콘 텍스트는 제외합니다.
    if new_string == "이모티콘" or new_string == "사진":
      new_string = ""

    df.loc[i, 'chat'] = new_string

  df = df[df.chat != ""] # 전처리 후 공백만 남은 row을 제외하고 추출합니다.
  df = df['chat']
  df.to_csv("final_output_" + number + ".csv")

  print("dataset", number, "completed")
