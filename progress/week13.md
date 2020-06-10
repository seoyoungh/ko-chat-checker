# Week 13
## 모델 예측과 edit distance 예측 비교
- 모델과 edit distance의 결과가 같은 경우
  - max distance = 0.4
    - 1451/2432
  - max distance = 0.8
    - 1725/2432
- 모델과 edit distance의 결과가 다른 경우 (max distance = 0.8)
  - 1) 모델이 맞은 경우
    - 477/707
  - 2) edit distance의 결과가 없었던 경우
    - 414/707
  - 3) edit distance가 맞은 경우
    - 79/293
  - 1), 3)간의 교집합이 없다.
  - 3)의 경우, 모델 예측에서 표준어 dataset에 없었던, 말이 되지 않는 output이 59개
    - e.g.) 찾아봐야자, 그랬, 교수님힘, 아버지가가, 신김해, 안들어가가서고

## 최종 model workflow
- 모델과 edit distance의 결과가 같은 경우
  - no problem!
  - max distance = 0.4로 설정
- 모델과 edit distance의 결과가 다른 경우
  - edit distance output이 없는 경우
    - model output return
  - model output이 original text와 같은 경우
    - edit distance output return
  - 둘 다 결과가 있는데 다른 경우
    - model output이 표준어 데이터셋에 있는 경우, model output return
    - 아닌 경우, edit distance output return

# 배포, Github 구축 완료
- https://github.com/seoyoungh/ko-chat-checker

```python
pip install chatchecker
from chatchecker import ChatChecker
```
