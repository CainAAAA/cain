#蒙特卡洛模拟期权定价
from random import gauss,seed
from math import exp,sqrt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import tushare as ts

ts.set_token("beb47e0397bcecc84a3761c908d6312033af11cdff596b76bf6cbcdc")

def single_simulation(s_0,T,n,r,sigma):#定义函数，模拟单一路径，返回一个列表
    p=[s_0,]
    for i in range(n):
        z=gauss(0,1)#生成随机数
        s_next=p[-1]*exp((r-0.5*sigma**2)*T/n+sigma*sqrt(T/n)*z)
        p.append(s_next)
    return p

def price_option(stock_price=4.05,strick=4.05,sigma=0.27,r=0.035,T=34/252,n=100,N=50000,opt_type='call'):
    '''
    :param opt_type:'call'/'put'
    :param stock_price:
    :param strick:
    :param sigma:
    :param r:
    :param T:
    :param n:
    :param N:
    :return:
    '''
    payoff=[]
    for i in range(N):
        s=single_simulation(stock_price,T,n,r,sigma)[-1]
        if opt_type.lower()=='call':
            path_payoff = max(s - strick, 0)
        else:
            path_payoff = max(strick - s, 0)
        payoff.append(path_payoff)
    payoff_mean=sum(payoff)/len(payoff)
    return payoff_mean*exp(-r*T)



data=ts.get_k_data('510050','2019-11-01')[:100]
#print(c)
#data=pd.read_csv('OK2020-02-0914.csv',encoding='gbk',sep='\t',parse_dates=True,header=)
data['d_return']=data['close'].pct_change()
data['volatility']=data.d_return.rolling(60).std()*sqrt(252)
#print(data['volatility'])
data.dropna().tail()
data.head()
sigma=data['volatility']#波动率
#print(sigma)
#n=100#步数拆分
#N=100#模拟价格路径的次数
#stock_price=4.05,strick=4.05,sigma=0.27,r=0.035,T=34/252,n=100,N=50000,opt_type='call'
stock=4.05
bottom_strick=4.05
sigma=0.27
r=0.03
T=34/252

opt_price=[]
for i in range(16):
    strick=bottom_strick+i*0.05
    opt_price.append((strick,price_option(stock,strick,sigma,r=r,T=T,opt_type='call'),price_option(stock,strick,sigma,r=r,T=T,opt_type='put')))
df=pd.DataFrame(opt_price,columns=['strick','call','put'])
print(df,type(df))
df.to_csv('D:/Cain/csv/aa.csv')
#a1=price_option(stock_price=2.475,strick=2.45,sigma=0.27,r=0.03,T=14/252,n=100,N=5000,opt_type='call')
#print(a1)
#payoff.plot(linewidth=0.5,figsize=(10,6))
#plt.savefig("D:/aa/aa/a1.png")#生成图像并且存储



#S=S0exp(r-v**2/2)▲t+v*sqrt(▲t)*zt    #zt服从正态分布的随机变量，基于风险中性找到的递推式
#波动率v用的是历史波动率
'''
data['d_return']=data['收盘'].pct_change()
data['volatility']=data.d_return.rolling(60).std()*sqrt(252)
data.dropna().tail()

#根据蒙特卡罗模拟计算到期价格，然后进行折现
s_0,K,T,n,r,sigma=0,0,0,0,0,0

def single_simulation(s_0,T,n,r,sigma):
    p=[s_0]
    for i in range(n):
        z=gauss(0,1)
        s_next=p[-1]*exp((r-0.5*sigma**2)*T/n+sigma*sqrt(T/n)*z)
        p.append(s_next)
    return p
payoff=[]
N=50000
for i in range(N):
    p=single_simulation(s_0,T,n,r,sigma)
    path_payoff=max (p[-1],-K,0)
    payoff.append(path_payoff)
payoff_mean=sum(payoff)/len(payoff)
call_premium=payoff_mean*exp(-r*T)
'''