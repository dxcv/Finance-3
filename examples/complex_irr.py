from email import header
from msilib.schema import File
#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   complex_irr.py
@Time    :   2022/03/13 21:55:58
@Author  :   liuzy2022 
@Version :   1.0
@Contact :   liuzy2013@163.com
@License :   (C)Copyright 2022-2023, creei
@WebSite :   https://path2019.github.io
'''

# Start typing your code from here
# 测算风光储等综合类项目的收益率

# here put the import lib
import numpy as np
import os, sys

# 加载模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from finance.base import Finance
from finance.base import Price
from finance.calculate import cal_price
from finance.tools import write_excel

####################################
# 风电模块，计算风电工程的三个现金流数据
####################################
wind_finance = Finance()
wind_finance.capacity = 100.0  # 项目容量（万千瓦）
wind_finance.equipment_ratio = 0.7  # 设备购置费占静态投资比例系数
wind_finance.build_ratio = 0.13  # 建筑工程（含辅助工程）费用占静态投资比例系数
wind_finance.install_ratio = 0.07  # 设备安装费占静态投资比例系数
wind_finance.other_ratio = 0.1  # 其它费用占静态投资比例系数
wind_finance.capital_ratio = 0.20  # 资本金比例
wind_finance.working_ratio = 0.30  # 流动资金资本金比例
wind_finance.loan_rate = 0.046  # 贷款利率（长期）
wind_finance.working_rate = 0.0435  # 流动资金贷款利率
wind_finance.rate_discount = 1.0  # 长期贷款利率折扣（1为无）
wind_finance.vat_refund_rate =0.5  # 增值税退税比率
wind_finance.workers = 25  # 运维人员数量（个）
wind_finance.labor_cost = 16  # 员工年工资及福利费（万元）
wind_finance.in_repair_rate = 0.005  # 质保期内修理费率
wind_finance.out_repair_rate  = 0.015  # 质保期外修理费率
wind_finance.warranty = 5  # 质保期（年）
wind_finance.depreciation_period = 20  # 折旧年限（年）
wind_finance.material_quota = 10  # 单位材料费（元/kW）
wind_finance.other_quota = 30  # 其它费用定额（元/kW）
wind_finance.working_quota = 30 # （铺底）流动资金定额（元/kW）
wind_finance.build_period = 1  # 建设期（年）
wind_finance.operate_period = 20  # 经营期（年）
wind_finance.loan_period = 15  # 借款期（年）
wind_finance.residual_rate = 0.05  # 残值率
wind_finance.cost_list = []  # 成本费辅助流量列表（万元）
wind_finance.cash_list = []  # 项目现金流量辅助列表（万元）
wind_finance.cap_list = []  # 资本金现金流量辅助列表（万元）
wind_finance.aep = 3000.0  # 年均发电量（小时）
wind_finance.price = 0.2829  # 上网电价（元/千瓦时）
wind_finance.static_investment = 5000 * wind_finance.capacity  # 静态投资额（万元)
wind_finance.cost_list = []  # 成本费辅助流量列表（万元）
wind_finance.cash_list = []  # 项目现金流量辅助列表（万元）
wind_finance.cap_list = []  # 资本金现金流量辅助列表（万元）


# 计算风电工程的税前项目净现金流、税后项目净现金流和税后资本金净现金流
wind_pre, wind_after, wind_cap = wind_finance.com_finance()

#####################################
# 光伏模块，计算光伏工程的三个现金流数据
#####################################
pv_finance = Finance()
pv_finance.capacity = 100.0  # 项目容量（万千瓦）
pv_finance.equipment_ratio = 0.7  # 设备购置费占静态投资比例系数
pv_finance.build_ratio = 0.13  # 建筑工程（含辅助工程）费用占静态投资比例系数
pv_finance.install_ratio = 0.07  # 设备安装费占静态投资比例系数
pv_finance.other_ratio = 0.1  # 其它费用占静态投资比例系数
pv_finance.capital_ratio = 0.20  # 资本金比例
pv_finance.working_ratio = 0.30  # 流动资金资本金比例
pv_finance.loan_rate = 0.046  # 贷款利率（长期）
pv_finance.working_rate = 0.0435  # 流动资金贷款利率
pv_finance.rate_discount = 1.0  # 长期贷款利率折扣（1为无）
pv_finance.vat_refund_rate =0.0  # 增值税退税比率
pv_finance.workers = 25  # 运维人员数量（个）
pv_finance.labor_cost = 16  # 员工年工资及福利费（万元）
pv_finance.in_repair_rate = 0.002  # 质保期内修理费率
pv_finance.out_repair_rate  = 0.005  # 质保期外修理费率
pv_finance.warranty = 5  # 质保期（年）
pv_finance.depreciation_period = 20  # 折旧年限（年）
pv_finance.material_quota = 10  # 单位材料费（元/kW）
pv_finance.other_quota = 20  # 其它费用定额（元/kW）
pv_finance.working_quota = 30 # （铺底）流动资金定额（元/kW）
pv_finance.build_period = 1  # 建设期（年）
pv_finance.operate_period = 25  # 经营期（年）
pv_finance.loan_period = 15  # 借款期（年）
pv_finance.residual_rate = 0.05  # 残值率
pv_finance.aep = 1600.0  # 年均发电量（小时）
pv_finance.static_investment = 3800 * pv_finance.capacity  # 静态投资额（万元）
pv_finance.price = 0.2829  # 上网电价（元/千瓦时）
pv_finance.cost_list = []  # 成本费辅助流量列表（万元）
pv_finance.cash_list = []  # 项目现金流量辅助列表（万元）
pv_finance.cap_list = []  # 资本金现金流量辅助列表（万元）

# 计算光伏工程的税前项目净现金流、税后项目净现金流和税后资本金净现金流
pv_pre, pv_after, pv_cap = pv_finance.com_finance()

#####################################
# 其它子工程的三个现金流数据
#####################################


#####################################
# 合并现金流量，并计算三个收益率指标
#####################################

pro_pre = wind_pre + pv_pre
pro_after = wind_after + pv_after
cap = wind_cap + pv_cap

pro_pre_irr = Finance.com_irr(pro_pre)
pro_after_irr = Finance.com_irr(pro_after)
cap_irr = Finance.com_irr(cap)
