# Week 7

## Approach
* Old approach: labeling을 모두 끝낸 후에 model training
* New approach
  - 머거써를 먹었어로 라벨링하는 작업이 결국 우리가 해야하는 task
  - 라벨링과 모델 구현이 별개의 일이 아님!
  - 모델 구현을 어떻게 할지부터 시작
* 우리 문제는 결국 의도적인 표기 오류가 일어난 단어를 **가장 유사한 단어** 로 교정해주는 것

## 단어 유사도를 구하는 방법
1) 의미적 거리
- word 수준 embedding  
  - Word2Vec, **FastText**, NPLM, GloVe
  - 단어 수준 임베딩 기법의 단점은 동음이의어를 분간하기 어려움
  - 단어의 형태가 같다면 동일한 단어로 보고, 모든 문맥 정보를 해당 단어 벡터에 투영하기 때문임
  - https://heung-bae-lee.github.io/2020/02/01/NLP_06/
- sentence 수준 embedding
  - 단어 등장 순서 정보를 명시적으로 학습
  - 예를 들어 한국어에서 배는 배(pear), 배(belly), 배(ship) 등 다양한 의미를 지닌 동음이의어인데 단어 임베딩을 썼다면 이 모든 의미가 뭉뚱 그려져 하나로 표현됨 문장 수준 임베딩 기법을 사용하면 이들을 분리해 이해 가능
  - ELMo, GPT, BERT ...
  - https://heung-bae-lee.github.io/2020/02/06/NLP_08/

2) **형태적 거리**
- ``character level similarity`` is also known as ``string similarity/matching``
- OCR accuracy improvement, 오타 교정에 쓰이는 방법
- ``edit distance`` (최소 편집 거리)
  - https://lovit.github.io/nlp/2018/08/28/levenshtein_hangle/

## 발생한 이슈들
1. ``의미적 거리`` doesn't work
- word 수준 embedding
  - ``Word2Vec``으로 카톡 데이터 내에서 특정 단어에 대해 유사한 단어 찾아봄
- sentence 수준 embedding
  - 채팅 데이터가 완결된 문장이 아니라는 한계점
    - 보통 끊어서 채팅하는 사람도 있음
    - 문장 수준 접근 어려움

2. 형태소 단위의 tokenizing은 채팅체를 잘 tokenize하지 못함
  - 뭐/해 는 tokenize하지만, 모/해는 잘 분석하지 못함
  - 우선 형태소가 아닌 **음절 단위** 로 접근해야겠다는 판단
  - 성능이 안나온다면, 형태소 unsupervised로 학습 가능한 케이스 고려
    - https://github.com/lovit/soynlp

3. 문어체와 대화체의 확연한 차이
- 국립국어원 사전 vocab 구축
  - 표준어를 찾고자 했지만!
  - '먹다', '-어' 이런식으로 표현되어 있어 적용이 어려웠음
- 사전 훈련된 Word2Vec 임베딩 사용해봄
  - training에 사용된 데이터셋이 문어체라 적합하지 않음
  - 문어체와는 사용되는 어체, 단어 도메인 자체가 다름

4. 맞춤법 검사기 api 존재하지 않음
- 네이버, 카카오의 부산대 검사기 표절 이슈, 관련 api 다 막힘, 사용 불가!
- 일단 표기가 올바르게 된 말뭉치 데이터 최대한 많이 수집하기

5. 문어체가 아닌 대화체 데이터셋의 필요성
- 기존 pre-trained 자료를 가져오면, 문어체여서 우리 데이터에 적용할 수 없었음
- 맞춤법 검사가 불가능하므로, 말뭉치 단위로 비교해서 표기 오류 찾을 예정
- 다른 **대화체** 데이터셋 최대한 많이 모아, 표기가 올바른 말뭉치 vocabulary 구축해야 함
- **문어체 데이터 + 대화체 데이터** 를 구축해 대화에 쓰이는 대부분의 말뭉치 커버
  - 학습 말뭉치(training corpus)

## 그러면 우리는?
1. 표기가 올바른 외부 데이터셋과 우리 데이터 대조해 표기 오류가 일어난 단어를 찾음

