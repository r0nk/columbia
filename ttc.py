#!/bin/env python3
#convert textrated file to final csvs
import json
import os
import re
import sys

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                if child_id in blocks_map:
                    cell = blocks_map[child_id]
                else:
                    continue
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}

                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    if child_id in blocks_map:
                        word = blocks_map[child_id]
                    else:
                        continue
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '
    return text


def all_table_blocks(data):
    # Get the text blocks
    blocks=data['Blocks']

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    tables = []
    for index, table in enumerate(table_blocks):
        tables.append(get_table(table, blocks_map, index +1))

    return tables


def get_table(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)

    csv = []

    # get cells.
#    csv = 'Table: {0}\n\n'.format(table_id)

    row = ""
    for row_index, cols in rows.items():
        for col_index, text in cols.items():
            row += "|" +text
        csv.append(row)
        row=""

    return csv

def all_text_blocks(data):
    blocks=data['Blocks']

    blocks_map = {}
    table_blocks = []
    ret = []
    for block in blocks:
        blocks_map[block['Id']] = block

    for block in blocks:
        if block['BlockType'] == "LINE":
            ret.append(get_text(block,blocks_map))
    return ret

def match_case_insensitive(text, pattern):
    """
    Returns a match if the pattern is contained in the text,
    regardless of case, or None if there is no match.
    """
    return re.search(pattern, text, flags=re.IGNORECASE)

hits=0
grab_misses=0
value_misses=0
def grab(label, value, data):
    for d in data:
        if match_case_insensitive(d,label):
            if match_case_insensitive(d,value):
                global hits
                hits+=1
                return match_case_insensitive(d,value).group()
            else:
                global value_misses
                value_misses+=1
    global grab_misses
    grab_misses+=1
    return "MISSING"

def pd(label,value,data):
    print(grab(label,value,data),end=",")

def mine(data):
    pd("reg(\.|i)","[0-9]{2,4}",data) #registration number
    pd("(insect|herb|fung)icida","(insect|herb|fung)icida",data) #Product Class
    pd("Ingrediente Activo:",".*",data) #Active Ingredient
    pd("tipo de formulac",".*",data) #Formulation type
    pd("Cultivo registrados",".*",data) #Crop
# VVV These are all form tables probably VVV
#Pests
#Application type
#Application timing
#Application methods
#Dose
#Dose Units
#Waiting period (days)
#Reentry interval (days)
#Number of applications
#Application interval (days)

    print("")

directory = '/tmp/extracted/'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(directory+filename, "r") as f:
            print(filename,end=",")
            j = json.load(f)
            data = all_text_blocks(j)
            for t in all_table_blocks(j):
                data+=t
            mine(data)
#            sys.exit(1)

print("Hits:",hits)
print("Grab misses:",grab_misses)
print("Value misses:",value_misses)

