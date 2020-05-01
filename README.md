# ko-chat-checker
본 연구는 경희대학교 ``데이터분석캡스톤디자인`` 수업에서 진행되었습니다.

## Overview

### Needs
일상적인 채팅에서 우리는 구어성이 두드러진 언어 사용을 흔히 볼 수 있습니다. 예로, ``밥은 먹었어?``라는 문장을 채팅에서 ``밥은 머거써?`` 또는 ``밥은 먹어써?`` 등으로 표기하는 것을 들 수 있습니다. 이러한 언어 습관은 한국어 채팅 데이터 분석을 어렵게 합니다. 다양한 자동 문법 교정 프로그램에서도 이는 완벽히 교정되지 않고 있습니다. 실제로 Google 대체 단어 suggestion에서 ``지금 모해?``는 ``지금 뭐해?``로 제안하지만 ``밥은 머금?``은 대체어를 제안하지 못하는 것을 볼 수 있습니다. 오탈자가 아니라 사용자의 의도적으로 표기 오류를 낸 것으로, OCR 연구와 misspell checking과는 결이 다르므로 연구가 필요합니다. 

### Goals
본 모델은 의도적인 표기 변형이 이루어진 문장을 표준어로 교정하는 모델입니다. 채팅체로 쓰여진 문장을 문법에 맞는 문장으로 교정합니다. 채팅 데이터 분석 전처리 과정에 활용되길 기대합니다. 그리고 후속 연구로는 모델을 반대의 flow로 배치해 사람처럼 말하는 챗봇을 만들어 보는 것을 제안합니다.

띄어쓰기 framework는 [chatspace](https://github.com/pingpong-ai/chatspace)를 사용합니다. 이 framework를 통해 교정하지 못한 띄어쓰기 오류, 신조어/축약어 등의 문법 오류는 교정하지 않습니다.

### Example
```머거써?```는 ```먹었어?```로, ```넹, 넵, 넴```은 ```네```로, ```조아```는 ```좋아```로 교정합니다.

## Model Workflow
0. model-training
  1. 초중종성 단위로 pair 만들기
  2. 종성이 없는 경우 e 추가 (optional)
  3. 3의 배수로 embedding 후 학습 시킴
    - text: ``머거써`` (ㅁ,ㅓ,e) (ㄱ,ㅓ,e) (ㅆ,ㅓ,e)
    - label: ``먹었어`` (ㅁ,ㅓ,ㄱ) (ㅇ,ㅓ,ㅆ) (ㅇ,ㅓ,e)

1. input으로 채팅체 문장 들어오면 spacing에 따라 말뭉치로 나누기

2. input 말뭉치와 기존 trained corpus를 대조, 비표준어 찾아냄
   1. if 말뭉치 == 표기 OK:
      - 텍스트가 아예 일치하는게 표준어 데이터셋에 있는 경우
      - 만약, 강한 규칙 적용이라면! (to solve 그게 ``모양``?)
        - 표준어로 분류된 case에 대해서도 한 번 더 check
        - 비표준어 case들에서 해당 단어와 가장 유사한 단어 찾기
        - 그 단어의 유사도가 특정 정도 이상이면 이 대체어로 변환하기
   2. elif 말뭉치 != 표기 OK:
      - 이미 학습한 표기 오류면 그대로 변환
      - 학습되지 않은 표기 오류면?
        - 표준어 데이터셋에서 가장 유사한 단어 찾기
        - 모델 자체가 찾은 규칙으로 prediction한 것
          - (ㅈ,ㅜ,ㄱ) (ㄱ,ㅔ,e) (ㅆ,ㅓ,e)
          - (ㅈ,ㅜ,ㄱ) (ㄱ,ㅔ,ㅆ) (ㅇ,ㅓ,e)
        - 두 결과 비교

3. 최종적으로 구한 vector를 단어로 바꾸어 주기

4. output: 단어를 종합, 표기 오류가 교정된 문장  

## Schedule

### Plan
* **March**
  - 주제 선정 ⭕️

* **April**
  - 표기 변형 케이스 조사 ⭕️
  - 연구에 사용할 프레임워크 및 데이터셋 조사 ⭕️
  - 데이터 수집 및 EDA ⭕️
  - 데이터 전처리 ⭕️

* **May**
  - 표기 오류가 없는 문어체 + 대화체 외부 데이터셋 구축 🔜
  - 표기 오류가 있는 데이터 분리, 라벨링 작업 수행 🔜
    - 외부 데이터와 ``character level text similarty`` 구해서 진행
      - ``Edit Distance``
      - ``FastText``
  - 모델 학습  
    - 음절로 분리해 학습 진행
      - e.g.) ``(ㅁ,ㅓ,e) (ㄱ,ㅓ,e) (ㅆ,ㅓ,e)``
    - 사용해볼 모델
      - CharCNN
      - FastText
      - ELMo
      - BERT
  - 모델 성능 비교 및 최종 모델 채택

* **June**
  - 최종 모델 성능 평가 및 보완
  - 파이썬 모듈 구축
  - 결과 보고서 작성
  - Github Repo 배포

### Progress Report

| March | April |  May  | June  |
|------ |-------|-------|-------|
| [Week3](/assets/progress/week3.md) | [Week4](/assets/progress/week4.md) | [Week8](/assets/progress/week8.md) | [Week12](/assets/progress/week12.md) |
| | [Week5](/assets/progress/week5.md) | [Week9](/assets/progress/week9.md) | [Week13](/assets/progress/week13.md) |
| | [Week6](/assets/progress/week6.md) | [Week10](/assets/progress/week10.md) | [Week14](/assets/progress/week14.md) |
| | [Week7](/assets/progress/week7.md) | [Week11](/assets/progress/week11.md) | [Week15](/assets/progress/week15.md) |

## Detail Usage


## Developers
* [Seoyoung Hong](https://github.com/seoyoungh) from Kyunghee Univ.
* [Midan Shim](https://github.com/midannii) from Kyunghee Univ.