2. character similarity로 접근!
- ``자모 분리`` - **text vectorization**
  - ``word embedding``이 아니라 ``character embedding``으로 approach
  - [open source](https://github.com/bluedisk/hangul-toolkit)
  - ``ㅁ,ㅓ,ㄱ,ㅓ,ㅆ,ㅓ``
    - 가장 유사한 sequence: ``ㅁ,ㅓ,ㄱ,ㅇ,ㅓ,ㅆ,ㅇ,ㅓ`` (먹었어)
  - ``ㅁ,ㅓ,ㄱ,ㅓ,ㄸ,ㅏ``
    - 가장 유사한 sequence: ``ㅁ,ㅓ,ㄱ,ㅇ,ㅓ,ㅆ,ㄷ,ㅏ`` (먹었어)

2. 단순히 character similarity, edit distance를 구하면 되나?
- No!
  - "그건 모냠?"에서 ``ㅁ,ㅗ,ㄴ,ㅑ,ㅁ``은 ``ㅁ,ㅜ,ㅓ,ㄴ,ㅑ``보다 ``ㅁ,ㅗ,ㅇ,ㅑ,ㅇ``과 유사
- 우리 task는 OCR accuracy improvement, 오타 교정과는 다름
  - 기존 오타 교정 알고리즘의 한계
  - 구글 대체 단어 suggestion에서 ``지금 모해?``는 ``지금 뭐해?``로 제안하지만 ``밥은 머금?``은 대체어를 제안하지 못함

3. 우리가 구하지 못한 case에 대해 모델 학습을 통해 prediction할 수 있어야 함
- 일단 labeling 작업에는 위 approach 적용해 데이터셋 구축
- ``머거써?``를 학습하면 ``죽게써``가 데이터셋에 없어도 잘 변환할 수 있도록

### 모델 workflow
0. model-training
  - 1) 초중종성 단위로 pair 만들기
  - 2) 종성이 없는 경우 e 추가 (optional)
  - 3) 3의 배수로 embedding 후 학습 시킴
    - text: ``머거써`` (ㅁ,ㅓ,e) (ㄱ,ㅓ,e) (ㅆ,ㅓ,e)
    - label: ``먹었어`` (ㅁ,ㅓ,ㄱ) (ㅇ,ㅓ,ㅆ) (ㅇ,ㅓ,e)

1. input으로 채팅체 문장 들어오면 spacing에 따라 말뭉치로 나누기

2. input 말뭉치와 기존 trained corpus를 대조, 비표준어 찾아냄
   1) if 말뭉치 == 표기 OK:
      - 텍스트가 아예 일치하는게 표준어 데이터셋에 있는 경우
      - 만약, 강한 규칙 적용이라면! (to solve 그게 ``모양``?)
        - 표준어로 분류된 case에 대해서도 한 번 더 check
        - 비표준어 case들에서 해당 단어와 가장 유사한 단어 찾기
        - 그 단어의 유사도가 특정 정도 이상이면 이 대체어로 변환하기
   2) elif 말뭉치 != 표기 OK:
      - 이미 학습한 표기 오류면 그대로 변환
      - 학습되지 않은 표기 오류면?
        - 표준어 데이터셋에서 가장 유사한 단어 찾기
        - 모델 자체가 찾은 규칙으로 prediction한 것
          - (ㅈ,ㅜ,ㄱ) (ㄱ,ㅔ,e) (ㅆ,ㅓ,e)
          - (ㅈ,ㅜ,ㄱ) (ㄱ,ㅔ,ㅆ) (ㅇ,ㅓ,e)
        - 두 결과 비교

3. 최종적으로 구한 vector를 단어로 바꾸어 주기

4. output: 단어를 종합, 표기 오류가 교정된 문장  

