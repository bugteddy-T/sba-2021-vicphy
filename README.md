# OGAM X SEOUL
[SBA]SW기초 역량 아카데미 빅데이터 2팀 프로젝트

오늘의 감정에 따라 서울 여행지를 추천.

## 오감(OGAM)이란?
오늘의 감성(또는 감정)의 줄임말, 오감(다섯가지 감각(시각, 청각, 후각, 미각, 촉각), 여행을 할 때 느끼는 감각) -> 중의적 단어.

## 기획
"오늘의 감정에 따라 여행지를 추천합니다."

어제의 평가가 아닌 오늘의 감정에 따라 여행지를 추천

### 기획의도
같은 여행지라도 어떤 감정인가에 따라 다르게 느껴지기 때문.

어떤 감정인가에 따라 가고 싶은 곳이 달라짐.

### 어떤 추천 시스템을 왜 사용했는가?

협업 필터링이 아닌 콘텐츠 기반 필터링을 사용.

협업 필터링(왓챠가 영화를 추천할 때 주로 쓰는 방식)의 경우 과거 좋았던 여행지 기준으로 추천한다면 매번 비슷한 여행지가 추천될 수밖에 없음.
영화는 전에 본 영화를 기반으로 평가해도 괜찮음. 영화는 계속 늘어남. 여행지는 영화나 웹툰, 책처럼 빠른 속도로 늘어날 수 없음.

## 서비스 구현

### 오늘의 감정을 어떻게 알 수 있는가?

사용자에게 마음에 드는 사진을 고르게 해서, 사진에 담긴 느낌을 바탕으로 여행지를 추천.

사용자는 그날 그날 감정이나 욕구에 따라 다른 사진을 고르게 됨. 매번 다른 여행지를 추천받을 수 있게 됨.

### 실제 구현 방법

각 사진에는 태그와 가중치 값이 저장되어 있음.

사진을 3개 선택하면 태그와 가중치 값이 합산되어 상위 5개 태그와 가중치 값을 얻게 됨.

예) {'역사': 8, '유익하다': 8, '힐링': 8, '박물관': 5, '관광지': 5}

이 태그값을 바탕으로 가상의 장소를 설정. 가상의 장소와 유사한 여행지를 추천해 줌.

추천 결과: 서대문 형무소 역사관, 강남스타일 말춤 무대, 충무공 이순신 동상, 숭례문, 문화역서울 284, 종묘, 동대문, 동대문 디자인 플라자, 영등포 중앙시장, 환기 미술관을 추천.

## 구현 화면

첫화면
<img src="https://github.com/jeongyedong/sba-bigdata-team2/blog/main/backup/web-page-screenshots/index.png" width="800"> 

사진 선택 화면
<img src="https://github.com/jeongyedong/sba-bigdata-team2/blog/main/backup/web-page-screenshots/select.png" width="800">

사진을 선택한 상태
<img src="https://github.com/jeongyedong/sba-bigdata-team2/blog/main/backup/web-page-screenshots/select-photos.png" width="800">

여행 유형
<img src="https://github.com/jeongyedong/sba-bigdata-team2/blog/main/backup/web-page-screenshots/type.png" width="800">

결과
<img src="https://github.com/jeongyedong/sba-bigdata-team2/blog/main/backup/web-page-screenshots/result.png" width="800">

장소 지도에 표시
<img src="https://github.com/jeongyedong/sba-bigdata-team2/blog/main/backup/web-page-screenshots/place.png" width="800">
