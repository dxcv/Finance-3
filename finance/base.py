#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   base.py
@Time    :   2020/11/30 17:21:38
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# 发电类工程项目财务评价：基础模块

import numpy as np
import numpy_financial as npf
import math

# 各省燃煤发电标杆上网电价
Price = {'Beijing':0.3598,'Tianjin':0.3655,
         'Jibei':0.372,'Jinan':0.3644,
         'Shanxi':0.332,'Shandong':0.3949,
         'Shanghai':0.4155,'Jiangsu':0.391,
         'Zhejiang':0.4153,'Anhui':0.3844,
         'Fujian':0.3932,'Jiangxi':0.4143,
         'Hubei':0.4161,'Hunan':0.45,
         'Henan':0.3779,'Sichuan':0.4012,
         'Chongqing':0.3964,'Heilongjiang':0.374,
         'Liaoning':0.3749,'Jilin':0.3731,
         'Mengdong':0.3035,'Mengxi':0.2829,
         'Shanxi':0.3545,'Gansu':0.3078,
         'Ningxia':0.2595,'Qinghai':0.3247,
         'Xinjiang':0.25,'Xizang':0.4993,
         'Guangxi':0.4207,'Yunnan':0.3358,
         'Guizhou':0.3515,'Hainan':0.4298,
         'Guangdong':0.4530}

