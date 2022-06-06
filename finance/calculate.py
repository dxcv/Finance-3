#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   calculate.py
@Time    :   2020/12/06 09:58:18
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# 计算各项财务边界面

# 导入工具包
import os, sys
import numpy as np
# 加载模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# 导入自己的包
from finance.base import Finance


def cal_price(finance, pro_irr=0.06, cap_irr=0.08, mode=0):
    """
    计算满足特定收益条件下的电价（含税）临界面。

    输入参数：
    ----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.065
            项目投资内部收益率（税前），默认值为 6.5 %
        
        cap_irr: float, default = 0.08
            项目资本金内部收益率（税后），默认值为 8 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= cap_irr 
                1：项目 IRR >= pro_irr 
                2：资本金 IRR >= cap_irr and 项目 IRR >= pro_irr
    
    返回结果：
    ----------
        price: float
            对应项目边界和给定收益率情况下的临界电价，单位为“元/度”

    备注：
    ----------
        1. 暂时用 mode 这种比较蹩脚的方式区分测算模式，比较好的方式是根据输入变量进行区分；
        2. 第一阶段暂时不考虑输入数据格式和范围有效性检查，默认其格式和范围都是合理的。
    
    """
    flow = finance.com_finance()  # 现金流元组（项目税前净现金流，项目税后净现金流，资本金现金流）
    com_pro_irr = Finance.com_irr(flow[0])  # 计算所得项目税前 IRR
    com_cap_irr = Finance.com_irr(flow[2])  # 计算所得资本金 IRR（税后）
    delta_price = 0.0  # 电价递增幅度，单位为“元”，将根据具体模式和具体计算结果确定增长方向

    if mode == 0:  # 要求资本金 IRR 达标
        if com_cap_irr < cap_irr:  # 低于标准 IRR
            delta_price = 0.0001 
        else:
            delta_price = -0.0001
        
        # 计算临界值
        temp = com_cap_irr - cap_irr
        while temp * (com_cap_irr - cap_irr) > 0:
            temp = com_cap_irr - cap_irr  # 保存上一个差值
            finance.price += delta_price
            flow = finance.com_finance()
            com_cap_irr = Finance.com_irr(flow[2])
    elif mode == 1:  # 要求项目投资 IRR 达标
        if com_pro_irr < pro_irr:  # 低于标准 IRR
            delta_price = 0.0001 
        else:
            delta_price = -0.0001
        
        # 计算临界值
        temp = com_pro_irr - pro_irr
        while temp * (com_pro_irr - pro_irr) > 0:
            temp = com_pro_irr - pro_irr  # 保存上一个差值
            finance.price += delta_price
            flow = finance.com_finance()
            com_pro_irr = Finance.com_irr(flow[0])
    else:  # 要求项目投资 IRR 和资本金 IRR 均达标
        if com_pro_irr < pro_irr or com_cap_irr < cap_irr:  # 低于标准 IRR
            delta_price = 0.0001 
        else:
            delta_price = -0.0001
        
        # 计算临界值
        if com_cap_irr >= cap_irr and com_pro_irr >= pro_irr:
            flag = (com_cap_irr - cap_irr) * (com_pro_irr - pro_irr) > 0
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = (com_cap_irr - cap_irr) * (com_pro_irr - pro_irr) > 0
        elif com_cap_irr >= cap_irr and com_pro_irr <= pro_irr:
            flag = com_pro_irr < pro_irr
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_pro_irr < pro_irr
        elif com_cap_irr <= cap_irr and com_pro_irr >= pro_irr:
            flag = com_cap_irr < cap_irr
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_cap_irr < cap_irr
        else:
            flag = com_cap_irr < cap_irr or com_pro_irr < pro_irr
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_cap_irr < cap_irr or com_pro_irr < pro_irr
    # 返回结果
    return finance.price
    


def cal_investment(finance, pro_irr=0.06, cap_irr=0.08, mode=0):
    """
    计算满足给定收益水平下的项目造价临界面。

    输入参数：
    -----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.06
            项目投资内部收益率（税后），默认值为 6 %
        
        cap_irr: float, default = 0.08
            项目资本金内部收益率（税后），默认值为 8 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= cap_irr
                1：项目 IRR >= pro_irr
                2：资本金 IRR >= cap_irr and 项目 IRR >= pro_irr
    
    返回结果：
    ----------
        investment: float
            对应项目边界和给定收益情况下的临界静态投资，单位为“元/kW”
    
    备注：
    ----------
        1. 暂时用 mode 这种比较蹩脚的方式区分测算模式，比较好的方式是根据输入变量进行区分；
        2. 第一阶段暂时不考虑输入数据格式和范围有效性检查，默认其格式和范围都是合理的。

    """
    pass


