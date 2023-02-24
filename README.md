# python_stock
 파이썬 주식 자동 거래기 (수동 설정 가격에 따라, 저렴할 때 사고 비쌀 때 판다.)

## 기반 프로그램
1. [아나콘다](https://www.anaconda.com/products/distribution)
2. [키움증권 api](), [참고](https://wikidocs.net/85553)
- pykiwoom api는 32bit 환경으로 설정해 둔 후 설치해야 한다.
`{bash}
 set CONDA_FORCE_32BIT=1
 pip install pykiwoom
`


## 원칙 (알고리즘?)

1. 시세와 원하는 매수가, 매도가와 비교한다.
2. 만약 원하는 가격을 넘는다면, 설정한 갯수 만큼 매수/매도 한다.
3. 단 매수는 구매할 시 예수금이 -로 될 경우, 매수하지 않는다(미수 거래 방지). 매도도 마찬가지로 주식이 없을 시, 매도하지 않는다.
4. 종목, 가격, 갯수를 설정할 수 있는 원격 Interface가 존재한다. (웹이나 앱, 디스코드 봇 등.)
5. 각 주식마다 매수 매도 시간 다름. (가격에 따라 거래 빈도 달라짐. ex. 목표 고가일 수록 빨리 매도)
6. 주식 매수에는 제한을 걸어둠. (몇 주까지, 혹은 몇원까지 최대 매수 제한)
7. 일단 지금은 config.json에 설정 저장한다. (불편할 경우 데이터베이스로 전환 예정.)

+ 1. 작동하고 있다고 주기적으로 알림 오도록해놓기?
+ 2. 매도가 도달하면 알림 오기? (on/off 가능)

## 디스코드
디스코드로 매수/매도 설정값을 변경한다.
- discord_boy.py와 같은 위치에 discord_bot_token.json 파일을 만들고, 아래 예시처럼 token 값을 담아 저장해주어야 한다. 
`{json}
    {"token": "토큰값"}
`
- 채팅 말고, 선택 등 ui가 존재하는 주문으로 해야 좋을 듯? [이것 참고](https://pypi.org/project/discord-ui/)
- nodejs로 하는게 나을지도? [이것 참고](https://discordjs.guide/)