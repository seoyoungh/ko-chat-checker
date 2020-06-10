# Week 10

## Finished Works
### 1. Edit distance 성능 평가
- 전체적으로 잘 찾아내지만 한계 있음
- good case
![ed_result_good](/assets/images/ed_result_good.png)
- bad case
![ed_result_bad](/assets/images/ed_result_bad.png)

### 2. Seq2Seq 채택 & base 구축
- Encoder, Decoder: LSTM
- hyperparameters 조정, attention 적용 등 Seq2Seq의 성능을 높이는 방향으로 갈 예정
- performance:
  - non-padded: | Test Loss: 1.271 | Test PPL: 3.565 |
  - padded: | Test Loss: 0.780 | Test PPL: 2.181 |
- cf) PPL은 이 언어 모델이 특정 시점에서 평균적으로 몇 개의 선택지를 가지고 고민하고 있는지를 의미
- decoder의 output (prediction 결과)와 실제 label을 비교해보고 싶은데 함수 define 과정에서 자꾸 error 발생 -> 해결예정

```
Epoch: 01 | Time: 0m 6s
	Train Loss: 2.455 | Train PPL:  11.642
	 Val. Loss: 1.971 |  Val. PPL:   7.177
Epoch: 02 | Time: 0m 6s
	Train Loss: 1.893 | Train PPL:   6.640
	 Val. Loss: 1.942 |  Val. PPL:   6.969
Epoch: 03 | Time: 0m 6s
	Train Loss: 1.828 | Train PPL:   6.219
	 Val. Loss: 1.913 |  Val. PPL:   6.774
Epoch: 04 | Time: 0m 6s
	Train Loss: 1.704 | Train PPL:   5.496
	 Val. Loss: 1.766 |  Val. PPL:   5.845
Epoch: 05 | Time: 0m 6s
	Train Loss: 1.581 | Train PPL:   4.860
	 Val. Loss: 1.635 |  Val. PPL:   5.131
Epoch: 06 | Time: 0m 6s
	Train Loss: 1.453 | Train PPL:   4.278
	 Val. Loss: 1.565 |  Val. PPL:   4.782
Epoch: 07 | Time: 0m 6s
	Train Loss: 1.307 | Train PPL:   3.695
	 Val. Loss: 1.399 |  Val. PPL:   4.053
Epoch: 08 | Time: 0m 6s
	Train Loss: 1.178 | Train PPL:   3.247
	 Val. Loss: 1.298 |  Val. PPL:   3.662
Epoch: 09 | Time: 0m 6s
	Train Loss: 1.061 | Train PPL:   2.889
	 Val. Loss: 1.310 |  Val. PPL:   3.708
Epoch: 10 | Time: 0m 6s
	Train Loss: 0.953 | Train PPL:   2.593
	 Val. Loss: 1.154 |  Val. PPL:   3.170
Epoch: 11 | Time: 0m 6s
	Train Loss: 0.876 | Train PPL:   2.402
	 Val. Loss: 1.059 |  Val. PPL:   2.885
Epoch: 12 | Time: 0m 6s
	Train Loss: 0.752 | Train PPL:   2.121
	 Val. Loss: 1.016 |  Val. PPL:   2.762
Epoch: 13 | Time: 0m 6s
	Train Loss: 0.655 | Train PPL:   1.925
	 Val. Loss: 0.987 |  Val. PPL:   2.683
Epoch: 14 | Time: 0m 6s
	Train Loss: 0.564 | Train PPL:   1.758
	 Val. Loss: 0.940 |  Val. PPL:   2.560
Epoch: 15 | Time: 0m 6s
	Train Loss: 0.478 | Train PPL:   1.613
	 Val. Loss: 0.896 |  Val. PPL:   2.449
Epoch: 16 | Time: 0m 6s
	Train Loss: 0.407 | Train PPL:   1.503
	 Val. Loss: 0.889 |  Val. PPL:   2.433
Epoch: 17 | Time: 0m 6s
	Train Loss: 0.341 | Train PPL:   1.406
	 Val. Loss: 0.846 |  Val. PPL:   2.331
Epoch: 18 | Time: 0m 6s
	Train Loss: 0.279 | Train PPL:   1.321
	 Val. Loss: 0.818 |  Val. PPL:   2.267
Epoch: 19 | Time: 0m 6s
	Train Loss: 0.238 | Train PPL:   1.269
	 Val. Loss: 0.833 |  Val. PPL:   2.301
Epoch: 20 | Time: 0m 6s
	Train Loss: 0.188 | Train PPL:   1.207
	 Val. Loss: 0.843 |  Val. PPL:   2.323
```

### 3. Padding 성능
- 종성 padding 부여
- e.g.) text: ``ㅈㅓP/ㄱㅣP/ㅇㅛㅁ``	label: ``ㅈㅓP/ㄱㅣP/ㅇㅛP``

### 4. Case 일반화
- 데이터가 작기 때문에 모델에게 정보를 더 부여해 성능을 높일 계획
- 표기 오류에 rule이 아예 없는 것은 아님, 그 rule을 발견할 수 있도록
- sequence의 대부분이 같고 특정 부분만 변함
- text와 label의 length가 같은 case가 많음 (padding 포함)
  - 같은 경우: 2308, 다른 경우: 339

1) 같은 부분은 'S'로 바꾸고 다른 부분만 특정해 비교
2) 초성:1, 중성 2, 종성:3으로 라벨링

```
trained:
(ㅇㅐㄱㅇㅣP) (ㅇㅐPㄱㅣP)
(SSㄱㅇSS) (SSSㄱSS)
3 - 'ㄱ' 1 - 'ㅇ' -> 3 - 'P' 1 - 'ㄱ'

can predict:
(ㅈㅓㄱㅇㅣP)(ㅈㅓPㄱㅣP)
(SSㄱㅇSS) (SSSㄱSS)

trained:
(ㅇㅏㄹㅇㅏㅅㄴㅔP)(ㅇㅏㄹㅇㅏㅆㄴㅔP)
(SSSSSㅅSSS)(SSSSSㅆSSS)
3 - 'ㅅ' -> 3 - 'ㅆ'

can predict:
(ㅁㅓㄱㅇㅓㅅㄴㅔ)(ㅁㅓㄱㅇㅓㅆㄴㅔ)
(ㅁㅓㄱㅇㅓㅅㄴㅣ)(ㅁㅓㄱㅇㅓㅆㄴㅣ)
```

### 5. 기타 이슈
- CharCNN, ELMo -> 주로 text classification에 사용, 결이 달라서 기각
- BERT는 모델 자체가 큼, 우리 데이터는 비교적 작아서 일단 차선책으로 보류
- FastText: 한국어 임베딩 관련해 모델 자체 오류 있어서 사용 어려움, 계속 research 중

### 6. Model Outline

1. 데이터 대조
- 우리 labelled 데이터에서 커버할 수 있는지

2-1. Text similarity
- edit distance
- (fasttext)

2-2. Prediction
- Seq2Seq

3. 최종 결과
