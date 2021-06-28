#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   direct_irr.py
@Time    :   2020/12/15 20:58:40
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# （正向直接）测算项目的 IRR 边界面

import numpy as np
import os, sys

# 加载模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from finance.base import Finance
from finance.calculate import cal_price
from finance.tools import write_excel

##############################################################
# 计算项目投资 IRR 和资本金 IRR
finance = Finance()
finance.capacity = 10.0  # 项目容量 10 万 kW
finance.price = 0.2829  # 电价按河南省标杆上网电价 0.3779 元/度
finance.capital_ratio = 0.20  # 资本金比例 25%
finance.loan_rate = 0.049  # 贷款利率（长期）
finance.workers = 10  # 运维人员数量

# 边界列表
aep = np.linspace(2500, 4000, 16)  # 发电量序列  “小时”
investment = np.linspace(5000, 6500, 16)  # 静态投资额变化序列  “元/kW”

# 结果列表
pre_pro_irr = []  # 税前项目投资 IRR 列表
after_pro_irr = []  # 税后项目投资 IRR 列表
cap_irr = []  # 资本金 IRR 列表

# 计算 IRR 矩阵
for aep_item in aep:
    aux_pre = []  # 税前项目 IRR 辅助列表
    aux_after = []  # 税后项目 IRR 辅助列表
    aux_cap = []  # 项目资本金 IRR 辅助列表
    for invst_item in investment:
        finance.static_investment = invst_item * finance.capacity
        finance.aep = aep_item
        finance.equipment_cost = finance.static_investment * finance.equipment_ratio
        pre, after, cap = finance.com_finance()  # 中间流量表结果
        aux_pre.append(Finance.com_irr(pre))
        aux_after.append(Finance.com_irr(after))
        aux_cap.append(Finance.com_irr(cap))
    pre_pro_irr.append(aux_pre)
    after_pro_irr.append(aux_after)
    cap_irr.append(aux_cap)

# 将 IRR 矩阵写入 excel 表
sheet_name = ['税前项目投资 IRR', '税后项目投资 IRR', '项目资本金 IRR']
row_name = [str(k) for k in aep]
column_name = [str(k) for k in investment]

write_excel([pre_pro_irr,after_pro_irr,cap_irr], sheet_name=sheet_name, row_header=row_name, column_header=column_name)