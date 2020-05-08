# Week 8


## Finished work

1. 맞춤법 검사를 대체할 정도의 외부 data 데이터 수집
  - ``대화체 데이터`` [약 13.8만개]
    - 챗봇 데이터
    - 외부에서 수집한 대화체 데이터
    - 한글 위키 (문어체 데이터)
  - ``wiki 데이터``

2.  자모 분리 후 단어의 유사도 구하기
  - edit distance
    - 수집한 data를 control로, 우리의 data를 treatment로 하여 유사도 구하기
  - fast text
    -


## To do next week

1. 라벨링 마치기

2. 모델 학습 시키기
  - 패턴을 통해 규칙을 찾아내는 ``CharCNN``
  - 단어를 문자의 n-gram 조합으로 취급하는 ``FastText``
