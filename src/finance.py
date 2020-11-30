#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   finance.py
@Time    :   2020/11/30 17:21:38
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here

import numpy as np

class Finance(object):
    """ 项目财务分析主类
    本类主要实现风电项目财务分析过程的抽象封装，
    包括对应一次财务评价的项目边界参数、核心算法。

    成员变量：
    ----------
        capacity: float, default = 10.0
            风电场装机容量，单位为“万kW”，默认值为 10 万kW
        
        power: float, default = 2500.0
            年发电量，单位为“小时”（年等效满发上网小时数）

        static_investment: float, default = 700 000 000.0
            项目静态总投资，单位为“元”，默认值为 7000元/kW * 10万kW

        price: float, default = 0.3779
            含税上网电价，单位为“元/度”，默认值为河南燃煤标杆上网电价

        equip_cost: float, default = 420 000 000.0
            设备购置费，单位为“元”，默认值 = 静态总投资*60%

        loan_rate: float, default = 0.054
            长期贷款利率，默认值为公司现阶段融资成本 5.4%

        current_rate: float, default = 0.06
            流动资金贷款利率，默认值为 6.0%
        
        rate_discount: float, default = 1.0
            长期贷款利率折扣，默认值 100%，即无折扣

        income_tax_rate: float, default = 0.25
            所得税税率（income tax rate），默认值为 25 %

        vat_rate: float, default = 0.13
            增值税税率（value-added tax rate），默认值为 13 %

        vat_refund_rate: float, default = 0.5
            增值税退税比率（vat refund rate），默认值为 50 %

        workers: integer, default = 10
            员工人数，默认值为 10 人（1万kW装机匹配1人）

        labor_cost: float, default = 15.5
            人均人工成本，单位为“万元/年·人”，默认值为

        in_repair_rate: float, default = 0.005
            质保期内修理费率（repair costs rate during the warranty period），默认值为 0.5 %

        out_repair_rate: float, default = 0.01
            质保期外修理费率（Out-of-warranty repair costs rate），默认值为 1 %

        warranty: float, default = 2.0
            质保期，单位为“年”，默认值为 2.0 年

        insurance_rate: float, default = 0.0025
            保险费率，默认值为 0.25 %

        material_fee: float, default = 10.0
            单位材料费，单位为“元/kW”，默认值为 10.0 元/kW

        other_fee_rate: float, default = 40.0
            其它费用定额，单位为“元/kW”，默认值为 40.0 元/kW

        withdraw_rate: float, default = 0.1
            盈余公积提取比例（withdrawal ratio of surplus reserve），默认值为 10 %

        operate_period: integer, default = 21
            经营期（operate period），单位为“年”，默认值为 21 年

        loan_period: integer, default = 15
            （长期贷款）借款期，单位为“年”，默认值为 15 年

        grace_period: integer, default = 1
            （长期贷款）宽限期，单位为“年”，默认值为 1 年
    
    备注：
    ----------
        1. 第一阶段版本暂按照“等额本金”的方式测算，“等额本息”的模式后续再行补充；
        2. 第一阶段版本仅考虑风电项目的收益测算，光伏项目和其它能源项目的测算逻辑后续再行添加；
        3. 第一阶段一些细节咱做概化（如造价构成、人员工资构成等），后续根据需要进行展开；
        
    """
    pass

if __name__ == "__main__":
    pass