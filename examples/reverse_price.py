#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   reverse_price.py
@Time    :   2020/12/15 21:52:53
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# 反向测算电价临界面

import numpy as np
import os, sys

# 加载模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from finance.base import Finance
from finance.calculate import cal_price
from finance.tools import write_excel

finance = Finance()  # 项目边界实例
finance.capacity = 10.0  # 项目容量 10 万 kW
finance.capital_ratio = 0.25  # 资本金比例 25%
finance.loan_rate = 0.054  # 贷款利率（长期）
finance.workers = 10  # 运维人员数量

pro_irr = 0.08  # 项目投资 IRR（税后） 标准
cap_irr = 0.12  # 资本金 IRR（税后） 标准
    
## 电价临界面计算逻辑测试
price = []  # 临界电价列表（二维）
aep = np.linspace(1800, 3000, 25)  # 发电量序列  “小时”
investment = np.linspace(5000, 8000, 31)  # 投资额变化序列  “元/kW”
for aep_item in aep:
    aux_price = []  # 辅助临界电价测算列表
    for invest_item in investment:
        finance.static_investment = invest_item * finance.capacity
        finance.aep = aep_item
        finance.equipment_cost = finance.static_investment * finance.equipment_ratio
        aux_price.append(cal_price(finance, pro_irr=pro_irr, cap_irr=cap_irr, mode=2))
    price.append(aux_price)
    
    # 将结果矩阵写入 excel 表
    row_name = [str(k) for k in aep]
    column_name = [str(k) for k in investment]

    write_excel(price, row_name=row_name, column_name=column_name)