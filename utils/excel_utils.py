# coding: utf-8

import xlrd


def excel_to_list(excel_file):
    '''处理excel，返回列表
    '''

    book = xlrd.open_workbook(file_contents=excel_file.read())
    sheet = book.sheet_by_index(0)

    dataset = []
    for r in xrange(sheet.nrows):
        col = []
        for c in range(sheet.ncols):
            col.append(sheet.cell(r, c).value)
        dataset.append(col)

    return dataset[1:]
