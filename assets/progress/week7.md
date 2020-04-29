# Week 7

## finished work
* Old approach: labeling을 모두 끝낸 후에 model training
* New approach
  - 머거써를 먹었어로 라벨링하는 작업이 결국 우리가 해야하는 task
  - 라벨링과 모델 구현이 별개의 일이 아님!
  - 같이 진행하자!
---
### 모델 구축 방향성, 알고리즘

1. Word2Vec
- ``LANGUAGE MODELING``
- ``text vectorization``, ``word embedding``
- 형태소별로 대체되는 단어를 찾을 수 있지 않을까?

- 단어 분리 전 문장 형태의 서영 카톡 데이터 사용
- 다양한 분석기(Okt, Kkma, Mecab)로 형태소 토큰화 시도해봄
  - 학습 속도: Kkma < Okt < Mecab 순으로 빠름
  - 정확도: (문어체에서는) Kkma < Okt < Mecab (대화체는) 고만고만
- 우리가 가진 데이터 셋에서 Word2Vec을 시도하면 ``안뇽``와 비슷한 단어가 ``안녕``이 아니라 ``아하``, ``우와``와 같은 단어로 나옴
- 같은 자리에 오는 단어를 유사하다고 판단하는 것
  - 우리가 하고자 하는 task와는 방향성이 조금 다름

- 사전 훈련된 Word2Vec 임베딩 사용해봄
  - 이 데이터셋은 문어체여서 적합하지 않았음, 대화체의 데이터셋을 구해야 함!

- 그래도 형태소 분리를 통해 형태소를 나누고 분리해서 유사한 단어를 찾아볼 수 있겠다는 가능하다는 방향성 발견
  - 뭐/해 에서 모/해 머/해
  - 먹/고/있/어 먹/고/이/써

- 미단님 데이터까지 합해서 한 번 더 진행
  - **문장 단위** 데이터셋 하나로 다 합치고(코드 실종 ㅜㅜ), 전처리하기
    - 전처리 code: ``ko_preprocessing_young_문장단위``
  - 서영 데이터랑 합쳐서 Word2Vec 돌려보기
  - code: ``Word2Vec``, ``KoNLPy_형태소분석``

- 새로 수집한 외부의 일상 대화 데이터 셋과 우리가 가진 데이터를 합쳐서 다시 도전해보기
  - 특수문자 전처리한거 다시 고려해야하나?

2. 대화 데이터셋에서 가장 유사한 단어 찾기
- **TEXT SIMILARITY**
- ``text vectorization``, ``character embedding``
- **자모 분리**: ``word embedding``이 아니라 ``character embedding``으로 approach
  - [open source](https://github.com/bluedisk/hangul-toolkit)
- ㅁ,ㅓ,ㄱ,ㅓ,ㅆ,ㅓ
  - 가장 유사한 sequence: ㅁ,ㅓ,ㄱ,ㅇ,ㅓ,ㅆ,ㅇ,ㅓ (먹었어)
- ㅁ,ㅓ,ㄱ,ㅓ,ㄸ,ㅏ
  - 가장 유사한 sequence: ㅁ,ㅓ,ㄱ,ㅇ,ㅓ,ㅆ,ㄷ,ㅏ (먹었어)
- 대화체 데이터셋 최대한 많이 모아서 vocabulary 구축하는 것이 가장 중요

- 빈도수가 그래도 꽤 있는 표기 오류에 대해 분석하기
  - 친구 이름 같은 것 제거 할 수 있지 않을까?
  - torch의 build_vocab 활용
  - code: ``build_chat_vocab``

4. 변환 규칙 발견
- ``TEXT CLASSIFICATION``
- ``character embedding``, ``text prediction``
- 단순히 유사한 단어를 찾아주는 것은 한계가 있음
- 분명 규칙성이 있을 것
- 2번 approach를 통해 labeling된 데이터를 가지고 모델 학습 진행

4. 최종 모델 방향성
- 1,2,3을 종합해서 정확도를 가장 높이는 모델 구현!

---

### 기타 작업
1. misspell checker
- 의도적인 문법 오류 보다는, 단순한 오타인 경우가 많음

2. 맞춤법 검사기 기근
- 네이버, 카카오가 부산대 검사기 베낌
- 그래서 api 다 막힘, 사용 불가!

3. 국립국어원 사전 vocab 구축
- 표준어를 찾고자 했지만!
- '먹다', '-어' 이런식으로 표현되어 있어 적용이 어려울 듯
- 실제로 일상에서 쓰이지 않는 단어가 대부분
- 문어체와 대화체에는 확연한 차이가 있었음

### 한국어 채팅 데이터 - BERT 🌼
- https://deview.kr/2019/schedule/285
- https://blog.pingpong.us/dialog-bert-pretrain/

---

## to do
1. 미단님 데이터까지 합해 우리가 가진 데이터로 Word2Vec 돌려보기
2. 일상적인 대화 데이터 많이 구해야함
   - http://www.aihub.or.kr/aidata/85
   - http://www.aihub.or.kr/open_data/ai_starthon_x_naver
   - http://www.aihub.or.kr/keti_data_board/language_intelligence
     - 트위터 기반 일상 대화 데이터셋
     - 대화형 한글 에이전트 데이터셋
   - https://github.com/songys/Chatbot_data
3. 해당 데이터와 우리 데이터 합해 Word2Vec 다시 해보기
4. 우리가 가진 word 단위 데이터 자모분리
   - 적용할 수 있는 모델 reference 많이 찾아보기
   - CNN/RNN/Transformer
   - BERT, XLNet이 최근에는 가장 좋은 성능을 내고 있음
5. 구한 데이터 자모분리
6. 구한 데이터에서 우리가 가진 word와 가장 유사한 word 찾기
7. 두 개가 일치하지 않는 경우에서 dictionary 구축해 most common cases 도출
8. 약 10000개 정도 목표로 하고, labeling 작업 수행
9. TEXT CLASSIFICATION task로 넘어가기
10. 라벨링한 데이터로 학습 시작, 규칙 발견, prediction
