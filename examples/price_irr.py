#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   price_irr.py
@Time    :   2020/12/15 22:33:42
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# 测算电价变化对收益率的影响

import numpy as np
import os, sys

# 加载模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from finance.base import Finance
from finance.calculate import cal_price
from finance.tools import write_excel

#############################################
# 测算逻辑
finance = Finance()
finance.capacity = 10.0  # 项目容量 10 万 kW
finance.aep = 2750.0  # 项目年发电量 2500 小时
finance.static_investment = 6000 * finance.capacity  # 项目静态投资额
finance.equipment_cost = finance.static_investment * finance.equipment_ratio  # 项目设备购置费
finance.capital_ratio = 0.20  # 资本金比例 25%
finance.loan_rate = 0.049  # 贷款利率（长期）
finance.workers = 10  # 运维人员数量

# 边界列表
price = np.linspace(0.2, 0.35, 16)  # 电价序列  “元/度”

# 结果列表
pre_pro_irr = []  # 税前项目投资 IRR 列表
after_pro_irr = []  # 税后项目投资 IRR 列表
cap_irr = []  # 资本金 IRR 列表

# 计算 IRR 矩阵
for price_item in price:
    finance.price = price_item
    pre, after, cap = finance.com_finance()  # 中间流量表结果
    pre_pro_irr.append(Finance.com_irr(pre))
    after_pro_irr.append(Finance.com_irr(after))
    cap_irr.append(Finance.com_irr(cap))

# 将 IRR 矩阵写入 excel 表
row_name = ['税前项目 IRR', '税后项目 IRR', '资本金 IRR']
column_name = [str(k) for k in price]

write_excel([pre_pro_irr,after_pro_irr,cap_irr], row_header=row_name, column_header=column_name)