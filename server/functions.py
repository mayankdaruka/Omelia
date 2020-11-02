import gspread
from pprint import pprint
from matplotlib import colors
import math
import numpy as np
from value_types import *
import re
# from sympy import *

def add(sheet, arg0, arg1):
    # num and entry
    if(isinstance(arg0, Value) and isinstance(arg1, Entry)):
        addNumEntry(sheet, arg0, arg1)
    # entry and entry
    if(isinstance(arg0, Entry) and isinstance(arg1, Entry)):
        addEntryEntry(sheet, arg0, arg1)
    # num and cell
    if(isinstance(arg0, Value) and isinstance(arg1, Cell)):
        print("Reached here")
        addNumCell(sheet, int(arg0.value), arg1.cell_str)

# works
def addNumCell(sheet, num, cell):
    try:
        val = sheet.acell(cell).value
        cell_update(sheet, cell, num + float(val))
    except TypeError:
        return

def addNumRange(sheet, num, range):
    values_list = sheet.range(range)
    for cell in values_list:
      if len(cell.value) > 0: 
        cell.value = str(int(cell.value) + num)
    sheet.update_cells(values_list)

def addNumEntry(sheet, num, entry):
    try:
      if entry.rowOrCol == "row":
        range1 = str(gspread.utils.rowcol_to_a1(entry, 1))
        addNumRange(sheet, num, str(entry) + ":BA" + str(entry))
      else:
        range1 = str(gspread.utils.rowcol_to_a1(1, entry))
        addNumRange(sheet, num, range1+':'+range1[0]+"1000")
    except TypeError:
        return

def addEntryEntry(sheet, entry, entry2):
    try:
      if entry.type == 'row':
        range1 = str(gspread.utils.rowcol_to_a1(entry, 1))
        range2 = str(gspread.utils.rowcol_to_a1(entry2, 1))
        values_list = sheet.range(range1 + ":BA" + str(entry))
        values2_list = sheet.range(range2 + ":BA" + str(entry2))
        for i in range(len(values_list)):
          cell = values_list[i]
          cell2 = values2_list[i]
          if len(cell.value) > 0 and len(cell2.value):
            cell2.value = str(int(cell2.value) + int(cell.value))
        sheet.update_cells(values2_list)
      else:
        range1 = str(gspread.utils.rowcol_to_a1(1, entry))
        range2 = str(gspread.utils.rowcol_to_a1(1, entry2))
        values_list = sheet.range(range1 + ":" + str(entry) + "1000")
        values2_list = sheet.range(range2 + ":" + str(entry2) + "1000")
        for i in range(len(values_list)):
          cell = values_list[i]
          cell2 = values2_list[i]
          if len(cell.value) > 0 and len(cell2.value):
            cell2.value = str(int(cell2.value) + int(cell.value))
        sheet.update_cells(values2_list)
    except TypeError:
        return


def insert_entry(sheet, index, type):
    new_list = []
    if (type == 'col'):
        sheet.insert_cols(ord(index) - ord("A") + 1, 1)
    else:
        sheet.insert_row(new_list, index)

# works
def multiply_cell(sheet, num, cell):
    val = sheet.acell(cell).value
    cell_update(sheet, cell, num * int(val))

# works
def multiply_range(sheet, num, range):
    values_list = sheet.range(range)
    for cell in values_list:
      if len(cell.value) > 0: 
        cell.value = str(int(cell.value) * num)
    sheet.update_cells(values_list)

# works
def multiply_entry(sheet, num, entry, type):
    if type == 0:
      num_elements = len(sheet.col_values(entry))
      range1 = str(gspread.utils.rowcol_to_a1(entry, 1))
      range2 = str(gspread.utils.rowcol_to_a1(entry, num_elements))
      multiply_range(sheet, num, range1+':'+range2)
    else:
      num_elements = len(sheet.row_values(entry))
      range1 = str(gspread.utils.rowcol_to_a1(1, entry))
      range2 = str(gspread.utils.rowcol_to_a1(num_elements, entry))
      multiply_range(sheet, num, range1+':'+range2)
    
# works
def divide_cell(sheet, num, cell):
    val = sheet.acell(cell).value
    cell_update(sheet, cell, int(val) / num)

# works
def divide_range(sheet, num, range):
    values_list = sheet.range(range)
    for cell in values_list:
      cell.value = str(int(cell.value) / num)
    sheet.update_cells(values_list)

# works
def divide_entry(sheet, num, entry, type):
    if type == 0:
      num_elements = len(sheet.col_values(entry))
      range1 = str(gspread.utils.rowcol_to_a1(entry, 1))
      range2 = str(gspread.utils.rowcol_to_a1(entry, num_elements))
      divide_range(sheet, num, range1+':'+range2)
    else:
      num_elements = len(sheet.row_values(entry))
      range1 = str(gspread.utils.rowcol_to_a1(1, entry))
      range2 = str(gspread.utils.rowcol_to_a1(num_elements, entry))
      divide_range(sheet, num, range1+':'+range2)

