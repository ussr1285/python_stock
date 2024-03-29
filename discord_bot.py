#!/usr/bin/env python
# -*- coding: utf-8 -*-

# discord bot (stock.py와 따로 동작.)
import os
import time
import json
import nest_asyncio 
import discord
from discord.ext import commands
from pykrx import stock

def load_json_config(stock_code): # 해당 주식이 어떤 설정을 했는지 stock_order_configs 폴더에 있는 파일들에서 가져와서, 주식 객체 만들어줌.
    with open("./stock_order_configs/"+stock_code+".json", "r") as json_file:
        json_data = json.load(json_file)
    return json_data

def load_json_configs():
    dirname = "./stock_order_configs" # 경로
    filenames = os.listdir(dirname)
    json_data_arr = []

    for file in filenames:
        with open("./stock_order_configs/"+file, "r") as json_file:
            json_data = json.load(json_file)
        json_data_arr.append(json_data)
    return json_data_arr

def save_json_config(stock_code, stock_name, max_stock_amount, will_buy, target_buy_price, buy_amount, buy_frequency_time, will_sell, target_sell_price, sell_amount, sell_frequency_time): # 각 주식에 수정 사항 있는데로 파일 저장.
    stock_object = {
        "stock_code" : stock_code,
        "stock_name" : stock_name,
        "max_stock_amount" : max_stock_amount,
        "will_buy" : will_buy,
        "target_buy_price" : target_buy_price,
        "buy_amount" : buy_amount,
        "buy_frequency_time" : buy_frequency_time,
        "will_sell" : will_sell,
        "target_sell_price" : target_sell_price,
        "sell_amount" : sell_amount,
        "sell_frequency_time" : sell_frequency_time,
    }
    with open("./stock_order_configs/"+stock_code+".json", "w") as json_file:
        json.dump(stock_object, json_file)

nest_asyncio.apply()

with open("./discord_bot_token.json", "r") as json_file:
    json_data = json.load(json_file)
token = json_data['token']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.command()
async def 도움말(ctx):
    await ctx.send('-----사용방법 알려주는 내용-----\n'+'점(.)을 메시지 맨 앞에 찍음으로써 명령어를 사용합니다.\n'+'   ex) .도움말\n'+'1. 주식 종목 추가/초기화하는 방법\n'+'.주식설정 (종목코드) (종목명) (최대매수한도) (목표매수주가) (매수개수) (매수시간간격) (목표매도주가) (매도주식개수) (매도시간간격)\n'+'   ex) .주식설정 042110 3500 0 1 60 5210 1 60\n'+'2. 최대 매수 개수\n'+'    ex) .최대매수개수 100\n'+'3. 매수 작동 on/off\n'+'    ex) .매수작동\n'+'4. 매수할 가격\n'+'    ex) .매수가격 55000\n'+'5. 거래마다 매수할 주식 개수\n'+'    ex) .매수개수 1\n'+'6. 매수 시간 간격(초 단위)\n'+'  ex) .매수시간간격 60\n'+'7. 매도 작동 on/off\n'+'   ex) .매도작동\n'+'8. 매도가격\n'+' ex) .매도가격 70000\n'+'9.거래마다 매수할 주식 개수\n'+'    ex) .매도개수 1\n'+'10. 매도 시간 간격(초 단위)\n'+'   ex) .매도시간간격 60\n') # 사용방법 알려주는 help


@bot.command()
async def 주식현황(ctx, stock_code='0'): # 주식 매수/매도 설정, 현황 확인
    if(stock_code == '0'):
        stocks = load_json_configs()
        for stock in stocks:
            await ctx.send("--------------\n"+"종목코드: "+ stock['stock_code']+ "\n종목명: "+ stock['stock_name'] +"\n최대 한도 매수 주식 개수: "+ str(stock['max_stock_amount'])+ "\n매수 자동화 작동: "+ str(stock['will_buy'])+ "\n목표 매수 주가: "+ str(stock['target_buy_price'])+ "\n매수할 개수: "+ str(stock['buy_amount'])+ "\n매수할 시간 간격: "+ str(stock['buy_frequency_time'])+ "\n매도 자동화 작동: "+ str(stock['will_sell'])+ "\n목표 매도 주가: "+ str(stock['target_sell_price'])+ "\n매도할 주식 개수: "+ str(stock['sell_amount'])+ "\n매도할 시간 간격: "+ str(stock['sell_frequency_time'])+ "\n--------------")
    else:
        origin = load_json_config(stock_code)
        await ctx.send("--------------\n"+"종목코드: "+ origin['stock_code']+ "\n종목명: "+ origin['stock_name'] +"\n최대 한도 매수 주식 개수: "+ str(origin['max_stock_amount'])+ "\n매수 자동화 작동: "+ str(origin['will_buy'])+ "\n목표 매수 주가: "+ str(origin['target_buy_price'])+ "\n매수할 개수: "+ str(origin['buy_amount'])+ "\n매수할 시간 간격: "+ str(origin['buy_frequency_time'])+ "\n매도 자동화 작동: "+ str(origin['will_sell'])+ "\n목표 매도 주가: "+ str(origin['target_sell_price'])+ "\n매도할 주식 개수: "+ str(origin['sell_amount'])+ "\n매도할 시간 간격: "+ str(origin['sell_frequency_time'])+ "\n--------------")
    
    