class Finance(object):
    """ 项目财务分析主类
    本类主要实现新能源项目财务分析过程的抽象封装，
    包括对应一次财务评价的项目边界参数、核心算法。

    成员变量：
    ----------
        capacity: float, default = 100.0
            装机容量，单位为“万kW”，默认值为 100 万 kW
        
        aep: float, default = 2500.0
            年发电量（annual energy product），单位为“小时”（年等效满发上网小时数），默认值为风电的2500小时

        static_investment: float, default = 500000.0
            项目静态总投资，单位为“万元”，默认值为风电投资 5000元/kW * 100万kW

        price: float, default = 0.2829
            含税上网电价，单位为“元/度”，默认值为蒙西燃煤标杆上网电价

        equipment_cost: float, default = 0.0
            设备购置费，单位为“万元”，默认值为 0.0，此时在计算时动态给出其值 = 静态总投资 * equipment_ratio
        
        equipment_ratio: float, default = 0.7
            设备购置费占静态总投资的比例，默认值为 0.7
            
        install_cost: float, default = 0.0
            设备安装费，单位为“万元”，默认值为 0.0，此时在计算时动态给出其值 = 静态总投资 * install_ratio
        
        install_ratio: float, default = 0.07
            设备安装费占静态总投资的比例，默认值为 0.07
            
        build_cost: float, default = 0.0
            建筑工程费，单位为“万元”，默认值为 0.0，此时在计算时动态给出其值 = 静态总投资 * build_ratio
        
        build_ratio: float, default = 0.13
            建筑工程费占静态总投资的比例，默认值为 0.13
            
        other_cost: float, default = 0.0
            其它费用，单位为“万元”，默认值为 0.0，此时在计算时动态给出其值 = 静态总投资 * other_ratio
        
        other_ratio: float, default = 0.1
           其它费用占静态总投资的比例，默认值为 0.1

        capital_ratio: float, default = 0.20
            资本金比例，默认值为公司现值 20 %

        working_ratio: float, default = 0.3
            流动资金资本金比例，默认值为 30 %

        loan_rate: float, default = 0.046
            长期贷款利率，默认值为现阶段融资成本 4.6 %

        working_rate: float, default = 0.0435
            流动资金贷款利率，默认值为 4.35 %
        
        rate_discount: float, default = 1.0
            长期贷款利率折扣，默认值 100 %，即无折扣

        income_tax_rate: float, default = 0.25
            所得税税率（income tax rate），默认值为 25 %

        vat_rate: float, default = 0.13
            增值税税率（value-added tax rate），默认值为 13 %

        vat_refund_rate: float, default = 0.5
            增值税退税比率（vat refund rate），默认值为风电的 50 %（光伏为 0.0）

        build_tax_rate: float, default = 0.05
            城建税税率，默认值为 5 %

        edu_surcharge_rate: float, default = 0.05
            教育费及附加费率，默认值为 5 %  

        workers: integer, default = 25
            员工人数，默认值为 25 人

        labor_cost: float, default = 16
            人均人工成本，单位为“万元/年·人”，默认值为16万元/年·人（含60%的福利费）

        in_repair_rate: float, default = 0.005
            质保期内修理费率（repair costs rate during the warranty period），默认值为风电的 0.5 %（光伏为 0.2%）

        out_repair_rate: float, default = 0.015
            质保期外修理费率（Out-of-warranty repair costs rate），默认值为风电的 1.5 %（光伏为 0.5%）

        warranty: integer, default = 5
            质保期，单位为“年”，默认值为 5 年
            
        depreciation_period: integer, default = 20
            折旧年限，单位为“年”，默认值为 20 年

        insurance_rate: float, default = 0.0025
            保险费率，默认值为 0.25 %

        material_quota: float, default = 10.0
            单位材料费，单位为“元/kW”，默认值为 10.0 元/kW

        other_quota: float, default = 30.0
            其它费用定额，单位为“元/kW”，默认值为 30.0 元/kW

        working_quota: float, default = 30.0
            （铺底）流动资金定额，单位为“元/kW”，默认值为 30.0 元/kW

        provident_rate: float, default = 0.1
            盈余公积提取比例（withdrawal ratio of surplus reserve），默认值为 10 %

        build_period: float, default = 1.0
            建设期，单位为“年”，默认值为 1.0，即 1 年，建设期也会有不满一年的小数存在

        operate_period: integer, default = 20
            经营期（operate period），不含建设期，单位为“年”，默认值为风电的 20 年（光伏25年）

        loan_period: integer, default = 15
            （长期贷款）借款期，单位为“年”，默认值为 15 年

        grace_period: integer, default = 1
            （长期贷款）宽限期，单位为“年”，默认值为 1 年

        residual_rate: float, default = 0.05
            残值率，默认值为 5 %
            
        ### 三个辅助性的流量表单
        cost_list: list<double>, default = []
            成本费辅助流量列表，单位为万元（在程序中动态初始化）
            
        cash_list: list<double>, default = []
            项目现金流量辅助列表，单位为万元（在程序中动态初始化）
            
        cap_list: list<double>, default = []
            资本金现金流量辅助列表，单位为万元（在程序中动态初始化）          
    
    备注：
    ----------
        1. 第一阶段版本暂按照“等额本金”的方式测算，“等额本息”的模式后续再行补充；
        2. 第一阶段版本仅考虑发电类工程项目的收益测算，其它非电类能源项目的测算逻辑后续再行添加；
        3. 第一阶段一些细节暂做概化（如造价构成、人员工资构成等），后续根据需要进行展开；
        
    """

    def __init__(self, capacity=100.0, aep=2500.0, static_investment=500000.0,
                 price=0.2829, capital_ratio=0.20, working_ratio=0.3, equipment_cost=0.0, equipment_ratio=0.7,
                 install_cost=0.0,install_ratio=0.07, build_cost=0.0, build_ratio=0.13, other_cost=0.0, other_ratio=0.1,
                 loan_rate=0.046, working_rate=0.0435, rate_discount=1.0, income_tax_rate=0.25, build_tax_rate=0.05,
                 vat_rate=0.13, vat_refund_rate=0.5, edu_surcharge_rate=0.05,workers=25, labor_cost=16.0, in_repair_rate=0.005,
                 out_repair_rate=0.015, warranty=5.0, depreciation_period=20,insurance_rate=0.0025, material_quota=10.0,
                 other_quota=30.0, working_quota=30.0, provident_rate=0.1, operate_period=20, build_period=1.0, loan_period=15, 
                 grace_period=1, residual_rate=0.05, cost_list=[], cash_list=[], cap_list=[]):
      """
      初始化类变量
      """
      self.capacity = capacity
      self.aep = aep
      self.static_investment = static_investment
      self.price = price
      self.capital_ratio = capital_ratio
      self.working_ratio = working_ratio
      self.equipment_cost = equipment_cost
      self.equipment_ratio = equipment_ratio
      self.install_cost = install_cost
      self.install_ratio = install_ratio
      self.build_cost = build_cost
      self.build_ratio = build_ratio
      self.other_cost = other_cost
      self.other_ratio = other_ratio
      self.loan_rate = loan_rate
      self.working_rate = working_rate
      self.rate_discount = rate_discount
      self.income_tax_rate = income_tax_rate
      self.vat_rate = vat_rate
      self.vat_refund_rate = vat_refund_rate
      self.build_tax_rate = build_tax_rate
      self.edu_surcharge_rate = edu_surcharge_rate
      self.workers = workers
      self.labor_cost = labor_cost
      self.in_repair_rate = in_repair_rate
      self.out_repair_rate = out_repair_rate
      self.warranty = int(warranty)
      self.depreciation_period = int(depreciation_period)
      self.insurance_rate = insurance_rate
      self.material_quota = material_quota
      self.other_quota = other_quota
      self.working_quota = working_quota
      self.provident_rate = provident_rate
      self.build_period = build_period
      self.operate_period = operate_period
      self.loan_period = loan_period
      self.grace_period = grace_period
      self.residual_rate = residual_rate
      self.cost_list = cost_list
      self.cash_list = cash_list
      self.cap_list = cap_list

    def com_finance(self, mode=False):
      """
      计算类实例所抽象出的项目（边界）的（财务、资本金等）现金流序列。

      输入参数：
      ----------
        mode: bool, default = False
          财务计算过程结果（表）返回标识，若为True，则将财评过程结果 com_result 返回；
          若为False，则结果不返回；默认值为 Fasle，即默认不返回财评过程结果。

      返回结果：
      ----------
        1. 若 mode 为 False：
        (pre_pro_netflow, after_pro_netflow, cap_netflow): (np.array<float>,np.array<float>,np.array<float>)
          税前财务现金流量、税后财务现金流量和资本金现金流量组成的元表，每个流量序列不含总计值
        2. 若 mode 为 True:
        (pre_pro_netflow, after_pro_netflow, cap_netflow, com_result): (np.array<float>,np.array<float>,np.array<float>,list)
          前三个参数同上，com_result 为财评过程数据表，三维列表[表页[表单]]

      备注：
      ----------
        1. 本方法是类对象的核心算法，会涉及到较大量的有效中间计算结果，需梳理好临时变量，以便能将结果输出；
        2. 注意临时变量的分类和初始化工作；
        3. 第一阶段默认建设期为 1 年，运营期（含建设期）为 21 年，后续再行扩充可变建设期和运营期。
      """
      ################################################################################
      ## 辅助标签变量
      build_cells = math.ceil(self.build_period)  # 建设期列表长度（整年数）
      row_cells = self.operate_period + build_cells + 1  # 序列长度（运营期+建设期+总计）
      ################################################################################
      ## 投资计划与资金筹措
      total_investment = np.zeros(row_cells)  # 总投资序列  “万元”
      build_investment = np.zeros(row_cells)  # 建设投资序列  “万元”
      build_interest = np.zeros(row_cells)  # 建设期利息序列  “万元”
      working_capital = np.zeros(row_cells)  # 流动资金序列  “万元”
      finance = np.zeros(row_cells)  # 资金筹措序列  “万元”
      capital = np.zeros(row_cells)  # 资本金序列  “万元”
      debt = np.zeros(row_cells)  # 总债务序列  “万元”
      long_loan = np.zeros(row_cells)  # 长期贷款序列  “万元”
      working_loan = np.zeros(row_cells)  # 流动资金贷款序列  “万元”
      ################################################################################
      ## 总成本费用估算
      material = np.zeros(row_cells)  # 外购材料费序列  “万元”
      wage = np.zeros(row_cells)  # 工资和福利序列  “万元”
      maintenance = np.zeros(row_cells)  # 维修费序列  “万元”
      insurance = np.zeros(row_cells)  # 保险费序列  “万元”
      other_expense = np.zeros(row_cells)  # 其它费用支出序列  “万元”
      operate_cost = np.zeros(row_cells)  # 经营成本序列  “万元”
      depreciation = np.zeros(row_cells)  # 折旧费序列  “万元”
      amortization = np.zeros(row_cells)  # 摊销费序列  “万元”
      interest = np.zeros(row_cells)  # 利息支出序列  “万元”
      fix_cost = np.zeros(row_cells)  # 固定成本序列  “万元”
      var_cost = np.zeros(row_cells)  # 可变成本序列  “万元”
      total_cost = np.zeros(row_cells)  # 总成本费用序列  “万元”
      self.cost_list = np.zeros(row_cells)  # 成本费用辅助流量表单  “万元”
      ################################################################################      
      ## 借款还本付息计划
      long_opening = np.zeros(row_cells)  # 长贷期初余额序列 “万元”
      long_return = np.zeros(row_cells)  # 当期还本付息序列  “万元”
      long_principal = np.zeros(row_cells)  # 当期还本序列  “万元”
      long_interest = np.zeros(row_cells)  # 当期付息序列  “万元”
      long_ending = np.zeros(row_cells)  # 长贷期末余额序列  “万元”
      working_interest = np.zeros(row_cells)  # 当期付息序列  “万元”
      working_principal = np.zeros(row_cells)  # 流动资金还本序列  “万元”
      working_return = np.zeros(row_cells)  # 流动资金还本付息序列  “万元”
      total_return = np.zeros(row_cells)  # 当期还本付息总计序列  “万元”
      ################################################################################
      ## 利润和利润分配
      power =np.zeros(row_cells)  # 发电量序列
      income = np.zeros(row_cells)  # 营业收入序列  “万元”
      vat = np.zeros(row_cells)  # 增值税序列
      intax_balance = np.zeros(row_cells)  # 进项税抵扣余额序列  “万元”
      operate_tax = np.zeros(row_cells)  # 营业税金及附加序列  “万元”
      build_tax = np.zeros(row_cells)  # 城建税序列  “万元”
      edu_surcharge = np.zeros(row_cells)  # 教育费附加序列  “万元”
      subside = np.zeros(row_cells)  # 补贴收入序列  “万元”
      vat_return = np.zeros(row_cells)  # 增值税即征即退  “万元”
      vat_turn =np.zeros(row_cells)  # 增值税转型（销项税额）序列  “万元”
      profit = np.zeros(row_cells)  # 利润总额序列  “万元”
      offset_loss = np.zeros(row_cells)  # 弥补以前年度亏损序列  “万元”
      tax_income = np.zeros(row_cells)  # 应纳税所得额序列  “万元”
      income_tax = np.zeros(row_cells)  # 所得税序列  “万元”
      net_profit = np.zeros(row_cells)  # 净利润序列  “万元”
      provident = np.zeros(row_cells)  # 法定盈余公积金序列  “万元”
      distribute_profit = np.zeros(row_cells)  # 可供投资者分配的利润序列  “万元”
      ebit = np.zeros(row_cells)  # 息税前利润（profit before interest and tax)序列  “万元”
      ################################################################################     
      ## 项目投资现金流量
      pro_inflow = np.zeros(row_cells)  # 项目现金流入序列  “万元”
      recover_asset = np.zeros(row_cells)  # 回收固定资产余值序列  “万元”
      recover_pro_working = np.zeros(row_cells)  # 回收项目流动资金序列  “万元”
      pro_outflow = np.zeros(row_cells)  # 项目现金流出序列  “万元”
      pre_pro_netflow = np.zeros(row_cells)  # 所得税前项目净现金流量  “万元”
      after_pro_netflow = np.zeros(row_cells)  # 所得税后项目净现金流量  “万元”
      self.cash_list = np.zeros(row_cells)  # 项目现金流辅助流标表单  “万元”
      ################################################################################
      # 项目资本金现金流量
      cap_inflow = np.zeros(row_cells)  # 现金流入（资本金）序列  “万元”
      recover_cap_working = np.zeros(row_cells)  # 回收流动资金（资本金）序列  “万元”
      cap_outflow = np.zeros(row_cells)  # 现金流出（资本金）序列  “万元”
      cap_netflow = np.zeros(row_cells)  # 资本金净现金流量  “万元”
      self.cap_list = np.zeros(row_cells)  # 资本金现金流量辅助流量表单  “万元”
      ################################################################################
      ################################################################################
      ## 投资计划与资金筹措（暂按建设期为 1 年的标准考虑）
      build_investment[1] = self.static_investment  # 建设期（首年）投资
      build_interest[1] = build_investment[1] * self.loan_rate * self.rate_discount / 2  # 建设期（首年）利息
      working_capital[build_cells + 1] = self.capacity * self.working_quota  # 运营期首年铺底流动资金
      build_investment[0] = np.sum(build_investment)  # 建设投资总额
      build_interest[0] = np.sum(build_interest)  # 建设利息总额
      working_capital[0] = np.sum(working_capital)  # 流动资金总额
      total_investment = build_investment + build_interest + working_capital  # 总投资序列（含建设期和运营首年）
      capital[1] = total_investment[1] * self.capital_ratio  # 建设期（首年）资本金
      capital[build_cells + 1] = total_investment[build_cells + 1] * self.working_ratio  # 运营首年流动资金资本金
      long_loan[1] = total_investment[1] - capital[1]  # 建设期（首年）长期贷款
      working_loan[build_cells + 1] = total_investment[build_cells + 1] - capital[build_cells + 1]  # 运营首年流动资金贷款
      capital[0] = np.sum(capital)  # 资本金总额
      long_loan[0] = np.sum(long_loan)  # 长期贷款总额
      working_loan[0] = np.sum(working_loan)  # 流动资金贷款总额
      debt = total_investment - capital  # 总贷款序列（含建设期和运营首年）
      finance = capital + debt  # 总筹款序列（含建设期和运营首年）
      ################################################################################
      ################################################################################
      ## 临时辅助性变量
      if self.equipment_ratio != 0.0:
            self.equipment_cost = self.static_investment * self.equipment_ratio
      if self.install_ratio != 0.0:
            self.install_cost = self.static_investment * self.install_ratio
      if self.build_ratio != 0.0:
            self.build_cost = self.static_investment * self.build_ratio
      if self.other_ratio != 0.0:
            self.other_cost = self.static_investment * self.other_ratio
            
      vat_deduction = self.equipment_cost / (1 + self.vat_rate) * self.vat_rate + (
          self.build_cost + self.install_cost) / (1 + 0.09) * 0.09 + self.other_cost / (1 + 0.06) * 0.06  # 增值税进项税抵扣额  “万元”
      fix_assets = total_investment[1] - vat_deduction  # 固定资产价值  “万元”
