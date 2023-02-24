# 프로그램 코드 (키움 증권 연동)
from pykiwoom.kiwoom import *
import time
import json
import os

# 로그인
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True) # 지속적으로 연결이 안되는건가? 주식 거래 체결하고나면 다시 거래 안되고, 이것 다시 실행해서 제연결해주면 됨.

# 계좌번호
account = kiwoom.GetLoginInfo("ACCNO")[0]

print(account)
print(kiwoom.GetConnectState())

# 프로그램 코드 (초기값 및 함수 정의)

def time_distance(input_time):
    return time.time() - input_time

def get_stock_price(stock_code): # 주식 현재가 확인 함수
    kiwoom.CommConnect(block=True)
    stock_df = kiwoom.block_request("opt10001",
        종목코드=stock_code,
        output="주식기본정보",
        next=0
    )
    return abs(int(stock_df['현재가'])) # 하락하고 있으면 음수로 반환해서 abs함수로 절대값으로 만듬.

def get_wallet(): # 주문 가능 금액(예수금) 확인 함수
    kiwoom.CommConnect(block=True)
    # opw00001 요청
    wallet_df = kiwoom.block_request("opw00001",
        계좌번호=account,
        비밀번호="",
        비밀번호입력매체구분="00",
        조회구분=2,
        output="예수금상세현황",
        next=0
    )
    money = int(wallet_df['주문가능금액'][0])
    return money

class Stock():
    def __init__(self, stock_code, max_stock_amount, target_buy_price, buy_amount, buy_frequency_time, target_sell_price, sell_amount, sell_frequency_time):
        self.stock_code = stock_code # 주식 주문 코드
        self.stock_price = get_stock_price(self.stock_code) # 주식 현재가

        self.stock_amount = self.get_stock_amount() # 보유 주식 수.
        self.max_stock_amount = max_stock_amount # 최대 매수 가능한 주식 수, 여기에 도달하면 더 이상 매수 안 함.

        self.will_buy = True # 매수 희망 유무
        self.target_buy_price = target_buy_price # 목표로 하는 매수가. 이것보다 현재가가 싸면 매수.
        self.buy_amount = buy_amount # 매수를 할 주식 개수

        self.buy_frequency_time = buy_frequency_time # 초 단위
        self.buy_last_time = time.time()
        
        self.will_sell = True # 매도 희망 유무
        self.target_sell_price = target_sell_price # 목표로 하는 매도가. 이것보다 현재가가 비싸면 매도.
        self.sell_amount = sell_amount # 매도를 할 주식 개수
        self.sell_frequency_time = sell_frequency_time # 초 단위
        self.sell_last_time = time.time()
        print(self.stock_code, "주식 객체 생성 완료.")

    def get_stock_amount(self):
        kiwoom.CommConnect(block=True)
        stock_df = kiwoom.block_request("opw00004",
            계좌번호=account,
            비밀번호="",
            상장폐지조회구분="0",
            비밀번호입력매체구분="00",
            output="주식기본정보",
            next=0
        )
        if(stock_df['종목코드'].str.contains(self.stock_code)[0]):
            target_stock = stock_df[stock_df['종목코드'].str.contains(self.stock_code)] # 종목코드에 해당하는 데이터 행 찾기.
            return int(target_stock['보유수량'])
        else:
            return 0

    def buy_stock(self): # 주식 매수 함수
        wallet = get_wallet()
        stock_price = get_stock_price(self.stock_code)
        if(
            wallet >= stock_price*self.buy_amount 
            and stock_price <= self.target_buy_price
            and time_distance(self.buy_last_time) >= self.buy_frequency_time
        ):
            kiwoom.CommConnect(block=True)
            if(self.max_stock_amount < self.stock_amount + self.buy_amount): # 매수를 하고 싶은데 주식 최대 보유량을 초과한다면 어떻게 할 것인가?에 관한 조건문
                temp_amount = (self.stock_amount + self.buy_amount) - self.max_stock_amount 
                if(temp_amount > 0):
                    kiwoom.SendOrder("시장가매수", "0101", account, 1, self.stock_code, temp_amount, 0, "03", "") # 시장가주문 매수
                    self.buy_last_time = time.time()
            else:
                kiwoom.SendOrder("시장가매수", "0101", account, 1, self.stock_code, self.buy_amount, 0, "03", "") # 시장가주문 매수
                self.buy_last_time = time.time()
            print(self.stock_code, "매수")
            
    def sell_stock(self): # 주식 매도 함수
        stock_price = get_stock_price(self.stock_code)
        if(
            stock_price >= self.target_sell_price
            and time_distance(self.sell_last_time) >= self.sell_frequency_time
        ):
            kiwoom.CommConnect(block=True)
            if(self.stock_amount < self.sell_amount):
                if(self.stock_amount > 0):
                    kiwoom.SendOrder("시장가매도", "0101", account, 2, self.stock_code, self.stock_amount, 0, "03", "") # 시장가주문 매도
                    self.sell_last_time = time.time()
            else:
                kiwoom.SendOrder("시장가매도", "0101", account, 2, self.stock_code, self.sell_amount, 0, "03", "") # 시장가주문 매도
                self.sell_last_time = time.time()
            print(self.stock_code, "매도")

def load_json_configs(): # 각 주식별로 어떤 설정을 했는지 stock_order_configs 폴더에 있는 파일들에서 가져와서, 주식 객체 만들어줌.
    stocks = []

    dirname = "./stock_order_configs" # 경로
    filenames = os.listdir(dirname)

    for file in filenames:
        with open("./stock_order_configs/"+file, "r") as json_file:
            json_data = json.load(json_file)
        stocks.append(
            Stock(
                json_data['stock_code'],
                json_data['max_stock_amount'],
                json_data['target_buy_price'],
                json_data['buy_amount'],
                json_data['buy_frequency_time'],
                json_data['target_sell_price'],
                json_data['sell_amount'],
                json_data['sell_frequency_time']
            )
        )
    return stocks

'''
def save_json_configs(stocks): # 각 주식에 수정 사항 있는데로 파일 저장.
    for stock in stocks:
        save_json_config(stock)

def save_json_config(stock): # 각 주식에 수정 사항 있는데로 파일 저장.
    stock_object = {
        "stock_code" : stock.stock_code,
        "max_stock_amount" : stock.max_stock_amount,
        "will_buy" : stock.will_buy,
        "target_buy_price" : stock.target_buy_price,
        "buy_amount" : stock.buy_amount,
        "buy_frequency_time" : stock.buy_frequency_time,
        "will_sell" : stock.will_sell,
        "target_sell_price" : stock.target_sell_price,
        "sell_amount" : stock.sell_amount,
        "sell_frequency_time" : stock.sell_frequency_time
    }
    with open("./stock_order_configs/"+stock.stock_code+".json", "w") as json_file:
        json.dump(stock_object, json_file)
'''

# def modify_function(stocks):

def trade_function(): # 거래 결정 함수 (이걸 계속 돌린다...!)
    stocks = load_json_configs()
    for stock in stocks:
        stock.buy_stock()
        time.sleep(1)
        stock.sell_stock()
        time.sleep(1)

# 프로그램 코드 (main)
if __name__ == "__main__":
    while(True):
        try:
            trade_function()
        except Exception as error:
            print(error)
    