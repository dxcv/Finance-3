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

import numpy as np
from finance import Finance
from tools import write_excel


def cal_price(finance, pro_irr=0.07, cap_irr=0.1, mode=0):
    """
    计算满足特定收益条件下的电价（含税）临界面。

    输入参数：
    ----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.07
            项目投资内部收益率（税后），默认值为 7 %
        
        cap_irr: float, default = 0.1
            项目资本金内部收益率（税后），默认值为 10 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= 10 %
                1：项目 IRR >= 7 %
                2：资本金 IRR >= 10 % and 项目 IRR >= 7 %
    
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
    com_pro_irr = Finance.com_irr(flow[1])  # 计算所得项目税后 IRR
    com_cap_irr = Finance.com_irr(flow[2])  # 计算所得资本金 IRR（税后）
    delta_price = 0.0  # 电价递增幅度，单位为“元”，将根据具体模式和具体计算结果确定增长方向

    if mode == 0:  # 要求资本金 IRR 达标
        if com_cap_irr < cap_irr:  # 低于标准 IRR
            delta_price = 0.001 
        else:
            delta_price = -0.001
        
        # 计算临界值
        temp = com_cap_irr - cap_irr
        while temp * (com_cap_irr - cap_irr) > 0:
            temp = com_cap_irr - cap_irr  # 保存上一个差值
            finance.price += delta_price
            flow = finance.com_finance()
            com_cap_irr = Finance.com_irr(flow[2])
    elif mode == 1:  # 要求项目投资 IRR 达标
        if com_pro_irr < pro_irr:  # 低于标准 IRR
            delta_price = 0.001 
        else:
            delta_price = -0.001
        
        # 计算临界值
        temp = com_pro_irr - pro_irr
        while temp * (com_pro_irr - pro_irr) > 0:
            temp = com_pro_irr - pro_irr  # 保存上一个差值
            finance.price += delta_price
            flow = finance.com_finance()
            com_pro_irr = Finance.com_irr(flow[1])
    else:  # 要求项目投资 IRR 和资本金 IRR 均达标
        if com_pro_irr < pro_irr or com_cap_irr < cap_irr:  # 低于标准 IRR
            delta_price = 0.001 
        else:
            delta_price = -0.001
        
        # 计算临界值
        if com_cap_irr >= cap_irr and com_pro_irr >= pro_irr:
            flag = (com_cap_irr - cap_irr) * (com_pro_irr - pro_irr) > 0
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[1])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = (com_cap_irr - cap_irr) * (com_pro_irr - pro_irr) > 0
        elif com_cap_irr >= cap_irr and com_pro_irr <= pro_irr:
            flag = com_pro_irr < pro_irr
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[1])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_pro_irr < pro_irr
        elif com_cap_irr <= cap_irr and com_pro_irr >= pro_irr:
            flag = com_cap_irr < cap_irr
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[1])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_cap_irr < cap_irr
        else:
            flag = com_cap_irr < cap_irr or com_pro_irr < pro_irr
            while flag:
                finance.price += delta_price
                flow = finance.com_finance()
                com_pro_irr = Finance.com_irr(flow[1])
                com_cap_irr = Finance.com_irr(flow[2])
                flag = com_cap_irr < cap_irr or com_pro_irr < pro_irr
    # 返回结果
    return finance.price
    


def cal_investment(finance, pro_irr=0.07, cap_irr=0.1, mode=0):
    """
    计算满足给定收益水平下的项目造价临界面。

    输入参数：
    -----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.07
            项目投资内部收益率（税后），默认值为 7 %
        
        cap_irr: float, default = 0.1
            项目资本金内部收益率（税后），默认值为 10 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= 10 %
                1：项目 IRR >= 7 %
                2：资本金 IRR >= 10 % and 项目 IRR >= 7 %
    
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


def cal_aep(finance,pro_irr=0.07, cap_irr=0.1, mode=0):
    """
    计算满足给定收益水平下的项目年发电量临界面。

    输入参数：
    -----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.07
            项目投资内部收益率（税后），默认值为 7 %
        
        cap_irr: float, default = 0.1
            项目资本金内部收益率（税后），默认值为 10 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= 10 %
                1：项目 IRR >= 7 %
                2：资本金 IRR >= 10 % and 项目 IRR >= 7 %
    
    返回结果：
    ----------
        aep: float
            对应项目边界和给定收益情况下的临界年发电量，单位为“小时”
    
    备注：
    ----------
        1. 暂时用 mode 这种比较蹩脚的方式区分测算模式，比较好的方式是根据输入变量进行区分；
        2. 第一阶段暂时不考虑输入数据格式和范围有效性检查，默认其格式和范围都是合理的。

    """
    pass


def cal_capacity(parameter_list):
    """
    计算满足给定收益水平下的项目装机规模临界面。

    输入参数：
    -----------
        finance: Finance
            与财务评价相关的项目各项边界，具体边界条目和默认值参见 Finance 类定义
        
        pro_irr: float, default = 0.07
            项目投资内部收益率（税后），默认值为 7 %
        
        cap_irr: float, default = 0.1
            项目资本金内部收益率（税后），默认值为 10 %
        
        mode: integer, default = 0
            测算模式，对应不同的收益边界要求
                0：资本金 IRR >= 10 %
                1：项目 IRR >= 7 %
                2：资本金 IRR >= 10 % and 项目 IRR >= 7 %
    
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
    pro_irr = 0.07  # 项目投资 IRR（税后） 标准（
    cap_irr = 0.10  # 资本金 IRR（税后） 标准
    
    ## 电价临界面计算逻辑测试
    price = []  # 临界电价列表（三维）
    capacity = np.array([5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # 装机容量   “万kW”
    aep = np.linspace(1800, 3000, 25)  # 发电量序列  “小时”
    investment = np.linspace(5000, 8000, 31)  # 投资额变化序列  “元/kW”
    for capa_item in capacity:
        temp_price=[]  # 辅助临界电价测算列表
        for aep_item in aep:
            aux_price = []  # 辅助临界电价测算列表
            for invest_item in investment:
                finance.capacity = capa_item
                finance.static_investment = invest_item * finance.capacity
                finance.aep = aep_item
                finance.equipment_cost = finance.static_investment * finance.equipment_ratio
                finance.workers = int(finance.capacity)
                aux_price.append(cal_price(finance, pro_irr=pro_irr, cap_irr=cap_irr, mode=2))
            temp_price.append(aux_price)
        price.append(temp_price)
    
    # 输出结果
    sheet_name = [str(k) + ' 万 kW' for k in capacity]
    row_name = [str(k) for k in aep]
    column_name = [str(k) for k in investment]

    write_excel(price, sheet_name=sheet_name, row_header=row_name, column_header=column_name)