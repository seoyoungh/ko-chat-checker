# ko-chat-checker
본 연구는 경희대학교 ``데이터분석캡스톤디자인`` 수업에서 진행되었습니다.

## Overview

### Needs
일상적인 채팅에서 우리는 구어성이 두드러진 언어 사용을 흔히 볼 수 있습니다. 예로, ``밥은 먹었어?``라는 문장을 채팅에서 ``밥은 머거써?`` 또는 ``밥은 먹어써?`` 등으로 표기하는 것을 들 수 있습니다. 이런 표기법은 오탈자가 아니라 사용자의 의도적 표기법이라는 특이점이 있습니다. 다양한 자동 문법 교정 프로그램에서도 이는 따로 교정되지 않고 있는데, 이러한 언어 습관이 한국어 채팅 데이터 분석을 어렵게 한다고 판단했습니다.

### Goals
본 모델은 의도적인 표기 변형이 이루어진 문장을 표준어로 교정하는 모델입니다. 채팅체를 문법에 맞는 문장으로 교정합니다. 채팅 데이터 분석 전처리 과정에 활용되길 기대합니다.

띄어쓰기 framework는 [chatspace](https://github.com/pingpong-ai/chatspace)를 사용합니다. 이 framework를 통해 교정하지 못한 띄어쓰기 오류, 신조어/축약어 등의 문법 오류는 교정하지 않습니다.

### Example
```머거써?```는 ```먹었어?```로, ```넹, 넵, 넴```은 ```네```로, ```조아```는 ```좋아```로 교정합니다.

## Schedule

### Plan
* **March**
  - 주제 선정 ⭕️

* **April**
  - 표기 변형 케이스 조사 ⭕️
  - 연구에 사용할 프레임워크 및 데이터셋 조사 ⭕️
  - 데이터 수집 및 EDA ⭕️
  - 데이터 전처리 ⭕️
  - 문법 오류가 있는 데이터와 오류가 없는 데이터 분리 🔜
  - 데이터 라벨링 작업 수행 및 5:5로 분리

* **May**
  - 음운 분리 작업 수행
  - K-fold 도입을 위한 베이스 구축
  - CNN 기반 모델
  - RNN(LSTM) 기반 모델 구축
  - 모델 성능 비교 및 최종 모델 채택

* **June**
  - 최종 모델 성능 평가 및 보완
  - 파이썬 모듈 구축
  - 자동 띄어쓰기 및 단어 분리 코드 추가
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

### chat_preprocessing
전처리 과정에 쓰이는 코드 set입니다.

### chat_data
preprocessing이 끝난 카카오톡 데이터입니다.

## Developers
* [Seoyoung Hong](https://github.com/seoyoungh) from Kyunghee Univ.
* [Midan Shim](https://github.com/midannii) from Kyunghee Univ.
