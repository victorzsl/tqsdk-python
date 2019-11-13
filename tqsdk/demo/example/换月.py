# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'vz, zhao shengli'


from datetime import datetime,date
from tqsdk import TqApi,TqAccount, TargetPosTask,TqSim, BacktestFinished, TqBacktest


### 本程序解决回测/实盘过程的换月问题 ###


acc = TqSim()
api = TqApi(acc, backtest=TqBacktest(start_dt=date(2016, 1, 1), end_dt=date(2019, 10, 1)))

SYMBOL_ZhuLian="KQ.m@CFFEX.IF"

quote = api.get_quote(SYMBOL_ZhuLian)
now = datetime.strptime(quote.datetime, "%Y-%m-%d %H:%M:%S.%f") 
symbol_underlying=quote.underlying_symbol

#自定义换月规则
yue=int(now.month/3+1)*3    #根据需要修改代码,此示例为03，06，09，12季月
if yue==15:
    huanyue=str(now.year+1)[2:]+"03"
else:
    huanyue=str(now.year)[2:]+"0"+str(yue) if yue<10 else str(now.year)[2:]+str(yue)

SYMBOL=SYMBOL_ZhuLian[5:]+huanyue
print("当前月",now.month,", 换月",huanyue,", 合约",SYMBOL,"\n" )        
quote = api.get_quote(SYMBOL)
now = datetime.strptime(quote.datetime, "%Y-%m-%d %H:%M:%S.%f")     
lastmonth = now.month

klinesH1 = api.get_kline_serial(SYMBOL, 3600,data_length =4)  # 86400: 使用M1线
position = api.get_position(SYMBOL)
target_pos = TargetPosTask(api, SYMBOL)

print("连续合约",SYMBOL_ZhuLian,"  合约",SYMBOL,"  quote.underlying_symbol",symbol_underlying,"  策略开始运行!\n")


def huanYue():
    global lastmonth,quote,now,klinesH1,position,target_pos
    if True:
        target_pos.set_target_volume(0) 
        
        #自定义换月规则
        yue=int(now.month/3+1)*3     #根据需要修改代码,此示例为03，06，09，12季月
        if yue==15:
            huanyue=str(now.year+1)[2:]+"03"
        else:
            huanyue=str(now.year)[2:]+"0"+str(yue) if yue<10 else str(now.year)[2:]+str(yue)

        SYMBOL=SYMBOL_ZhuLian[5:]+huanyue
        print("当前月",now.month,", 换月",huanyue,", 合约",SYMBOL,"\n" )        
        quote = api.get_quote(SYMBOL)
        now = datetime.strptime(quote.datetime, "%Y-%m-%d %H:%M:%S.%f") 
        lastmonth = now.month

        klinesH1 = api.get_kline_serial(SYMBOL, 3600,data_length =4)  #
        position = api.get_position(SYMBOL)
        lot = position.pos_long - position.pos_short # 净目标净持仓数
        target_pos = TargetPosTask(api, SYMBOL)


while True:
    api.wait_update()
    if api.is_changing(klinesH1.iloc[-1], "datetime"):  # 产生新k线,则重新计算指标线
        now = datetime.strptime(quote.datetime, "%Y-%m-%d %H:%M:%S.%f") 
        if now.month != lastmonth:
            huanYue()




