#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   wind_reverse_price.py
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
finance.capacity = 100.0  # 项目容量（万千瓦）
finance.equipment_ratio = 0.7  # 设备购置费占静态投资比例系数
finance.build_ratio = 0.13  # 建筑工程（含辅助工程）费用占静态投资比例系数
finance.install_ratio = 0.07  # 设备安装费占静态投资比例系数
finance.other_ratio = 0.1  # 其它费用占静态投资比例系数
finance.capital_ratio = 0.20  # 资本金比例
finance.working_ratio = 0.30  # 流动资金资本金比例
finance.loan_rate = 0.046  # 贷款利率（长期）
finance.working_rate = 0.0435  # 流动资金贷款利率
finance.rate_discount = 1.0  # 长期贷款利率折扣（1为无）
finance.vat_refund_rate =0.5  # 增值税退税比率
finance.workers = 25  # 运维人员数量（个）
finance.labor_cost = 16  # 员工年工资及福利费（万元）
finance.in_repair_rate = 0.005  # 质保期内修理费率
finance.out_repair_rate  = 0.015  # 质保期外修理费率
finance.warranty = 5  # 质保期（年）
finance.depreciation_period = 20  # 折旧年限（年）
finance.material_quota = 10  # 单位材料费（元/kW）
finance.other_quota = 30  # 其它费用定额（元/kW）
finance.working_quota = 30 # （铺底）流动资金定额（元/kW）
finance.build_period = 1  # 建设期（年）
finance.operate_period = 20  # 经营期（年）
finance.loan_period = 15  # 借款期（年）
finance.residual_rate = 0.05  # 残值率
finance.cost_list = []  # 成本费辅助流量列表（万元）
finance.cash_list = []  # 项目现金流量辅助列表（万元）
finance.cap_list = []  # 资本金现金流量辅助列表（万元）

pro_irr = 0.01  # 项目投资 IRR（税后） 标准
cap_irr = 0.08  # 资本金 IRR（税后） 标准
    
## 电价临界面计算逻辑测试
price = []  # 临界电价列表（二维）
aep = np.linspace(1500, 4000, 251)  # 发电量序列  “小时”
investment = np.linspace(4000, 6500, 51)  # 投资额变化序列  “元/kW”
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

write_excel(price, row_header=row_name, 
            column_header=column_name,file='风电上网电价-资本金-8%.xlsx')