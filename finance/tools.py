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


def write_excel(data, sheet_name=[], row_header=[], column_header=[], file='result.xlsx'):
    """
    将 data 列表数据写入到 file（excel）文件中。

    输入参数：
    ----------
        data: list
            列表数据，可以是一~三维，若为一维、二维数据，则直接写入表格中；
                若为三维数据，则第一维设置为表签名（SheetName）

        sheet_name: list<str>, default = ['data']
            表单标签，一维列表，数量应与 data 表单数对应，默认值为 ['data']
        
        row_header: list<str>, default = []
            数据行名，一维列表，数量应与 data 表单行数对应，默认值为 []

        column_header: list<str>, default = []
            数据列名，一维列表，数量应与 data 表单列数对应，默认值为 [] 

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
        if dim == 1:  # 若为一维列表
            if sheet_name:
                sheet = workbook.add_worksheet(sheet_name[0])
            else:
                sheet = workbook.add_worksheet('Data')
            if row_header:
                sheet.write(1, 0, row_header[0])  # 写入行名
            else:
                sheet.write(1, 0, '数据')
            for index in range(len(data)):
                if column_header:
                    sheet.write(0, index + 1, column_header[index])  # 写入列名
                else:
                    sheet.write(0, index + 1, str(index + 1))
                sheet.write(1, index + 1, data[index])  # 写入数据
        elif dim == 2:  # 若为二维列表
            if sheet_name:
                sheet = workbook.add_worksheet(sheet_name[0])
            else:
                sheet = workbook.add_worksheet('Data')
            for i in range(len(data)):
                if row_header:
                    sheet.write(i + 1, 0, row_header[i])  # 写入行名
                else:
                    sheet.write(i + 1, 0, str(i + 1))
                for j in range(len(data[i])):
                    if i == 0:
                        if column_header:
                            sheet.write(i, j + 1, column_header[j])
                        else:
                            sheet.write(i, j + 1, str(j + 1))
                        sheet.write(i + 1, j + 1, data[i][j])
                    else:
                        sheet.write(i + 1, j + 1, data[i][j])
        else:
            for k in range(len(data)):
                if sheet_name:
                    sheet = workbook.add_worksheet(sheet_name[k])  # 表单标签
                else:
                    sheet = workbook.add_worksheet('表格' + str(k + 1))  # 表单标签
                for i in range(len(data[k])):
                    if row_header:
                        sheet.write(i + 1, 0, row_header[i])  # 写入行名
                    else:
                        sheet.write(i + 1, 0, str(i + 1))
                    for j in range(len(data[k][i])):
                        if i == 0:
                            if column_header:
                                sheet.write(i, j + 1, column_header[j])
                            else:
                                sheet.write(i, j + 1, str(j + 1))
                            sheet.write(i + 1, j + 1, data[k][i][j])
                        else:
                            sheet.write(i + 1, j + 1, data[k][i][j])
        workbook.close()
        return 0
    except Exception as inst:
        return - 1
        

if __name__ == "__main__":
    
    # 代码功能测试
    data_1 = [1, 2, 3, 4]
    data_2 = [data_1, data_1]
    data_3 = [data_2, data_2, data_2]
    
    write_excel(data_1, file='result_1.xlsx')
    write_excel(data_2, file='result_2.xlsx')
    write_excel(data_3, file='result_3.xlsx')