def cal_aep(finance,pro_irr=0.06, cap_irr=0.08, mode=0):
    """
    计算满足给定收益水平下的项目年发电量临界面。

    输入参数：
    -----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.06
            项目投资内部收益率（税前），默认值为 6 %
        
        cap_irr: float, default = 0.08
            项目资本金内部收益率（税后），默认值为 8 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= cap_irr
                1：项目 IRR >= pro_irr
                2：资本金 IRR >= cap_irr and 项目 IRR >= pro_irr
    
    返回结果：
    ----------
        aep: float
            对应项目边界和给定收益情况下的临界年发电量，单位为“小时”
    
    备注：
    ----------
        1. 暂时用 mode 这种比较蹩脚的方式区分测算模式，比较好的方式是根据输入变量进行区分；
        2. 第一阶段暂时不考虑输入数据格式和范围有效性检查，默认其格式和范围都是合理的。

    """
    flow = finance.com_finance()  # 现金流元组（项目税前净现金流，项目税后净现金流，资本金现金流）
    com_pro_irr = Finance.com_irr(flow[0])  # 计算所得项目税前 IRR
    com_cap_irr = Finance.com_irr(flow[2])  # 计算所得资本金 IRR（税后）
    delta_aep = 1 # 电价递增幅度，单位为“小时”，将根据具体模式和具体计算结果确定增长方向

    if mode == 0:  # 要求资本金 IRR 达标
        if com_cap_irr < cap_irr:  # 低于标准 IRR
            delta_aep = 1 
        else:
            delta_aep = -1
        
        # 计算临界值
        temp = com_cap_irr - cap_irr
        while temp * (com_cap_irr - cap_irr) > 0:
            temp = com_cap_irr - cap_irr  # 保存上一个差值
            finance.aep += delta_aep
            flow = finance.com_finance()
            com_cap_irr = Finance.com_irr(flow[2])
    elif mode == 1:  # 要求项目投资 IRR 达标
        if com_pro_irr < pro_irr:  # 低于标准 IRR
            delta_aep = 1 
        else:
            delta_aep = -1
        
        # 计算临界值
        temp = com_pro_irr - pro_irr
        while temp * (com_pro_irr - pro_irr) > 0:
            temp = com_pro_irr - pro_irr  # 保存上一个差值
            finance.aep += delta_aep
            flow = finance.com_finance()
            com_pro_irr = Finance.com_irr(flow[0])
    else:  # 要求项目投资 IRR 和资本金 IRR 均达标
        if com_pro_irr < pro_irr or com_cap_irr < cap_irr:  # 低于标准 IRR
            delta_aep = 1 
        else:
            delta_aep = -1
        
        # 计算临界值
        if com_cap_irr >= cap_irr and com_pro_irr >= pro_irr:
            flag = (com_cap_irr - cap_irr) * (com_pro_irr - pro_irr) > 0
            while flag:
                finance.aep += delta_aep
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = (com_cap_irr - cap_irr) * (com_pro_irr - pro_irr) > 0
        elif com_cap_irr >= cap_irr and com_pro_irr <= pro_irr:
            flag = com_pro_irr < pro_irr
            while flag:
                finance.aep += delta_aep
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_pro_irr < pro_irr
        elif com_cap_irr <= cap_irr and com_pro_irr >= pro_irr:
            flag = com_cap_irr < cap_irr
            while flag:
                finance.aep += delta_aep
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_cap_irr < cap_irr
        else:
            flag = com_cap_irr < cap_irr or com_pro_irr < pro_irr
            while flag:
                finance.aep += delta_aep
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[0])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_cap_irr < cap_irr or com_pro_irr < pro_irr
    # 返回结果
    return finance.aep


def cal_capacity(parameter_list):
    """
    计算满足给定收益水平下的项目装机规模临界面。

    输入参数：
    -----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.06
            项目投资内部收益率（税后），默认值为 6 %
        
        cap_irr: float, default = 0.08
            项目资本金内部收益率（税后），默认值为 8 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= cap_irr
                1：项目 IRR >= pro_irr
                2：资本金 IRR >= cap_irr and 项目 IRR >= pro_irr
    
    返回结果：
    ----------
        capacity: float
            对应项目边界和给定收益情况下的临界装机容量，单位为“万kW”
    
    备注：
    ----------
        1. 暂时用 mode 这种比较蹩脚的方式区分测算模式，比较好的方式是根据输入变量进行区分；
        2. 第一阶段暂时不考虑输入数据格式和范围有效性检查，默认其格式和范围都是合理的。

    """
    pass


if __name__ == "__main__":
    
    # 程序功能测试
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
    
    finance.aep = 2500 # 发电量（小时）
    finance.price = 0.25 # 电价（元/千瓦时）
    finance.static_investment = 5500 * finance.capacity # 静态总投资（万元）

    pro_irr = 0.06  # 项目投资 IRR（税前） 标准
    cap_irr = 0.08  # 资本金 IRR（税后） 标准
    
    # 计算临界电价
    price = cal_price(finance, pro_irr=pro_irr, cap_irr=cap_irr)
    
    # 计算临界小时数
    finance.price = 0.2277
    aep = cal_aep(finance,pro_irr=pro_irr,cap_irr=cap_irr)
    # 打印结果
    print(price,aep)