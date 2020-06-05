# Week 12

## Finished Works
1) 최종 모델 accuracy
   - test accuracy
     - 400/486
     - **82.3%**
   - train accuracy
     - 8753/9284
     - **94.3%**
   - n-gram 제외 전체 데이터
     - 2171/2432
     - **89.3%**
   - n-gram 포함 전체 데이터
     - 9476/10159
     - **93.3%**

2) ``gensim``의 ``Dictionary`` 활용해 표기 오류가 있는 단어 빠르게 찾도록 개선

- 맞춤법 검사 대신 대화체 데이터셋에 있는지 여부 체크

![searching_time](/assets/images/searching_time.png)

3) 코드 모듈화

```python
# import custom package

import CustomModel # seq2seq module
from EditDistance import * # editdistance module
from Utils import * # other functions

def main():
  text = spacer("이짜나, 햇졍! 밥머것어! 배고픈뎅@ 머행 😌!") # input, 띄어쓰기
  text_list = tokenizer(text) # spacing 단위로 문장 나누
  id_list, wrong_list = check_error(text_list) # 표기 오류 찾기
  fianl_wrong, pceq = clean_w_pceq(id_list, text_list) # 특수문자 제거 but .,!?는 index 기억했다가 표기 교정 후 다시 붙여줌
  seq = seq2seq(wrong_list) # custom model 교정 결과
  edit = editdistance(wrong_list) # edit distance 교정 결과
  corrected = compare(seq, edit) # 이부분이 아직 미완
  output = correct(text_list, id_list, corrected, pceq) # 교정한 단어, .,!? 문장에 넣어주기
  final_output = spacer(sum(output)) # 최종 띄어쓰기
  return final_output # 최종 교정 문장 리턴
```

* 예시
![example](/assets/images/example.png)

## To Do
1) 코드 workflow 확정
  - if ``model output`` in ``edit_list``: # 같은 경우
    - 같은 output 리턴
  - elif ``model == None`` && ``edit == None``: # 모델 X edit X
    - 원래 텍스트 리턴
  - elif ``model == None`` && ``edit == [...]``: # 모델 X edit O
    - edit output 리턴
  - elif ``model == "..."`` && ``edit == None``: # 모델 O edit X
    - model output 리
  - **``model output`` not in ``edit_list``:**
    - 세가지 케이스 정확도 비교해서 예측 알고리즘 확정하기
          1) 그냥 모델 아웃풋 리턴
          2) 모델 output의 edit distance가 일정 수준 이하이면 edit output 리턴
          3) 모델 output의 edit distance가 edit output보다 크면 edit output 리턴

2) 코드 패키지화
  - ``pip``활용해 배포할 계획

3) 결과 보고서 작성
