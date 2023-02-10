# 프로그램 코드 (키움 증권 연동)
from pykiwoom.kiwoom import *

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)

# 프로그램 코드 (초기값 및 함수 정의)

# 계좌번호
account_list = kiwoom.GetLoginInfo("ACCNO")
account = account_list[0]

print(account)
print(kiwoom.GetConnectState())

def get_wallet(): # 예수금 확인 함수
    # opw00001 요청
    wallet_df = kiwoom.block_request("opw00001",
        계좌번호=account,
        비밀번호="",
        비밀번호입력매체구분="00",
        조회구분=2,
        output="예수금상세현황",
        next=0
    )
    print(wallet_df['예수금'][0]) # 에러 확인
    money = int(wallet_df['예수금'][0])
    return money

def get_stock_price(stock_code): # 주식 현재가 확인 함수
    stock_df = kiwoom.block_request("opt10001",
        종목코드=stock_code,
        output="주식기본정보",
        next=0
    )
    print(stock_df['현재가']) # 에러 확인
    price = int(stock_df['현재가'])
    return price
    
def buy_stock(stock_code, target_price, how_many_amount, wallet): # 주식 매수 함수
    stock_price = get_stock_price(stock_code)
    if((wallet >= stock_price*how_many_amount) and (stock_price <= target_price)):
        # 시장가주문 매수
        kiwoom.SendOrder("시장가매수", "0101", account, 1, stock_code, how_many_amount, 0, "03", "")

def sell_stock(stock_code, target_price, how_many_amount, stock_amount): # 주식 매도 함수
    # 시장가주문 매도
    kiwoom.SendOrder("시장가매도", "0101", account, 2, stock_code, how_many_amount, 0, "03", "")

def trade_function(stock_code): # 거래 결정 함수 (이걸 계속 돌리면 될 듯.)
    wallet = get_wallet()
    # stock_amount = 


# 프로그램 코드 (테스트)
stock_code = "038500"
how_many_amount = 1
wallet = get_wallet()
target_price = 3700

buy_stock(stock_code, target_price, how_many_amount, wallet)