## Model to train and predict
  - ``CharCNN``
    - https://github.com/yoonkim/lstm-char-cnn
    - https://github.com/srviest/char-cnn-text-classification-pytorch
    - https://yujuwon.tistory.com/entry/Char-based-Text-to-CNN-한글-적용하기

  - ``FastText``
    - https://inspiringpeople.github.io/data%20analysis/word_embedding/
    - 최종적으로 각 단어는 Embedding된 n-gram의 합으로 표현됨
    - 본질적으로 word2vec 모델을 확장한 것이지만, 단어를 문자(character) 의 ngram 조합으로 취급
    - 본 연구에서는 단어를 Bag-of-Characters로 보고, 개별 단어가 아닌 n-gram의 Characters를 Embedding함 (Skip-gram model 사용)
    - Self-trained FastText by FastText API
    - Self-trained FastText by Gensim
    - https://brunch.co.kr/@learning/7
    - https://brunch.co.kr/@learning/8

  - ``ELMo``
    - http://blog.naver.com/PostView.nhn?blogId=gkvmsp&logNo=221496147296
    - 사전 훈련된 언어 모델 사용
    - **character 기반으로 CNN 임베딩한 벡터 input으로 사용**
    - output은 token 단위
    - 내가 가진 데이터로 pre-train 수행할 수 있음
    - 프리트레인(pre-train)이 끝나면 파인튜닝(fine-tuning) 용도로 파라메터를 별도로 저장

  - ``BERT``
    - https://keep-steady.tistory.com/19?category=702926
    - https://www.statestitle.com/resource/using-nlp-bert-to-improve-ocr-accuracy/
    - 사전 훈련된 언어 모델 사용
    - 내가 가진 데이터로 pre-train 수행할 수 있음
    - 프리트레인(pre-train)이 끝나면 파인튜닝(fine-tuning) 수행
    - https://blog.pingpong.us/dialog-bert-pretrain/

---

## Finished work
1. 카톡 말뭉치 데이터셋 구축 완료
- 서영, 미단 각각의 데이터에서 공통으로 나온 단어만 합침
- 총 21923개의 말뭉치

2. 외부 문어체 + 대화체 데이터 수집
- 문어체 데이터
  - 한글 위키 dump
- 대화체 데이터
  - 수집완료
    - [챗봇 데이터](https://github.com/songys/Chatbot_data)
  - 수집중 - AI hub에서 제공하는 데이터 신청 승인 대기중
    - http://www.aihub.or.kr/aidata/85
    - http://www.aihub.or.kr/open_data/ai_starthon_x_naver
    - http://www.aihub.or.kr/keti_data_board/language_intelligence
      - 트위터 기반 일상 대화 데이터셋
      - 대화형 한글 에이전트 데이터셋

3. 챗봇 데이터 대화 말뭉치 데이터셋 구축 완료
- 45225개 -> 중복 제거 후 총 13301개의 말뭉치

3. 우리 데이터셋의 말뭉치와 가장 유사한 챗봇 말뭉치 찾기
- 자모 분리 후 단어 유사도 구하는중
  - [edit distance](https://lovit.github.io/nlp/2018/08/28/levenshtein_hangle/)
  - [FastText](https://inspiringpeople.github.io/data%20analysis/word_embedding/)
- 음절 나누고, 음절 나누지 않고 유사도 구해보기

## To Do
1. 학습에 쓰일 데이터 종합하기 (대화체 + 문어체)
- 수집할 데이터
  - 챗봇 데이터
  - 외부에서 수집한 대화체 데이터
  - 한글 위키 (문어체 데이터)
- 데이터 셋 최대한 큰 규모로 구축
  - 맞춤법 검사의 역할을 대신할 정도의 데이터 셋 구축해야 함
  - 표기 오류가 일어난 단어와 가장 유사한 말뭉치를 잘 찾아줄 수 있도록 해야 함

2. 표기 오류 데이터 분리 및 라벨링
- 우리 채팅 데이터와 외부 데이터셋의 텍스트 유사도 구하기
- 외부 데이터셋에 없는 말뭉치는 표기 오류가 일어났다고 가정
- 해당 단어는 외부 데이터에서 가장 유사한 단어로 일단 라벨링
- 라벨링이 잘 되었는지 검토

## 제안하는 후속 프로젝트
- workflow 반대로, 사람처럼 말하는 챗봇 만들기