#      output_vat = self.capacity * self.aep * self.price * self.vat_rate / (1 + self.vat_rate)  # 增值税销项税  “万元”
      ################################################################################
      ################################################################################
      ## 总成本费用估算
      material[build_cells + 1 :] = self.capacity * self.material_quota  # 材料费序列
      wage[build_cells + 1 :] = self.workers * self.labor_cost  # 工资和福利序列
      maintenance[build_cells + 1 : build_cells + 1 + self.warranty] = fix_assets * self.in_repair_rate  # 质保期内维修费序列
      maintenance[build_cells + 1 + self.warranty :] = fix_assets * self.out_repair_rate  # 质保期外维修费序列
      insurance[build_cells + 1 :] = fix_assets * self.insurance_rate  # 保险费序列
      other_expense[build_cells + 1 :] = self.capacity * self.other_quota  # 其它费用序列
      depreciation[build_cells + 1:build_cells + 1 + self.depreciation_period] = fix_assets * \
          (1 - self.residual_rate) / self.depreciation_period  # 折旧费序列
      depreciation[0] = np.sum(depreciation)  # 总折旧费
      maintenance[0] = np.sum(maintenance)  # 总维修费
      wage[0] = np.sum(wage)  # 总工资和福利费
      insurance[0] = np.sum(insurance)  # 总保险费
      material[0] = np.sum(material)  # 总材料费
      other_expense[0] = np.sum(other_expense)  # 总其它费
      amortization[0] = np.sum(amortization)  # 总摊销费
      var_cost = material  # 可变成本序列
      operate_cost = maintenance + wage + insurance + material + other_expense + self.cost_list  # 运营成本序列
      ################################################################################
      ################################################################################
      ## 借款还本付息计划
      long_principal[build_cells + 1 : build_cells + self.loan_period + 1] = long_loan[1] / self.loan_period  # 采用等额本金的方法还款
      for i in range(self.loan_period):
        long_opening[build_cells + i + 1] = long_loan[1] - i * long_principal[build_cells + i]  # 期初贷款余额序列
      long_ending[build_cells+1 : build_cells + self.loan_period] = long_opening[build_cells + 2 : build_cells + self.loan_period + 1]  # 期末贷款余额序列
      long_interest = long_opening * self.loan_rate * self.rate_discount  # 应付利息序列
      long_interest[0] = np.sum(long_interest)  # 付息总额
      long_principal[0] = np.sum(long_principal)  # 还本总额
      long_return = long_principal + long_interest  # 还本付息序列
      working_interest[build_cells + 1 :] = working_loan[build_cells + 1] * self.working_rate  # 流动资金应付利息序列
      working_principal[row_cells - 1] = working_loan[build_cells + 1]  # 流动资金还本（最后一年返还）
      working_interest[0] = np.sum(working_interest)  # 流动资金利息合计
      working_principal = np.sum(working_principal)  # 流动资金还本合计
      working_return = working_interest + working_principal  # 流动资金还本付息合计
      interest = long_interest + working_interest  # 总利息支出序列
      total_return = long_return + working_return  # 当期还本付息总计序列
      total_cost = depreciation + operate_cost + amortization + interest  # 总成本费用序列
      fix_cost = total_cost - var_cost  # 固定成本序列
      ################################################################################
      ################################################################################
      ## 利润和利润分配
      power[build_cells + 1] = self.capacity * self.aep / 0.93112
      power[build_cells + 2] = power[build_cells + 1]*0.98
      for i in range(self.operate_period-2):
        power[build_cells + 3 + i] = power[build_cells + 2] * (0.9755-i * 0.0045)  # 发电量序列
      income[build_cells + 1:] = power[build_cells+1:] * self.price / (1 + self.vat_rate)  # 运营期营业收入序列
      income[0] = np.sum(income)  # 运营期营业收入总计
      vat[build_cells+1:] = income[build_cells + 1:] * self.vat_rate/(1+self.vat_rate)  # 增值税序列
      vat[0] = np.sum(vat)  # 增值税总计
      for i in range(self.operate_period):
        if i == 0:
          intax_balance[build_cells + 1 + i] = vat_deduction  # 进项税抵扣余额序列
        else:
          intax_balance[build_cells + 1 + i] = intax_balance[build_cells + i] - vat[build_cells+i]
      for i in range(self.operate_period):
        if intax_balance[build_cells + 1 + i] <= 0:
          build_tax[build_cells + 1 + i] = vat[build_cells+1+i] * self.build_tax_rate  # 城建税序列（设备进项税抵扣完后）
          edu_surcharge[build_cells + 1 + i] = vat[build_cells + 1+i] * self.edu_surcharge_rate  # 教育费及附加序列
        elif intax_balance[build_cells + 1 + i] > 0 and intax_balance[build_cells + 1 + i] - vat[build_cells+1+i] <= 0:
          build_tax[build_cells + 1 + i] = (vat[build_cells + 1 + i] - intax_balance[build_cells + 1 + i]) * self.build_tax_rate  # 城建税序列（设备进项税即将不足抵扣）
          edu_surcharge[build_cells + 1 + i] = (vat[build_cells + 1 + i] - intax_balance[build_cells + 1 + i]) * self.edu_surcharge_rate  # 教育费及附加序列
        else:
          build_tax[build_cells + 1 + i] = 0  # 城建税序列（设备进项税未抵扣完）
          edu_surcharge[build_cells + 1 + i] = 0  # 教育费及附加序列
      build_tax[0] = np.sum(build_tax)  # 城建税总计
      edu_surcharge[0] = np.sum(edu_surcharge)  # 教育费及附加总计
      operate_tax = build_tax + edu_surcharge  # 营业税金及附加
      vat_return = build_tax * self.vat_refund_rate / self.build_tax_rate  # 增值税即征即退序列
      for i in range(build_cells + 1, self.operate_period):  # 计算销项税序列
        if intax_balance[i] < 0:
          vat_turn[i] = 0
        elif intax_balance[i] >= vat[i]:
          vat_turn[i] = vat[i]
        else:
          vat_turn[i] = intax_balance[i]
      vat_turn[0] = np.sum(vat_turn)  # 增值税转型（销项税额）总计
      subside = vat_return + vat_turn  # 补贴收入序列
      profit = income - operate_tax - total_cost + vat_return  # 利润总额序列
      tax_income = profit - offset_loss  # 应纳税所得额序列
      for i in range(self.operate_period):  # 所得税序列计算
        if i < 3:
          income_tax[build_cells + 1 + i] = 0  # “三免”
        elif tax_income[build_cells + 1 + i] <= 0:
          income_tax[build_cells + 1 + i] = 0  # 应税所得为负值
        elif i < 6:
          income_tax[build_cells + 1 + i] = tax_income[build_cells + 1 + i] * self.income_tax_rate / 2  # “三减半”
        else:
          income_tax[build_cells + 1 + i] = tax_income[build_cells + 1 + i] * self.income_tax_rate  # 正常所得税序列
      income_tax[0] = np.sum(income_tax)  # 所得税总计
      net_profit = profit - income_tax  # 净利润序列
      provident = net_profit * self.provident_rate  # 法定盈余公积金序列
      distribute_profit = net_profit - provident  # 可供投资者分配的利润序列
      ebit = profit + interest  # 息税前利润序列
      ################################################################################
      ################################################################################
      ## 项目投资现金流量
      recover_asset[build_cells + self.operate_period] = fix_assets * self.residual_rate  # 回收固定资产余值序列
      recover_pro_working[build_cells + self.operate_period] = working_capital[build_cells + 1]  # 回收项目流动资金序列
      recover_asset[0] = np.sum(recover_asset)  # 回收固定资产总计
      recover_pro_working[0] = np.sum(recover_pro_working)  # 回收项目流动资金总计
      pro_inflow = income + subside + recover_asset + recover_pro_working  # 项目现金流入序列
      pro_outflow = build_investment + working_capital + operate_cost + operate_tax  # 项目现金流出序列  “万元”
      pre_pro_netflow = pro_inflow - pro_outflow + self.cash_list  #  所得税前项目净现金流量  “万元”
      after_pro_netflow = pre_pro_netflow - income_tax  # 所得税后项目净现金流量  “万元”
      ################################################################################
      ################################################################################
      ## 项目资本金现金流量
      recover_cap_working[[0, build_cells + self.operate_period]] = working_capital[build_cells + 1] * self.working_ratio  # 回收流动资金（资本金）
      cap_inflow = income + subside + recover_asset + recover_cap_working  # 现金流入序列（资本金）
      cap_outflow = capital + long_principal + interest + operate_cost + operate_tax + income_tax # 现金流出序列（资本金）
      cap_netflow = cap_inflow - cap_outflow + self.cap_list  # 净现金流量（资本金）
      ################################################################################
      ################################################################################
      ## 处理 mode 为 TRUE 情况（即需要计算表格输出）
      if mode == True:
        # 项目总投资使用计划与资金筹措表
        investment_finance = [total_investment[: build_cells + 2], build_investment[: build_cells + 2], build_interest[: build_cells + 2], working_capital[: build_cells + 2],
                              finance[: build_cells + 2], capital[: build_cells + 2], debt[: build_cells + 2], long_loan[: build_cells + 2], working_loan[: build_cells + 2]]  
        
        # 总成本费用估算表
        cost_finance = [material, wage, maintenance, insurance, other_expense, operate_cost,
                        depreciation, amortization, interest, total_cost, var_cost, fix_cost]
        
        # 借款还本付息计划表
        return_finance = [long_loan, long_opening, long_return, long_principal, long_interest, long_ending, working_loan, working_loan, working_return, working_principal, working_interest,
                          working_loan-working_principal, long_loan+working_loan, long_opening+working_loan, total_return, long_principal+working_principal, long_interest+working_interest]
        
        # 利润和利润分配表
        profit_finance = [income, operate_tax, build_tax, edu_surcharge, total_cost, subside,
                          vat_return, vat_turn, profit, offset_loss, tax_income, income_tax, net_profit, provident, ebit]

        # 项目现金流量表
        pro_flow = [pro_inflow, income, subside, recover_asset, recover_pro_working, pro_outflow, build_investment,
                    working_capital, operate_cost, operate_tax, pre_pro_netflow, income_tax, after_pro_netflow]
        
        # 项目资本金现金流量表
        cap_flow = [cap_inflow, income, subside, recover_asset, recover_cap_working, cap_outflow,
                    capital, long_return, interest, operate_cost, operate_tax, income_tax, cap_netflow]
        
        # 合并过程结果表（项目总投资使用计划与资金筹措表，总成本费用估算表，借款还本付息计划表，利润与利润分配表，项目现金流量表，项目资本金流量表等）
        com_result = [investment_finance, cost_finance, return_finance, profit_finance, pro_flow, cap_flow]
      ################################################################################
      ################################################################################
      # 返回结果数组（元组）（总计值不再列入返回的流量表）
      if mode:
        return pre_pro_netflow[1:], after_pro_netflow[1:], cap_netflow[1:], com_result
      else:
        return pre_pro_netflow[1:], after_pro_netflow[1:], cap_netflow[1:]

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
      return npf.irr(cash_array)

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
      return np.npv(discount_rate,cash_array)

    @staticmethod
    def com_lcoe(cost_array, power, discount_rate):
      """
      根据所给的总费用数组、总发电量和折现率，计算对应的LCOE（平准化度电成本）。

      输入参数：
      ----------
        cost_array: np.array<>
          项目总费用流量数组，一维 np.array 数组

        power: float
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

    # 实例化类对象，并测验相关算法逻辑
    finance = Finance()
    finance.capacity = 5.0  # 风电场容量，万 kW
    finance.aep = 1800.0  # 风电场年发电量，小时
    finance.price = 0.3799  # 上网电价（含税），元/度
    finance.static_investment = 5000 * finance.capacity  # 静态总投资，万元
    finance.capital_ratio = 0.25  # 资本金比例
    finance.loan_rate = 0.054  # 贷款利率
    finance.workers = int(finance.capacity)
    # 其它参数采用默认值

    # 计算项目的现金流和内部收益率
    pre_pro_netflow, after_pro_netflow, cap_netflow = finance.com_finance() # 计算各现金流
    pre_pro_irr = finance.com_irr(pre_pro_netflow)  # 项目税前 IRR
    after_pro_irr = finance.com_irr(after_pro_netflow)  # 项目税后 IRR
    cap_irr = finance.com_irr(cap_netflow)  # 资本金 IRR

    # 打印结果
    print(pre_pro_irr, after_pro_irr, cap_irr)

    
