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

        equipment_cost: float, default = 420 000 000.0
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
    
    def __init__(self, capacity=10.0,power=2500.0,static_investment=700000000.0,price=0.3779,equipment_cost=420000000.0,loan_rate=0.054,current_rate=0.06,rate_discount=1.0,income_tax_rate=0.25,vat_rate=0.13,vat_refund_rate=0.5,workers=10,labor_cost=15.5,in_repair_rate=0.005,out_repair_rate=0.01,warranty=2.0,insurance_rate=0.0025,material_fee=10.0,other_fee_rate=40.0,withdraw_rate=0.1,operate_period=21,loan_period=15,grace_period=1):
      """
      初始化类变量
      """
      self.capacity=capacity
      self.power=power
      self.static_investment=static_investment
      self.price=price
      self.equipment_cost=equipment_cost
      self.loan_rate=loan_rate
      self.current_rate=current_rate
      self.rate_discount=rate_discount
      self.income_tax_rate=income_tax_rate
      self.vat_rate=vat_rate
      self.vat_refund_rate=vat_refund_rate
      self.workers=workers
      self.labor_cost=labor_cost
      self.in_repair_rate=in_repair_rate
      self.out_repair_rate=out_repair_rate
      self.warranty=warranty
      self.insurance_rate=insurance_rate
      self.material_fee=material_fee
      self.other_fee_rate=other_fee_rate
      self.withdraw_rate=withdraw_rate
      self.operate_period=operate_period
      self.loan_period=loan_period
      self.grace_period=grace_period


    def com_finance(self, mode=False,file=''):
      """
      计算类实例所抽象出的项目（边界）的财务现金流和资本金现金流序列。

      输入参数：
      ----------
        mode: bool, default = False
          中间计算结果写入excel表格标识，若为True，则将中间计算结果输出到名字为file的excel文件中；
          若为False，则中间计算结果不输出；默认值为 Fasle，即默认不输出中间结果。

        file: str, default = ''
          中间结果输出文件名称，与 mode 取值相关联，默认值为''（空字符串）

      返回结果：
      ----------
        (finance_flow,capital_flow): (np.array<operate_period>,np.array<operate_period>)
          财务现金流量表和资本金现金流量表组成的元表，每个财务现金流量表和资本金流量表数据长度为运营期长（运营年数，含建设期）

      备注：
      ----------
        1. 本方法是类对象的核心算法，会涉及到较大量的有效中间计算结果，需梳理好临时变量，以便能写入excel表；
        2. 注意临时变量的分类和初始化工作。
      """
      pass


    @staticmethod
    def com_payback(cash_array):
      """
      根据现金流量数组，计算对应的回收期。

      输入参数：
      -----------
        cash_array: np.array<>
          现金流量数组，一维 np.array 数组
      
      返回结果：
      ----------
        payback_period: float
          与现金流量表对应的项目某种回收期，单位为“年”
        
      备注：
      ----------
        1. 为扩大方法的使用范围，将方法设置为类方法；
        2. 第一阶段暂不考虑输入参数无效的检查和处理；
        3. 注意对特殊情况，即项目回收期无限大，即项目无法收回投资的处理。

      """
      pass


    @staticmethod
    def com_irr(cash_array):
      """
      根据输入的现金流量数组，计算对应的内部收益率。

      输入参数：
      ----------
        cash_array: np.array<>
          现金流量数组，一维 np.array 数组

      返回结果：
      ----------
        irr: float
          现金流量数组所对应的项目某个内部收益率

      备注：
      ----------
        1. 为扩大方法的使用范围，将方法设置为类方法；
        2. 第一阶段暂不考虑输入参数无效的检查和处理；
        3. 注意极端情况的考虑。
      """
      pass


    @staticmethod
    def com_present(cash_array,discount_rate=0.05):
      """
      根据所给的现金流量数组和折现率，计算对应的项目净现值。

      输入参数：
      ----------
        cash_array: np.array<>
          现金流量数组，一维 np.array 数组

        discount_rate: float
          折现率，默认值为 5 %

      返回结果：
      ----------
        present_value: float
          与所给的现金流量数组和折现率对应的项目净现值
      
      备注：
      -----------
        1. 为扩大方法的使用范围，将方法设置为类方法；
        2. 第一阶段暂不考虑输入参数无效的检查和处理；
        3. 注意特殊情况的考虑。       

      """
      pass


    @staticmethod
    def com_lcoe(cost_array,total_power,discount_rate):
      """
      根据所给的总费用数组、总发电量和折现率，计算对应的LCOE（平准化度电成本）。

      输入参数：
      ----------
        cost_array: np.array<>
          项目总费用流量数组，一维 np.array 数组

        total_power: float
          运营期内总发电量

        discount_rate: float
          折现率

      返回结果：
      ----------
        lcoe: float
          对应所给总费用流量数组、总发电量和折现率的平准化度电成本

      备注：
      ----------
        1. 为扩大方法的使用范围，将方法设置为类方法；
        2. 第一阶段暂不考虑输入参数无效的检查和处理；
        3. 注意特殊情况的考虑。 

      """
      pass


if __name__ == "__main__":
    finance = Finance()
    finance.capacity=10.0
    finance.com_finance()
    print(finance.capacity)