@bot.command()
async def 주식설정(ctx, stock_code, max_stock_amount, target_buy_price, buy_amount, buy_frequency_time, target_sell_price, sell_amount, sell_frequency_time):
    stock_name = stock.get_market_ticker_name(stock_code)
    will_buy = True
    will_sell = True
    save_json_config(stock_code, stock_name, max_stock_amount, will_buy, target_buy_price, buy_amount, buy_frequency_time, will_sell, target_sell_price, sell_amount, sell_frequency_time)
    await ctx.send(stock_name+'('+stock_code + ')에 대한 주식 매매 설정 완료.')

@bot.command()
async def 최대매수개수(ctx, stock_code, max_stock_amount):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], max_stock_amount, origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("최대 한도 매수 주식 개수: ", max_stock_amount)

@bot.command()
async def 매수작동(ctx, stock_code):
    origin = load_json_config(stock_code)
    if(origin['will_buy'] == True):
        origin['will_buy'] = False
    else:
        origin['will_buy'] = True
    save_json_config(origin['stock_code'], origin['max_stock_amount'], will_buy, origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("매수 자동화 작동: ", origin['will_buy'])

@bot.command()
async def 매수가격(ctx, stock_code, target_buy_price):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], target_buy_price, origin['buy_amount'], origin['buy_frequency_time'], origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("목표 매수 주가: ", target_buy_price)

@bot.command()
async def 매수개수(ctx, stock_code, buy_amount):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], buy_amount, origin['buy_frequency_time'], origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("매수할 개수: ", buy_amount)

@bot.command()
async def 매수시간간격(ctx, stock_code, buy_frequency_time):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], buy_frequency_time, origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("매수할 시간 간격: ", buy_frequency_time)

@bot.command()
async def 매도작동(ctx, stock_code):
    origin = load_json_config(stock_code)
    if(origin['will_sell'] == True):
        origin['will_sell'] = False
    else:
        origin['will_sell'] = True

    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], will_sell, origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("매도 자동화 작동: ", origin['will_sell'])

@bot.command()
async def 매도가격(ctx, stock_code, target_sell_price):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], origin['will_sell'], target_sell_price, origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send("목표 매도 주가: ", target_sell_price)

@bot.command()
async def 매도개수(ctx, stock_code, sell_amount):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], origin['will_sell'], origin['target_sell_price'], sell_amount, origin['sell_frequency_time'])
    await ctx.send("매도할 주식 개수: ", sell_amount)

@bot.command()
async def 매도시간간격(ctx, stock_code, sell_frequency_time):
    origin = load_json_config(stock_code)
    save_json_config(origin['stock_code'], origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], sell_frequency_time)
    await ctx.send("매도할 시간 간격: ", sell_frequency_time)

@bot.command()
async def buy(ctx, stock_code, max_stock_amount, will_buy, target_buy_price, buy_amount, buy_frequency_time): # 매수 설정
    origin = load_json_config(stock_code)
    save_json_config(stock_code, max_stock_amount, will_buy, target_buy_price, buy_amount, buy_frequency_time, origin['will_sell'], origin['target_sell_price'], origin['sell_amount'], origin['sell_frequency_time'])
    await ctx.send('매수 설정하는 코드')

@bot.command()
async def sell(ctx, stock_code, will_sell, target_sell_price, sell_amount, sell_frequency_time): # 매도 설정
    origin = load_json_config(stock_code)
    save_json_config(stock_code, origin['max_stock_amount'], origin['will_buy'], origin['target_buy_price'], origin['buy_amount'], origin['buy_frequency_time'], will_sell, target_sell_price, sell_amount, sell_frequency_time)
    await ctx.send('매도 설정하는 코드')


bot.run(token)