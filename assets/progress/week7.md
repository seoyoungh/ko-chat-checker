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
  - 단어 수준 임베딩 기법의 단점은 동음이의어(Homonym)를 분간하기 어려움 - 단어의 형태가 같다면 동일한 단어로 보고, 모든 문맥 정보를 해당 단어 벡터에 투영하기 때문임
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
1. 의미적 거리 doesn't work
- ``Word2Vec``으로 카톡 데이터 내에서 특정 단어에 대해 유사한 단어 찾아봄
- 채팅 데이터가 완결된 문장이 아니라는 한계점
  - 보통 끊어서 채팅하는 사람도 있음
  - 문장 수준 접근 어려움

2. 형태소 단위의 tokenizing은 채팅체를 잘 tokenize하지 못함
  - 뭐/해 는 tokenize하지만, 모/해는 잘 분석하지 못함
  - 우선 형태소가 아닌 음절 단위로 접근해야겠다는 판단
  - 성능이 안나온다면, 형태소 unsupervised로 학습 가능한 케이스 고려
    - https://github.com/lovit/soynlp

3. 문어체와 대화체의 확연한 차이
- 국립국어원 사전 vocab 구축
  - 표준어를 찾고자 했지만!
  - '먹다', '-어' 이런식으로 표현되어 있어 적용이 어려웠음
- 사전 훈련된 Word2Vec 임베딩 사용해봄
  - training에 사용된 데이터셋이 문어체라 적합하지 않음

4. 맞춤법 검사기 api 존재하지 않음
- 네이버, 카카오의 부산대 검사기 표절 이슈, 관련 api 다 막힘, 사용 불가!
- 일단 표기가 올바르게 된 대화 말뭉치 데이터 최대한 많이 수집해 커버
- 구축한 데이터셋이 대화에 쓰이는 대부분의 경우를 커버해야함

5. 다른 대화 데이터셋의 필요성
- 기존 pretrained 자료를 가져오면, 문어체여서 우리 데이터에 적용할 수 없었음
- 맞춤법 검사가 불가능하므로, 말뭉치 단위로 비교해서 표준어 찾을 예정
- 우리 데이터는 한정된 데이터
- 다른 **대화체** 데이터셋 최대한 많이 모아, 표기가 올바른 말뭉치 vocabulary 구축하는 것이 가장 중요
  - 학습 말뭉치(training corpus)


6. 수집한 일상 대화 데이터
- [챗봇 데이터](https://github.com/songys/Chatbot_data)
- http://www.aihub.or.kr/aidata/85
- http://www.aihub.or.kr/open_data/ai_starthon_x_naver
- http://www.aihub.or.kr/keti_data_board/language_intelligence
  - 트위터 기반 일상 대화 데이터셋
  - 대화형 한글 에이전트 데이터셋


## 그러면 우리는?
1. character similarity로 접근!
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
- 구글 대체 단어 suggestion에서 ``지금 모해?``는 ``지금 뭐해?``로 제안하지만 ``밥은 머금?``은 제안하지 못함

3. 우리가 구하지 못한 case에 대해 모델 학습을 통해 prediction할 수 있어야 함
- 일단 labeling 작업에는 위 approach 사용해서 데이터셋 구축
- ``머거써?``를 학습하면 ``죽게써``가 데이터셋에 없어도 잘 변환할 수 있도록

4. 제안하는 후속 프로젝트
- workflow 반대로, 사람처럼 말하는 챗봇 만들기

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
    - 내가 가진 데이터로 pretrain 수행할 수 있음
    - 프리트레인(pretrain)이 끝나면 파인튜닝(fine-tuning) 용도로 파라메터를 별도로 저장

  - ``BERT``
    - https://keep-steady.tistory.com/19?category=702926
    - https://www.statestitle.com/resource/using-nlp-bert-to-improve-ocr-accuracy/
    - 사전 훈련된 언어 모델 사용
    - 내가 가진 데이터로 pretrain 수행할 수 있음
    - 프리트레인(pretrain)이 끝나면 파인튜닝(fine-tuning) 수행
    - https://blog.pingpong.us/dialog-bert-pretrain/

## 모델 workflow
0. 모델 학습
  1. 초중종성 단위로 pair 만들기
  2. 종성이 없는 경우 e 추가 (optional)
  3. 3의 배수로 embedding
    (ㅂ,ㅏ,e) (ㅂ,ㅜ,e) (ㅇ,ㅑ,ㅁ)
    (ㅂ,ㅏ,e) (ㅂ,ㅗ,e) (ㅇ,ㅑ,e)
  4. 모델이 자체적으로 학습
  5. 최종적으로 구한 vector를 단어로 바꾸어 주기

1. 인풋으로 "채팅체" 들어오면 spacing에 따라 말뭉치로 나누기
2. 모델 자체가 학습한대로 비표준어 찾아냄
   1. if 말뭉치 == 표기 OK:
      - 텍스트가 아예 일치하는게 표준어 데이터셋에 있는 경우
      - 우리가 놓친 표기가 올바른 단어가 있을 수 있으므로 외부에서 표기가 올바른지 검증해볼 수 있는 것 추가되어야 함
        - 기존에 구축된 한국어 말꾸러미
      - 만약, 강한 규칙 적용이라면! (to solve 그게 ``모양``?)
        - 표준어로 분류된 case에 대해서도 한 번 더 check
        - 비표준어 case들에서 해당 단어와 가장 유사한 단어 찾기
        - 그 단어의 유사도가 특정 수치 이상이면 이 대체어로 변환하기
   2. elif 말뭉치 != 표기 OK:
      - 표준어 데이터셋에서 가장 유사한 단어 찾기
      - 모델 자체가 찾은 규칙으로 prediction한 것
      - 두 결과 비교

---

## To do
1. 카톡 말뭉치 데이터셋 만들기
- 서영, 미단 각각의 데이터에서 공통으로 나온 단어만 합치기
  - 공통으로 쓰였을만한 텍스트는 인위적으로 처리
2. 챗봇 말뭉치 데이터셋 만들기
- 우선 질문 데이터만 사용, 다른 데이터의 질을 보고 답변 데이터도 쓸지 결정
3. 우리 데이터셋의 말뭉치와 가장 유사한 챗봇 말뭉치 찾기
- 단어 유사도 구하기
  - [edit distance](https://lovit.github.io/nlp/2018/08/28/levenshtein_hangle/)
  - [FastText](https://inspiringpeople.github.io/data%20analysis/word_embedding/)
    - 우선 챗봇 데이터로 학습시켜서 유사한 단어 구해볼 수 있을듯
- 자모분리 (모델 안에서 구함)
- 처음에는 음절 나누지 않고 유사도 구해보기
4. 모델 서칭
- CharCNN, FastText, ELMo, BERT
