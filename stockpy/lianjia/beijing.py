# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 15:41:36 2018

@author: blan
"""

import pandas as pd

import numpy as np

import seaborn as sns

import matplotlib as mpl

import matplotlib.pyplot as plt

from IPython.display import display

plt.style.use("fivethirtyeight")

sns.set_style({'font.sans-serif':['simhei','Arial']})



# 检查Python版本

from sys import version_info

if version_info.major != 3:

    raise Exception('请使用Python 3 来完成此项目')
    
    
# 导入链家二手房数据

lianjia_df = pd.read_csv('D:/qqtongbu/tongbu/lianjia.csv')

display(lianjia_df.head(n=2))    

# 检查缺失值情况

lianjia_df.info()

#发现了数据集一共有    23677 条数据，其中     Elevator 特征有明显的缺失值。

lianjia_df.describe()

"""
上面结果给出了特征值是数值的一些统计值，包括平均数，标准差，中位数，最小值，最大值，25%分位数，75%分位数。
这些统计结果简单直接，对于初始了解一个特征好坏非常有用，比如我们观察到 Size 特征 的最大值为1019平米，
最小值为2平米，那么我们就要思考这个在实际中是不是存在的，如果不存在没有意义，那么这个数据就是一个异常值，
会严重影响模型的性能。

当然，这只是初步观察，后续我们会用数据可视化来清晰的展示，并证实我们的猜测。
"""

# 添加新特征房屋均价

df = lianjia_df.copy()

df['PerPrice'] = lianjia_df['Price']/lianjia_df['Size']

# 重新摆放列位置

columns = ['Region', 'District', 'Garden', 'Layout', 'Floor', 'Year', 'Size',
           'Elevator', 'Direction', 'Renovation', 'PerPrice', 'Price']

df = pd.DataFrame(df, columns = columns)

# 重新审视数据集

display(df.head(n=2))

"""
我们发现 Id 特征其实没有什么实际意义，所以将其移除。由于房屋单价分析起来比较方便，
简单的使用总价/面积就可得到，所以增加一个新的特征 PerPrice（只用于分析，不是预测特征）。
另外，特征的顺序也被调整了一下，看起来比较舒服。
"""
"""
Region特征分析

对于区域特征，我们可以分析不同区域房价和数量的对比。

对二手房区域分组对比二手房数量和每平米房价
"""


df_house_count = df.groupby('Region')['Price'].count().sort_values(ascending=False).to_frame().reset_index()

df_house_mean = df.groupby('Region')['PerPrice'].mean().sort_values(ascending=False).to_frame().reset_index()

f, [ax1,ax2,ax3] = plt.subplots(3,1,figsize=(20,15))

sns.barplot(x='Region', y='PerPrice', palette="Blues_d", data=df_house_mean, ax=ax1)

ax1.set_title('北京各大区二手房每平米单价对比',fontsize=15)

ax1.set_xlabel('区域')

ax1.set_ylabel('每平米单价')

sns.barplot(x='Region', y='Price', palette="Greens_d", data=df_house_count, ax=ax2)

ax2.set_title('北京各大区二手房数量对比',fontsize=15)

ax2.set_xlabel('区域')

ax2.set_ylabel('数量')

sns.boxplot(x='Region', y='Price', data=df, ax=ax3)

ax3.set_title('北京各大区二手房房屋总价',fontsize=15)

ax3.set_xlabel('区域')

ax3.set_ylabel('房屋总价')

plt.show()

"""
使用了 pandas 的网络透视功能 groupby  分组排序。区域特征可视化直接采用  seaborn 完成 ，
颜色使用调色板 palette  参数，颜色渐变，越浅说明越少，反之越多。

可以观察到：

二手房均价：西城区的房价最贵均价大约11万/平，因为西城在二环以里，且是热门学区房的聚集地。
其次是东城大约10万/平，然后是海淀大约8.5万/平，其它均低于8万/平。
二手房房数量：从数量统计上来看，目前二手房市场上比较火热的区域。
海淀区和朝阳区二手房数量最多，差不多都接近3000套，毕竟大区，需求量也大。
然后是丰台区，近几年正在改造建设，有赶超之势。
二手房总价：通过箱型图看到，各大区域房屋总价中位数都都在1000万以下，且房屋总价离散值较高，
西城最高达到了6000万，说明房屋价格特征不是理想的正太分布。
"""

'''Size特征分析'''

f, [ax1,ax2] = plt.subplots(1, 2, figsize=(15, 5))

# 建房时间的分布情况

sns.distplot(df['Size'], bins=20, ax=ax1, color='r')

sns.kdeplot(df['Size'], shade=True, ax=ax1)

# 建房时间和出售价格的关系

sns.regplot(x='Size', y='Price', data=df, ax=ax2)

plt.show()

'''
Size 分布：
通过 distplot  和 kdeplot 绘制柱状图观察 Size 特征的分布情况，属于长尾类型的分布，
这说明了有很多面积很大且超出正常范围的二手房。
Size 与 Price 的关系：
通过 regplot 绘制了 Size 和 Price 之间的散点图，发现 Size 特征基本与Price呈现线性关系，
符合基本常识，面积越大，价格越高。但是有两组明显的异常点：1. 面积不到10平米，但是价格超出10000万；
2. 一个点面积超过了1000平米，价格很低，需要查看是什么情况。

'''

df.loc[df['Size']< 10]


#Layout特征分析

f, ax1= plt.subplots(figsize=(20,20))

sns.countplot(y='Layout', data=df, ax=ax1)

ax1.set_title('房屋户型',fontsize=15)

ax1.set_xlabel('数量')

ax1.set_ylabel('户型')

plt.show()
