# -*- coding: utf-8 -*- 
import sys
import pandas as pd
import numpy as np

def report_diff(x):
    return x[0] if x[0] == x[1] else u'{} <-> {}'.format(*x)

#df1 get,#df2 get

df1 = pd.read_excel('test-1.xlsx', 'Sheet1', na_values=['NA'], index_col=0) 
df2 = pd.read_excel('test-2.xlsx', 'Sheet1', na_values=['NA'], index_col=0)


print '*' * 100

my_panel = pd.Panel(dict(df1=df1,df2=df2))
diff_output = my_panel.apply(report_diff, axis=0)


writer = pd.ExcelWriter('my-diff.xlsx', engine='xlsxwriter')
diff_output.to_excel(writer, "changed")
print diff_output

# Get access to the workbook and sheet
workbook = writer.book
worksheet = writer.sheets['changed']

number_rows = len(diff_output.index)
color_range = "A1:L{}".format(number_rows+1)
# Add a format. Light red fill with dark red text.
format1 = workbook.add_format({'bg_color': '#FFE4B5',
                               'font_color': '#0000FF',
                               'bold': 1, 'italic': 1
                               })
format2 = workbook.add_format({'bg_color': '#9999FF',
                               'font_color': '#000000',
                               'bold': 1, 'italic': 1
                               })


#worksheet.conditional_format(color_range, {'type': 'text', 'criteria': 'containing', 'value': '<->', 'format': format1})
worksheet.conditional_format(color_range, {'type': 'text', 'criteria': 'containing', 'value': 'nan <->', 'format': format2})
worksheet.conditional_format(color_range, {'type': 'text', 'criteria': 'containing', 'value': '<-> nan', 'format': format2})
worksheet.conditional_format(color_range, {'type': 'text', 'criteria': 'containing', 'value': '<->', 'format': format1})
writer.save()