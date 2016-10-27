#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xlrd import open_workbook
import unicodecsv as csv

def get_value(cell):
    data = cell.value
    if (type(data) in [float]):
        try:
            return int(data)
        except ValueError:
            return data
    return data


def extract_csv(client_master_fpath, sheet_names):
    output_fpaths = []

    book = open_workbook(client_master_fpath)
    for sheet_name in sheet_names:
        sheet = book.sheet_by_name(sheet_name)
        output_fpath = '{0}.csv'.format(sheet_name)
        with open(output_fpath, 'wb') as f:
            writer = csv.writer(f)
            for row_index in range(sheet.nrows):
                row = sheet.row(row_index)
                writer.writerow(list(map(lambda x: get_value(x), row)))
            f.seek(-2, os.SEEK_END)
            f.truncate()
            output_fpaths.add(output_fpath)

    return output_fpaths
