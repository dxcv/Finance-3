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
import math


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

        static_investment: float, default = 70000.0
            项目静态总投资，单位为“万元”，默认值为 7000元/kW * 10万kW

        price: float, default = 0.3779
            含税上网电价，单位为“元/度”，默认值为河南燃煤标杆上网电价

        equipment_cost: float, default = 0.0
            设备购置费，单位为“万元”，默认值为 0.0，此时在计算时动态给出其值 = 静态总投资*60%

        capital_ratio: float, default = 0.25
            资本金比例，默认值为公司现值 25 %

        working_capital_ratio: float, default = 0.3
            流动资金资本金比例，默认值为 30 %

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

        material_fee_quota: float, default = 10.0
            单位材料费，单位为“元/kW”，默认值为 10.0 元/kW

        other_fee_quota: float, default = 40.0
            其它费用定额，单位为“元/kW”，默认值为 40.0 元/kW

        working_capital_quota: float, default = 30.0
            （铺底）流动资金定额，单位为“元/kW”，默认值为 30.0 元/kW

        withdraw_rate: float, default = 0.1
            盈余公积提取比例（withdrawal ratio of surplus reserve），默认值为 10 %

        build_period: float, default = 1.0
            建设期，单位为“年”，默认值为 1.0，即 1 年，建设期也会有不满一年的小数存在

        operate_period: integer, default = 21
            经营期（operate period），不含建设期，单位为“年”，默认值为 20 年

        loan_period: integer, default = 15
            （长期贷款）借款期，单位为“年”，默认值为 15 年

        grace_period: integer, default = 1
            （长期贷款）宽限期，单位为“年”，默认值为 1 年

        residual_rate: float, default = 0.05
            残值率，默认值为 5 %
    
    备注：
    ----------
        1. 第一阶段版本暂按照“等额本金”的方式测算，“等额本息”的模式后续再行补充；
        2. 第一阶段版本仅考虑风电项目的收益测算，光伏项目和其它能源项目的测算逻辑后续再行添加；
        3. 第一阶段一些细节暂做概化（如造价构成、人员工资构成等），后续根据需要进行展开；
        
    """

    def __init__(self, capacity=10.0, power=2500.0, static_investment=70000.0,
                 price=0.3779, capital_ratio=0.25, working_capital_ratio=0.3, equipment_cost=0.0,
                 loan_rate=0.054, current_rate=0.06, rate_discount=1.0, income_tax_rate=0.25,
                 vat_rate=0.13, vat_refund_rate=0.5, workers=10, labor_cost=15.5, in_repair_rate=0.005,
                 out_repair_rate=0.01, warranty=2.0, insurance_rate=0.0025, material_fee_quota=10.0,
                 other_fee_quota=40.0, working_capital_quota=30.0, withdraw_rate=0.1, operate_period=20,
                 build_period=1.0, loan_period=15, grace_period=1, residual_rate=0.05):
      """
      初始化类变量
      """
      self.capacity = capacity
      self.power = power
      self.static_investment = static_investment
      self.price = price
      self.capital_ratio = capital_ratio
      self.working_capital_ratio = working_capital_ratio
      if equipment_cost == 0.0:
          self.equipment_cost = static_investment * 0.6
      else:
          self.equipment_cost = equipment_cost
      self.loan_rate = loan_rate
      self.current_rate = current_rate
      self.rate_discount = rate_discount
      self.income_tax_rate = income_tax_rate
      self.vat_rate = vat_rate
      self.vat_refund_rate = vat_refund_rate
      self.workers = workers
      self.labor_cost = labor_cost
      self.in_repair_rate = in_repair_rate
      self.out_repair_rate = out_repair_rate
      self.warranty = warranty
      self.insurance_rate = insurance_rate
      self.material_fee_quota = material_fee_quota
      self.other_fee_quota = other_fee_quota
      self.working_capital_quota = working_capital_quota
      self.withdraw_rate = withdraw_rate
      self.build_period = build_period
      self.operate_period = operate_period
      self.loan_period = loan_period
      self.grace_period = grace_period
      self.residual_rate = residual_rate

    def com_finance(self, mode=False, file=''):
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
        2. 注意临时变量的分类和初始化工作；
        3. 第一阶段默认建设期为 1 年，运营期（含建设期）为 21 年，后续再行扩充可变建设期和运营期。
      """

      # 重要中间变量（数组）
      ## 投资计划与资金筹措
      build_cells = math.ceil(self.build_period)  # 建设期列表长度（整年数）
      row_cells = build_cells + 2  # 数组长度（建设期+总计+首年运行）
      total_investment = np.zeros(row_cells)  # 总投资
      construct_investment = np.zeros(row_cells)  # 建设投资
      construct_interest = np.zeros(row_cells)  # 建设期利息
      working_capital = np.zeros(row_cells)  # 流动资金
      financing = np.zeros(row_cells)  # 资金筹措
      capital = np.zeros(row_cells)  # 资本金
      loan = np.zeros(row_cells)  # 贷款
      long_loan = np.zeros(row_cells)  # 长期贷款
      working_loan = np.zeros(row_cells)  # 流动资金贷款

      ## 总成本费用估算
      row_cells = self.operate_period + build_cells + 1  # 数组长度（运营期+建设期+总计）
      depreciation = np.zeros(row_cells)  # 折旧费
      maintenance = np.zeros(row_cells)  # 维修费
      wage = np.zeros(row_cells)  # 工资和福利
      insurance = np.zeros(row_cells)  # 保险费
      material = np.zeros(row_cells)  # 材料费
      amortization = np.zeros(row_cells)  # 摊销费
      interest = np.zeros(row_cells)  # 利息支持
      other_expense = np.zeros(row_cells)  # 其它费用支出
      fix_cost = np.zeros(row_cells)  # 固定成本
      var_cost = np.zeros(row_cells)  # 可变成本
      total_cost = np.zeros(row_cells)  # 总成本费用
      operate_cost = np.zeros(row_cells)  # 经营成本
      
      # 借款还本付息计划
      long_loan=np.zeros(row_cells)  # 长期贷款
      long_opening_balance = np.zeros(row_cells)  # 长贷期初余额
      long_debt_service = np.zeros(row_cells)  # 当期还本付息
      long_pay_principal = np.zeros(row_cells)  # 当期还本
      long_pay_interest = np.zeros(row_cells)  # 当期付息
      long_ending_balance = np.zeros(row_cells)  # 长贷期末余额
      short_loan = np.zeros(row_cells)  # 流动资金（短期）贷款
       

      # 临时辅助性变量
      fix_assets = total_investment[1] - \
          self.equipment_cost/(1+self.vat_rate)*self.vat_rate  # 固定资产数值

      # 返回结果变量（数组）
      finance_flow = np.zeros(row_cells)
      capital_flow = np.zeros(row_cells)

      # 计算各中间变量值
      ## 投资计划与资金筹措（暂按建设期为 1 年的标准考虑
      construct_investment[1] = self.static_investment  # 建设期（首年）投资
      construct_interest[1] = self.static_investment * self.loan_rate * \
          (1 - self.capital_ratio) / \
          (2 - self.loan_rate * (1 - self.capital_ratio)) # 建设期（首年）利息
      working_capital[2] = self.capacity * self.working_capital_quota  # 运营期首年铺底流动资金
      construct_investment[0] = np.sum(construct_investment)  # 建设投资总额
      construct_interest[0] = np.sum(construct_interest)  # 建设利息总额
      working_capital[0] = np.sum(working_capital)  # 流动资金总额
      total_investment = construct_investment + construct_interest + working_capital  # 总投资序列（含建设期和运营首年）

      capital[1] = total_investment[1] * self.capital_ratio  # 建设期（首年）资本金
      capital[2] = total_investment[2] * self.working_capital_ratio  # 运营首年流动资金资本金
      long_loan[1] = total_investment[1] - capital[1]  # 建设期（首年）长期贷款
      working_loan[2] = total_investment[2] - capital[2]  # 运营首年流动资金贷款
      long_loan[0] = np.sum(long_loan)  # 长期贷款总额
      working_loan[0] = np.sum(working_loan)  # 流动资金贷款总额
      loan = long_loan + working_loan  # 总贷款序列（含建设期和运营首年）
      finance = capital + loan  # 总筹款序列（含建设期和运营首年）

      ## 总成本费用估算
      depreciation[build_cells + 1:] = fix_assets * (1 - self.residual_rate) / self.operate_period  # 折旧费序列
      maintenance[build_cells + 1 : build_cells + 1 + self.warranty] = fix_assets * self.in_repair_rate  # 质保期内维修费序列
      maintenance[build_cells + 1 + self.warranty :] = fix_assets * self.out_repair_rate  # 质保期外维修费序列
      wage[build_cells + 1 :] = self.workers * self.labor_cost  # 工资和福利序列
      insurance[build_cells + 1 :] = fix_assets * self.insurance_rate  # 保险费序列
      material[build_cells + 1 :] = self.capacity * self.material_fee_quota  # 材料费序列
      other_expense[build_cells + 1 :] = self.capacity * self.other_fee_quota  # 其它费用序列
      depreciation[0] = np.sum(depreciation)  # 总折旧费
      maintenance[0] = np.sum(maintenance)  # 总维修费
      wage[0] = np.sum(wage)  # 总工资和福利费
      insurance[0] = np.sum(insurance)  # 总保险费
      material[0] = np.sum(material)  # 总材料费
      other_expense[0] = np.sum(other_expense)  # 总其它费
      amortization[0] = np.sum(amortization)  # 总摊销费
      
      var_cost = material  # 可变成本序列
      operate_cost = maintenance + wage + insurance + material + other_expense  # 运营成本序列
      
      
      # 返回结果数组（元组）
      return finance_flow, capital_flow

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
    def com_present(cash_array, discount_rate=0.05):
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
    def com_lcoe(cost_array, total_power, discount_rate):
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
    finance.capacity = 10.0  # 风电场容量，万 kW
    finance.power = 2500.0  # 风电场年发电量，小时
    finance.price = 0.3779  # 上网电价（含税），元/度
    finance.static_investment = 6800 * 100000  # 静态总投资，元
    finance.capital_ratio = 0.25  # 资本金比例
    finance.loan_rate = 0.054  # 贷款利率
    # 其它参数采用默认值

    # 计算项目的财务现金流和资本金现金流
    finance_flow, capital_flow = finance.com_finance()

    # 打印结果
    print(finance_flow, capital_flow)

    
