#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   wind_price_irr.py
@Time    :   2020/12/15 22:33:42
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# 测算风电电价变化对收益率的影响

import numpy as np
import os, sys

# 加载模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from finance.base import Finance
from finance.calculate import cal_price
from finance.tools import write_excel

#############################################
# 测算逻辑
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

# 边界列表
aep = np.linspace(1500, 4000, 251)  # 发电量序列  “小时”
investment = np.linspace(4000, 6500, 6)  # 投资额变化序列  “元/kW”
price = np.linspace(0.1, 0.4, 31)  # 电价序列  “元/度”

for invest in investment:
    # 工程造价
    finance.static_investment = invest * finance.capacity
    
    # 结果列表
    pre_pro_irr = []  # 税前项目投资 IRR 列表
    after_pro_irr = []  # 税后项目投资 IRR 列表
    cap_irr = []  # 资本金 IRR 列表

    # 计算 IRR 矩阵
    for aep_item in aep:
        aux_pre = []  # 税前项目 IRR 辅助列表
        aux_after = []  # 税后项目 IRR 辅助列表
        aux_cap = []  # 项目资本金 IRR 辅助列表
        for price_item in price:
            finance.price = price_item
            finance.aep = aep_item
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
    column_name = [str(k) for k in price]

    write_excel([pre_pro_irr,after_pro_irr,cap_irr], sheet_name=sheet_name, 
                row_header=row_name, column_header=column_name,
                file='风电收益-' + str(invest) + '.xlsx')