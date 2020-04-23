# ko-chat-checker

의도적인 표기 변형이 이루어진 문장을 표준어로 교정하는 모델입니다. 채팅체를 문법에 맞는 문장으로 교정합니다. 채팅 데이터 분석 전처리 과정에 활용되길 기대합니다.

```머거써?```는 ```먹었어?```로, ```넹, 넵, 넴```은 ```네```로, ```조아```는 ```좋아```로 교정합니다.


띄어쓰기 framework는 [chatspace](https://github.com/pingpong-ai/chatspace)를 사용합니다. 이 framework를 통해 교정하지 못한 띄어쓰기 오류, 신조어/축약어 등의 문법 오류는 교정하지 않습니다.

## Detail Usage

### chat_preprocessing
전처리 과정에 쓰이는 코드 set입니다.

### chat_data
preprocessing이 끝난 카카오톡 데이터입니다.

## Developers
* [Seoyoung Hong](https://github.com/seoyoungh) from Kyunghee Univ.
* [Midan Shim](https://github.com/midannii) from Kyunghee Univ.
