# ko-chat-checker
본 연구는 경희대학교 ``데이터분석캡스톤디자인`` 수업에서 진행되었습니다.

## Overview

### Needs
일상적인 채팅에서 우리는 구어성이 두드러진 언어 사용을 흔히 볼 수 있습니다. 예로, ``밥은 먹었어?``라는 문장을 채팅에서 ``밥은 머거써?`` 또는 ``밥은 먹어써?`` 등으로 표기하는 것을 들 수 있습니다. 이러한 언어 습관은 한국어 채팅 데이터 분석을 어렵게 합니다. 다양한 자동 문법 교정 프로그램에서도 이는 완벽히 교정되지 않고 있습니다. 실제로 Google 대체 단어 suggestion에서 ``지금 모해?``는 ``지금 뭐해?``로 제안하지만 ``밥은 머금?``은 대체어를 제안하지 못하는 것을 볼 수 있습니다. 오탈자가 아니라 사용자가 의도적으로 표기 오류를 낸 것으로, OCR 연구와 misspell checking과는 결이 다르므로 연구가 필요합니다.

### Goals
본 모델은 의도적인 표기 변형이 이루어진 문장을 표준어로 교정하는 모델입니다. 채팅체로 쓰여진 문장을 문법에 맞는 문장으로 교정합니다. 채팅 데이터 분석 전처리 과정에 활용되길 기대합니다. 그리고 후속 연구로는 모델을 반대의 flow로 배치해 사람처럼 말하는 챗봇을 만들어 보는 것을 제안합니다.

띄어쓰기 framework는 [chatspace](https://github.com/pingpong-ai/chatspace)를 사용합니다. 이 framework를 통해 교정하지 못한 띄어쓰기 오류, 신조어/축약어 등의 문법 오류는 교정하지 않습니다.

### How it works?
교정을 위해 다음 두 가지 방법을 사용합니다.  

1) ``Seq2Seq`` Model with ``Attention``

모델 학습에 쓰인 채팅체 데이터는 두 연구자의 카톡 데이터에서 공통으로 나온 단어만 추출한 데이터입니다. 전체 21923개의 단어 중 2432개가 의도적인 표기 오류를 포함한 case로 분류되었습니다. 그리고, 모델 학습을 위해 해당 단어를 교정해 라벨링했습니다. 더 나은 모델학습을 위해 단어의 초,중,종성을 분리하고 종성이 없는 경우 padding을 넣었습니다.

```
original text
text: 모해용 label: 뭐해요

modified text
text: ㅁㅗPㅎㅐPㅇㅛㅇ label: ㅁㅝPㅎㅐPㅇㅛP
```
그리고 적은 데이터를 보완하고, case를 일반화하기 위해 n-gram 기법을 적용해 10159개로 학습 데이터를 늘렸습니다.
```
text: ㅁㅗPㅎㅐP label: ㅁㅝPㅎㅐP
text: ㅗPㅎㅐPㅇ label: ㅝPㅎㅐPㅇ
text: PㅎㅐPㅇㅛ label: PㅎㅐPㅇㅛ
text: ㅎㅐPㅇㅛㅇ label: ㅎㅐPㅇㅛP
```

결과적으로, 아래와 같은 성능을 내는 모델을 구축했습니다.
- test accuracy
  - 82.3% (400/486)
- train accuracy
  - 94.3% (8753/9284)
- n-gram 제외 전체 데이터
  - 89.3% (2171/2432)
- n-gram 포함 전체 데이터
  - 93.3% (9476/10159)

2) ``Edit Distance``

텍스트 유사도를 구하기 위한 척도로 자모 분리 후의 ``Edit Distance``를 채택했습니다. [빠른 한글 수정 거리 검색](https://github.com/lovit/inverted_index_for_hangle_editdistance)을 활용했습니다.


### Correction Example
```머거써?```는 ```먹었어?```로, ```넹, 넵, 넴```은 ```네```로, ```조아```는 ```좋아```로 교정합니다.

## Installation

```
pip install chatchecker
```

```python
from chatchecker import ChatChecker
```

### Requirements
``GPU``환경이어야 합니다. 구동을 위해 필요한 라이브러리는 아래와 같습니다.  
``pytorch`` ``torchtext`` ``gensim`` ``pandas``

### Guideline
1) ``Edit Distance``의 경우 동일한 거리를 갖는 모든 단어를 리스트로 return합니다.  
2) 문장이 input일 때, 표기 오류가 있는 단어를 분류할 맞춤법 검사 API가 따로 존재하지 않습니다. 따라서, 자체적으로 구어체 말뭉치 데이터 (약 13만개)를 수집했습니다. 이 데이터에 해당 단어가 포함되면 표기 오류가 없는 데이터로, 데이터에 존재하지 않는 단어라면 표기 오류가 있는 단어로 분류되어 교정이 진행됩니다.

### Using Example
1) 표기 오류가 있는 단어가 input일 때
```python
test_word = "모행"
model_word = ChatChecker.model_only_word(test_word) # 모델만 사용해 교정
edit_word = ChatChecker.edit_only_word(test_word) # Edit Distance만 사용해 교정
model_word, edit_word = ChatChecker.both_word(test_word) # 두 결과 모두 return
```
output
```
model_word: 뭐해
edit_word: 모형
```


2) 표기 오류가 있는 단어와 없는 단어가 섞인 문장이 input일 때
```python
test = "이짜나, 배고픈뎅 머행 밥머것어! 아까 밥먹었즤 월욜에보까? 조아요 사랑행 😌!"
model_sentence = ChatChecker.model_only(test) # 모델만 사용해 교정
both_sentence = ChatChecker.both(test) # 자체 rule에 따라 두 방법을 조합해 교정
```
output
```
있잖아, 배고픈데 뭐해 밥 먹었어! 아까 밥 먹었지 월요일에 볼까? 좋아요 사랑해 😌!
```



## workflow 


![workflow](https://github.com/seoyoungh/ko-chat-checker/blob/master/progress/assets/images/workflow.JPG)




## Developers
* [Seoyoung Hong](https://github.com/seoyoungh) from Kyunghee Univ.
* [Midan Shim](https://github.com/midannii) from Kyunghee Univ.



|  Period    |    workflow     |   role.  |
| :------------- | :------------- | :---------------|
| 4월 | 	데이터 수집| 	홍서영, 심미단 | 
 | 4월 | 데이터 전처리 및 라벨링	홍서영, 심미단  | 
 | 4월 | 	모델 리서치	홍서영 | 
 | 5월 | 	모델 학습 (charCNN, FastText, ELMo, seq2seq)	홍서영, 심미단 | 
 | 5월 | 	edit distance 코드 작성	심미단 | 
 | 5월 | 	최종 모델 채택 및 보완 (seq2seq)	홍서영 | 
 | 6월 | 	모델과 edit distance의 성능 비교 	홍서영, 심미단 | 
 | 6월 | 	파이썬 모듈 구축	홍서영 | 
 | 6월	 | 결과 보고서 작성	홍서영, 심미단 | 
 | 4월 - 6월 | github repository 작성	홍서영, 심미단 | 

