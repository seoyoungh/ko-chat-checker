# Week 6

## finished work
1. 단어로 분리된 텍스트 데이터 한번 더 전처리
   - 영어, 숫자, 자음(ᄏᄏᄏ,ᄒᄒ,ᅲᅲ) 등 제거
     - [Code](/chat_preprocessing/3_preprocessing.py)


2. 문법 오류 여부에 따라 데이터 분리
   - 맞춤법 검사 opensource
     1. [py-hanspell](https://github.com/ssut/py-hanspell)
         - [네이버 맞춤법 검사 url 변경](https://github.com/ssut/py-hanspell/issues/7)으로 현재 사용 불가
         - [가장 최근 검색되는 url](https://blog.naver.com/PostView.nhn?blogId=duswl0319&logNo=221516903176&parentCategoryNo=&categoryNo=16&viewDate=&isShowPopularPosts=true&from=search)로 코드 수정해보았지만 여전히 Json error 발생
     2. [hunspell-dict-ko](https://github.com/spellcheck-ko/hunspell-dict-ko)
     3. [맞춤법 검사 사이트](https://speller.cs.pusan.ac.kr) 에서 직접 자동화


3. Related work 조사
  - [문자열 데이터에 1D CNN 적용한 case](https://cholol.tistory.com/465)
     - [한국어 text classifiers](https://www.ripublication.com/ijaer18/ijaerv13n4_12.pdf)
     - [어절 단위의 chatbot sentence classifiers](https://www.aclweb.org/anthology/P17-2089.pdf)


## to do
1. 데이터 라벨링
   - 문법 오류가 있는 텍스트 어떻게 라벨링할 것인지?
   
2. 학습에 이용할 데이터 5:5로 분리 
