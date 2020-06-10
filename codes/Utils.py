from gensim.corpora.dictionary import Dictionary
from chatspace import ChatSpace

import os
import sys
import re
import pathlib
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from ._index import LevenshteinIndex # edit distance
from . import CustomModel
from . import Jamo

from .CustomModel import *
from .Jamo import *

# 사전 & 사후 spacing
def spacer(text):
  spacer = ChatSpace()
  result = spacer.space(text)
  return result

# spacing 단위로 tokenize
def tokenizer(text):
  return list(text.split(" "))

# 사전 로드
fn = pathlib.Path(__file__).parent / 'dictionary.txt'
loaded_dct = Dictionary.load_from_text(fn)

# 표기 오류가 있는 단어 indices, words return
def check_error(word_list):
  wrong_ids = []
  wrong_words = []
  pattern = re.compile('[ㄱ-ㅣa-zA-Z0-9]+')

  for i in range(len(word_list)):
    word = word_list[i]
    matched = pattern.search(word)
    hangul = re.compile('[^가-힣]+')
    word = hangul.sub('', word) # 특수문자, 이모지 제거

    # 한글 자모, 영어, 숫자가 포함된 경우는 패스
    if matched != None:
      pass
    elif word == "": # 특수문자만 있었던 경우
      pass
    elif word in loaded_dct.token2id:
      pass
    else:
      wrong_ids.append(i)
      wrong_words.append(word_list[i])

  return wrong_ids, wrong_words

# 특수문자는 다 제거하지만, 끝에 .,!?가 오는 경우에는 모든 처리가 끝난 후 붙여줄 것
# return 특수문자 제거된 표기 오류 리스트, 처리가 끝난 후 붙여줄 mark와 index를 담은 리스트

def clean_w_pceq(id_list, text_list):
  pattern = re.compile('[.,!?]')
  cleaned = []
  pceq = []

  for idx in id_list:
    text = text_list[idx]
    matched = pattern.search(text)

    if matched == None:
      pass
    elif text.endswith('.'):
      pceq.append([idx, "."])
    elif text.endswith(','):
      pceq.append([idx, ","])
    elif text.endswith('!'):
      pceq.append([idx, "!"])
    elif text.endswith('?'):
      pceq.append([idx, "?"])
    else:
      pass

    hangul = re.compile('[^가-힣]+')
    new_text = hangul.sub('', text) # 특수문자, 이모지 제거

    cleaned.append(new_text)

  return cleaned, pceq

def split_text(text):
  t = ""
  for item in text:
    d = Jamo.split_syllables(item)
    if len(d) != 3:
      d = d + "P"
      t = t + d
    else:
      t = t + d

  return t

def join_text(text):
  new = list(filter(lambda a: a != 'p', text))
  new = list(filter(lambda a: a != '<eos>', new))

  join = Jamo.join_jamos(new)

  return join

# Custom Model에서 구하기
def seq2seq(text_list):
  model = CustomModel.model
  prediction_list = []

  for item in text_list:
    text = split_text(item) # 오류 있는 단어 tokenizing and padding
    prediction, attention = CustomModel.translate_sentence(text, model, CustomModel.device)
    prediction_list.append(prediction)

  for i in range(len(prediction_list)):
    joined = join_text(prediction_list[i]) # 다시 tockenizing and padding 풀기
    prediction_list[i] = joined

  return prediction_list

fn = pathlib.Path(__file__).parent / 'clean_dataset.csv'
default_word = pd.read_csv(fn, names = ['num', 'words'])
default_word = list(default_word['words'])[1:]

# 빠른 Edit Distance 도출을 위한 indexer
indexer = LevenshteinIndex(default_word, verbose=True)

# Edit Distance로 구하기
# 최대 distance 0.4로 설정
def edit_distance_04(text_list):
    """
    output example:
    [('그래', 0),
    ('그대', 0.3333333333333333),
    ('그려', 0.3333333333333333)]
    """

    prediction_list = []
    for item in text_list:
        result = indexer.jamo_levenshtein_search(item, max_distance=0.4)
        prediction_list.append(result)

    return prediction_list

# Edit Distance로 구하기
# 최대 distance 1.0로 설정
def edit_distance_10(text_list):
    """
    output example:
    [('그래', 0),
    ('그대', 0.3333333333333333),
    ('그려', 0.3333333333333333)]
    """

    prediction_list = []
    for item in text_list:
        result = indexer.jamo_levenshtein_search(item, max_distance=1)
        prediction_list.append(result)

    return prediction_list