# works
def cell_update(sheet, cell, data):
    # Cell needs to be in A1 format
    sheet.update(cell, data)

# works
def update_cell_literal(sheet, row, col, data):
    # Ensure we have valid row and col int values
    sheet.update_cell(row, col, data)

def update_range(sheet, range, arr):
    # Range needs to be in "A1:B2" format
    values_list = sheet.range(range)
    for i in range(len(values_list)):
      values_list[i].value = str(arr[i])
    sheet.update_cells(values_list)

# works
def average_entry(sheet, entry, type):
    # type - 0 for row and 1 for column
    values_list = sheet.row_values(entry) if type == 'row' else sheet.col_values(ord(entry) - ord("A") + 1)
    sumRes = 0
    lenRes = 0
    for i in values_list:
        if i != '':
            sumRes += int(i)
            lenRes += 1
    average = sumRes / lenRes
    return average

# works
def format_bold(sheet, range):
    sheet.format(range, {'textFormat': {'bold': True}}) 

def format_bold_entry(sheet, entry):
    if(entry.type == 'col'):
        format_bold(entry.value + '0:' + entry.value + "1000")
    else:
        format_bold('A' + entry.value + ":Z" + entry.value )


# works
def sort(sheet, spec):
    #spec: (col : 'asc' or 'des')
    #example: (2: 'asc)
    #sorts based on second column in increasing order
    sheet.sort(spec, range='A2:G1000')

# works
def sin_cell(sheet, cell):
    val = sheet.acell(cell).value
    cell_update(sheet, cell, math.sin(int(val)))

# works
def cos_cell(sheet, cell):
    val = sheet.acell(cell).value
    cell_update(sheet, cell, math.cos(int(val)))

# works
def sin_range(sheet, range):
    values_list = sheet.range(range)
    for cell in values_list:
      cell.value = str(math.sin(int(cell.value)))
    sheet.update_cells(values_list)

# works
def cos_range(sheet, range):
    values_list = sheet.range(range)
    values_list = np.cos(values_list)
    update_range(range, values_list)

def sin_entry(sheet, entry, type):
    values_list = sheet.row_values(entry) if type == 0 else sheet.col_values(entry)
    new_list = []
    REPLACE_NO_SPACE = re.compile('[^A-Za-z0-9]+')
    values_list = [REPLACE_NO_SPACE.sub("", line.lower()) for line in values_list]
    for i in values_list: # RIGHT HERE
        if i != '':
            new_list.append(float(i))
    values_list = list(np.sin(new_list))
    cell_list = None
    pprint(entry)
    if(type == 'row'):
        cell_list = sheet.range("A" + entry + ":" + chr(len(values_list) + ord("A")) + entry)
    else:
        cell_list = sheet.range(chr(entry + ord("A") - 1) + str(1) + ":" + chr(entry + ord("A") - 1) + str(len(values_list) + 1))
    for i in range(len(values_list)):
        cell_list[i].value = values_list[i]
    sheet.update_cells(cell_list) # idk if this works

def cos_entry(sheet, entry, type):
    values_list = sheet.row_values(entry) if type == 0 else sheet.col_values(entry)
    new_list = []
    REPLACE_NO_SPACE = re.compile('[^A-Za-z0-9]+')
    values_list = [REPLACE_NO_SPACE.sub("", line.lower()) for line in values_list]
    for i in values_list: # RIGHT HERE
        if i != '':
            new_list.append(float(i))
    values_list = list(np.cos(new_list))
    cell_list = None
    pprint(entry)
    if(type == 'row'):
        cell_list = sheet.range("A" + entry + ":" + chr(len(values_list) + ord("A")) + entry)
    else:
        cell_list = sheet.range(chr(entry + ord("A") - 1) + str(1) + ":" + chr(entry + ord("A") - 1) + str(len(values_list) + 1))
    for i in range(len(values_list)):
        cell_list[i].value = values_list[i]
    sheet.update_cells(cell_list) # idk if this works

# works
def set_background(sheet, range, color):
    # color will be an actual color name
    arr = colors.to_rgb(color)
    sheet.format(range, {
        "backgroundColor": {
            "red": arr[0],
            "green": arr[1],
            "blue": arr[2]
        }
    })

def set_background_entry(sheet, entry, color):
    if(entry.rowOrCol == 'col'):
        set_background(sheet, entry.value + '0:' + entry.value + "1000", color)
    else:
        set_background(sheet, 'A' + entry.value + ":Z" + entry.value, color)


def filter_by_prime(sheet):
    vals = sheet.get_all_values()
    result = ()
    for i in vals:
        if(type(vals[i]) == int and isPrime(vals[i])):
            result.__add__(i)
    return result

def isPrime(n):
   if n <= 1 or n % 1 > 0:
      return False
   for i in range(2, n//2):
      if n % i == 0:
         return False
   return True

# def graph(r):
#     dataframeObj=GET.read_sheet_to_dataframe(connection_url,driveouth_json)

#     plot=r.plot_chart(g,X,Y,'line',imagename='test')

