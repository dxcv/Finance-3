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

from finance import Finance

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
    pass


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