def compare(wrong_list, model_list, edit_list):
    final_output = []

    for i in range(len(model_list)):
        if edit_list[i] == []: # edit distance로 예측한 결과가 없는 경우
            final_output.append(model_list[i])

        else:
            size = len(edit_list[i])

            if wrong_list[i] == model_list[i]: # model이 원래 text 그대로 output을 낸 경우
                edit_only_word = "["
                for j in range(size):
                    if j == (size-1):
                        edit_only_word = edit_only_word + str(edit_list[i][j][0]) + "]"
                    else:
                        edit_only_word = edit_only_word + str(edit_list[i][j][0]) + ", "
                final_output.append(edit_only_word)

            else:
                same_check = False
                for j in range(size):
                    if edit_list[i][j][0] == model_list[i]:
                        same_check = True

                if same_check == True:
                    final_output.append(model_list[i])

                else:
                    if model_list[i] in loaded_dct.token2id:
                        final_output.append(model_list[i])
                    else:
                        edit_only_word = "["
                        for j in range(size):
                            if j == (size-1):
                                edit_only_word = edit_only_word + str(edit_list[i][j][0]) + "]"
                            else:
                                edit_only_word = edit_only_word + str(edit_list[i][j][0]) + ", "
                        final_output.append(edit_only_word)

    return final_output

# 오류 교정된 단어 기존 리스트에 대체해주기 (문장부호 포함)
# All inputs are lists
def correct(origin, idx, corrected, pceq):
  count = 0
  for i in idx:
    origin[i] = corrected[count]
    count += 1

  if len(pceq) == 0:
    pass
  else:
    for case in pceq:
      idx = case[0]
      mark = case[1]
      origin[idx] = origin[idx] + mark

  return origin

# 문장으로 합치기
def sum(corrected):
  result = ""
  length = len(corrected)

  for i in range(length):
    if i != length - 1:
      result += corrected[i] + " "
    else: # 끝에는 No spacing
      result += corrected[i]

  return result

#늘어지는 말들 줄이기
kor_begin = 44032
kor_end = 55203
chosung_base = 588
jungsung_base = 28
jaum_begin = 12593
jaum_end = 12622
moum_begin = 12623
moum_end = 12643

chosung_list = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
        'ㅅ', 'ㅆ', 'ㅇ' , 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

jungsung_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ',
        'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ',
        'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ',
        'ㅡ', 'ㅢ', 'ㅣ']

jongsung_list = [
    ' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ',
        'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
        'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ',
        'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

jaum_list = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ',
              'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ',
              'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

moum_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
              'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

def compose(chosung, jungsung, jongsung):
    char = chr(
        kor_begin +
        chosung_base * chosung_list.index(chosung) +
        jungsung_base * jungsung_list.index(jungsung) +
        jongsung_list.index(jongsung)
    )
    return char

def decompose(c):
    if not character_is_korean(c):
        return None
    i = ord(c)
    if (jaum_begin <= i <= jaum_end):
        return (c, ' ', ' ')
    if (moum_begin <= i <= moum_end):
        return (' ', c, ' ')

    # decomposition rule
    i -= kor_begin
    cho  = i // chosung_base
    jung = ( i - cho * chosung_base ) // jungsung_base
    jong = ( i - cho * chosung_base - jung * jungsung_base )
    #if jong == ' ': jong = 'e'
    return (chosung_list[cho], jungsung_list[jung], jongsung_list[jong])

def character_is_korean(c):
    i = ord(c)
    return ((kor_begin <= i <= kor_end) or
            (jaum_begin <= i <= jaum_end) or
            (moum_begin <= i <= moum_end))

def make_shorter_word(word):
  de = []
  output = []
  for w in word:
    de.append(decompose(w))

  if de.count(" ")>=2:
    print('case')
    if len(de)==2:
      print(compose(de[0][0], de[1][1], ' '))
    elif len(de)==3:
      print(compose(de[0][0], de[1][1], de[2][0]))
    else:
      print(compose(de[0][0], de[1][1], ' ')+compose(de[2][0], de[3][1], ' '))

  result = ""
  length = len(de)
  for i in range(len(de)): # 모든 글자에 대해
    if de[i][0] != 'ㅇ': # 첫글자 초성이 ㅇ이 아닐때
       if i+2<=length and de[i][1] == de[i+1][1]:
         if i+3<=length and de[i][1] == de[i+2][1]:
           if i+4<=length and de[i][1] == de[i+3][1]:
             output.append([de[i][0], de[i][1], de[i+3][2]])
           else:
             output.append([de[i][0], de[i][1], de[i+2][2]])
         else:
           output.append([de[i][0], de[i][1], de[i+1][2]])
       else:
         output.append(de[i])
    else:
       # 앞글자와 같은 중성이면, pass
      if i!=0 and de[i][1] == de[i-1][1]:
        pass
      elif i+2<=length and de[i][1] == de[i+1][1]:
        if i+3<=length and de[i][1] == de[i+2][1]:
          if i+4<=length and de[i][1] == de[i+3][1]:
            output.append([de[i][0], de[i][1], de[i+3][2]])
          else:
           output.append([de[i][0], de[i][1], de[i+2][2]])
        else:
         output.append([de[i][0], de[i][1], de[i+1][2]])
      else:
        output.append(de[i])
  short = []

  for i in range(len(output)):
    if output[i][0]!=' ' and output[i][1]!=' ':
      result += compose(output[i][0], output[i][1], output[i][2])
    elif output[i][1]==' ':
      short.append(output[i][0])
    elif output[i][0]==' ':
      short.append(output[i][1])

  if len(short)>0:
    if len(short)==2:
      result = compose(short[0], short[1], ' ')
    elif len(short)==3:
      result = compose(short[0], short[1], short[2])
  return result
