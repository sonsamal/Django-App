from django.shortcuts import render
from django.http import HttpResponse
from BinanceExchange.models import Binanceexchangeinformation
from .models import Coinlist
from .models import payload
from django.template import loader
import json
import pymysql
##Imports for Binance Modules
from binance.client import Client
from binance.enums import *
from binance import *
##End of Imports for Binance Modules

#Global Data

class viewload:
    panda_data = {}
    panda_rebalance = {}
    key = ''
    secret=''
    main_curreny=''
    quantity = 0.0
    prices = []

pl = viewload()

#End Global Data

def index(request):
    return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/index.html')

def checkBalances(request):
    if 'key' in request.GET and 'secret' in request.GET:
        
        
        client = Client(request.GET['key'],request.GET['secret'])

        pl.key = request.GET['key']
        pl.secret=request.GET['secret']

        if 'portfolio' in request.GET:
            url = request.GET['portfolio']
            if url != '':
                url = url.split('&')
                for item in url:
                    item = item.split('=')
                    pl.panda_data[item[0].upper()] = float(item[1])
        sum = 0.0
        for item in pl.panda_data:
            sum = sum + pl.panda_data[item]

        print(sum)
        
        if sum != 1.0:
            context = {
                'error':'The Portfolio is not a 100% rebalance. Please try again with a different configuration.',
                'backurl':request.META.get('HTTP_REFERER'),
            }
            return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/errorpage.html',context=context)
            
        if pl.panda_data == {}:
            context = {
                'error':'You seem to have entered a text that cannot be parsed',
                'backurl':request.META.get('HTTP_REFERER'),
            }
            return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/errorpage.html',context=context)

        try:
            Account_info = client.get_account()
        except:
            context={
                'error':'You seem to have entered either a wrong API Key or a wrong API secret.',
                'backurl':request.META.get('HTTP_REFERER')
            }
            return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/errorpage.html',context=context)


        pl.prices = client.get_all_tickers()
        
        balance = []
        for item in Account_info['balances']:
            if float(item['free']) > 0.0:
                balance.append(item)
        print(balance)

        balance_selection = []
        for item in balance:
            if item['asset'] == 'BTC' or item['asset'] == 'ETH':
                balance_selection.append(item)
        
        context = {
            'balance':balance,
            'balance_selection':balance_selection,
        }
        return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/balanceandbuy.html',context=context)

def marketPlace(request):
    if 'currency' in request.GET and 'quantity' in request.GET:
        currency = str(request.GET['currency'])
        quantity = request.GET['quantity']

        currency = currency.replace("'",'"')
        currency = json.loads(currency)
        
        if not float(quantity):
            context={
                'error':'You have not entered a number as the quantity you want to trade. Please enter a number',
                'backurl':request.META.get('HTTP_REFERER'),
            }
            return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/errorpage.html',context=context)

        if float(quantity) > float(currency['free']):
            print("YooHoo!")
            print(request.META.get('HTTP_REFERER'))
            context = {
                'error':'You have entered a selling quantity that is higher than what is available in your basket. Please change the amount.',
                'backurl':request.META.get('HTTP_REFERER'),
            }
            return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/errorpage.html',context=context)
        else:
            
            #panda_rebalance = {}
            
            currency = request.GET['currency']
            currency = currency.replace("'",'"')
            currency = json.loads(currency)

            pl.quantity = float(request.GET['quantity'])

            pl.main_curreny = currency['asset']

            for item in pl.panda_data:
                pl.panda_rebalance[item] = []
            
            exchange_record = {}
            del_array = []

            for item in pl.panda_rebalance:

                if item == pl.main_curreny:
                    del_array.append(item)

                result = getPairName(pl.main_curreny,item)

                if result is not None:
                    
                    pl.panda_rebalance[item].append(pl.panda_data[item])

                    for iterable in pl.prices:
                        if iterable['symbol'] == result['symbol']:
                            exchange_record = iterable
                            break
                    
                    print('\n')
                    print(exchange_record)

                    temp = exchange_record['symbol'].split(pl.main_curreny)
                    index = temp.index(item)

                    if index == 1:
                        actual_investment = float(exchange_record['price'])
                        side = SIDE_SELL
                    elif index == 0:
                        actual_investment = 1/(float(exchange_record['price']))
                        side = SIDE_BUY
                    

                    
                    pl.panda_rebalance[item].append(str(pl.panda_data[item]*pl.quantity*actual_investment))
                    pl.panda_rebalance[item].append(str(pl.panda_data[item]*pl.quantity))
                
                    
                    pl.panda_rebalance[item].append(result['symbol'])
                    pl.panda_rebalance[item].append(side)
                
                else:
                    context={
                        'error':'Currency with symbol '+item+' does not exist in Binance. Try another currency',
                        'backurl':request.META.get('HTTP_REFERER'),
                    }
                    return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/errorpage.html',context=context)

            for del_item in del_array:
                if del_item in pl.panda_rebalance:
                    pl.panda_rebalance.pop(del_item)        
                
            print(pl.panda_rebalance)

            context={
                'panda_rebalance':pl.panda_rebalance,
                'backurl':request.META.get('HTTP_REFERER'),
            }
            return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/tradeconfirmation.html',context=context)

