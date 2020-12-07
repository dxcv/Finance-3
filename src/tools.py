#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py
@Time    :   2020/12/07 16:17:14
@Author  :   liuzy2020 
@Version :   1.0
@Contact :   liuzy2013@163.com
@WebSite :   https://github.com/path2019
'''
# Start typing your code from here
# 这里是一些基础的工具

import xlsxwriter as xlsw
import numpy as np


def write_excel(data, file='result.xlsx'):
    """
    将 data 列表数据写入到 file（excel）文件中。

    输入参数：
    ----------
        data: list
            列表数据，可以是一~三维，若为一维、二维数据，则直接写入表格中；
                若为三维数据，则第一维设置为表签名（SheetName）
        
        file: str, default = 'result.xlsx'
            写入文件的名称，需包含后缀".xlsx"，默认值为 "result.xlsx"

    返回结果：
    ----------
        status: boolean
            操作返回码，正产返回 True

    备注：
    ----------
        1. 第一阶段暂不考虑非正常的格式和数据问题；
        2. 暂时不考虑表格的格式化问题，包括标题、表头、列头等，后续再行补加。

    """
    # 取得 data 列表维度
    dim = len(np.array(data).shape)

    # 根据不同维度进行表格写入
    try:
        workbook = xlsw.Workbook(file)  # 创建表格缓冲
        if dim == 1:
            sheet = workbook.add_worksheet("Data Result")
            for index in range(len(data)):
                sheet.write(0, index, data[index])
        elif dim == 2:
            sheet = workbook.add_worksheet("Data_Result")
            for i in range(len(data)):
                for j in range(len(data[i])):
                    sheet.write(i, j, data[i][j])
        else:
            for k in range(len(data)):
                # sheet = workbook.add_worksheet('表格 ' + str(k + 1))
                ## 下面一行代码只是目前特殊目的需要，过了这次测算，即用上面一行代替这行
                sheet = workbook.add_worksheet(str((k + 1) * 5) + ' 万 kW')
                for i in range(len(data[k]) + 1):
                    for j in range(len(data[k][i - 1]) + 1):
                        ## 下面这行也是此次特殊测算的需要，过后删除或替换其它表头和列头
                        if i == 0 and j == 0:
                           sheet.write(i, j, '千瓦造价/上网小时') 
                        elif i == 0 and j > 0:
                            sheet.write(i, j, 4950 + j * 50)
                        elif j == 0 and i > 0:
                            sheet.write(i, j, 1750 + i * 50)
                        else:
                            sheet.write(i, j, data[k][i-1][j-1])
        workbook.close()
        return 0
    except Exception as inst:
        return - 1
        

if __name__ == "__main__":
    
    # 代码功能测试
    data_1 = [1, 2, 3, 4]
    data_2 = [data_1, data_1]
    data_3 = [data_2, data_2, data_2]
    
    write_excel(data_1, 'result_1.xlsx')
    write_excel(data_2, 'result_2.xlsx')
    write_excel(data_3, 'result_3.xlsx')