def finalsell(request):

    error={}
    success={}

    #print(pl.key)
    
    client = Client(pl.key,pl.secret)

    #prices = client.get_all_tickers()

    #print(pl.panda_rebalance)
    symbols = []
    for item in pl.panda_rebalance:
        result = getPairName(pl.main_curreny,item)

        # print(result)
        # print(pl.main_curreny)

        
        temp = result['symbol'].split(pl.main_curreny)

        symbols.append(result['symbol'])

        index = temp.index(item)

        if index == 0:
            side = SIDE_BUY
        elif index == 1:
            side = SIDE_SELL

        try:

            stepSize = result['stepSize'].split('.')
            if stepSize[0] == '1':
                quantity = round(float(pl.panda_rebalance[item][1]))
            else:
                prec = stepSize[1].index('1')+1
                pre_quant = pl.panda_rebalance[item][1].split('.')
                quantity = float(pre_quant[0]+'.'+pre_quant[1][:prec])

            order=client.create_order(
                symbol=result['symbol'],
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )

            success[item] = ['Transaction Successful',order['orderId']]
            #print(order)
        except:
            try:
                
                if side == SIDE_BUY:
                    side = SIDE_SELL
                elif side == SIDE_SELL:
                    side = SIDE_BUY

                stepSize = result['stepSize'].split('.')
                if stepSize[0] == '1':
                    quantity = round(float(pl.panda_rebalance[item][2]))
                else:
                    prec = stepSize[1].index('1')+1
                    pre_quant = pl.panda_rebalance[item][2].split('.')
                    quantity = float(pre_quant[0]+'.'+pre_quant[1][:prec])
                    
                order=client.create_order(
                    symbol=result['symbol'],
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                success[item] = ['Transaction Successful',order['orderId']]
                
                print(order)
                print('\n')
            
            except:
                
                order=client.create_order(
                    symbol=result['symbol'],
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                print(order)
                print('\n')
                error[item] = ['Transaction Failed','Transaction doesnt allow lower than minimum tradeable amount']
    
        ##Displaying the balance
        
    Account_info = client.get_account()
    
    balance = []
    #counter = 0

    #price_to_use = []
    
    # for symbol in symbols:
    #     for item in pl.prices:
    #         if item['symbol'] == symbol:
    #             price_to_use.append(item['symbol'])
    #             break

    for item in Account_info['balances']:
        exchange_record = {}
        equiv_price = 0.0
        if float(item['free']) > 0.0:

            result = getPairName(item['asset'],'BTC')

            if result is None:
                item['equiv_price'] = float(item['free'])
            
            else:
                for iterable in pl.prices:
                    if iterable['symbol'] == result['symbol']:
                        exchange_record = iterable
                        break
                
                temp = exchange_record['symbol'].split(pl.main_curreny)
                index = temp.index(item['asset'])

                if index == 0:
                    actual_investment = float(exchange_record['price'])
                elif index == 1:
                    actual_investment = 1/(float(exchange_record['price']))

                equiv_price = float(item['free']) * actual_investment
                print(item)
                print(equiv_price)
                print('\n')
                item['equiv_price'] = equiv_price
            

            balance.append(item)
    
    total = 0.0
    for item in balance:
        total = total+item['equiv_price']
    for item in balance:
        percent = round((float(item['equiv_price'])/total)*100,2)
        percent = str(percent)+'%'
        item['percent'] = percent
        #print(balance)

    context = {
        'success':success,
        'error':error,
        'balance':balance,
    }

    #pl = None
    #pl = viewload()
     
    return render(request,'/home/cherokee/streamer/Django app/mysite/BinanceExchange/templates/exchange.html',context=context)
    #return HttpResponse(pl.key+" "+pl.secret+" ")




# Create your views here.

#helper functions
def getCoinList():
    data = Coinlist.objects.all()
    coinlist = []
    for item in data:
        coinlist.append(item)
        print(item.fetchData())
    return coinlist

def getPairName(asset1,asset2):
    
    host = 'social-data.cfsorzk52kgn.us-east-2.rds.amazonaws.com'
    dbname = 'SocialData'
    user = 'root'
    password = '5X97nbBUFnEU'
    port = 3306

    conn = pymysql.connect(host,user=user,port=port,passwd=password,db=dbname,
                        cursorclass=pymysql.cursors.DictCursor)
    
    with conn.cursor() as cursor:
        query = 'Select * from BinanceExchangeInformation where baseAsset IN {} and quoteAsset IN {}'.format((asset1,asset2),(asset1,asset2))
        cursor.execute(query)
        result = cursor.fetchone()
    conn.close()
    
    print(result)

    return result