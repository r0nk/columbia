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


def get_table_csv_results(data):
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

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1)
        csv += '\n\n'

    return csv


def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)

    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():

        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'

    csv += '\n\n\n'
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

def grab(label,value, data):
    for d in data:
        if match_case_insensitive(d,label):
            if match_case_insensitive(d,value):
                return match_case_insensitive(d,value).group()
    return ""

def mine(data):
    print(grab("regi","[0-9]{2,4}",data),end=",")
    print(grab("(insect|herb|fung)icida","(insect|herb|fung)icida",data),end=",")

    print("")
#    else:
#        print("REGISTRATION NUMBER NOT FOUND")
#        sys.exit()

directory = 'extracted/'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open('extracted/'+filename, "r") as f:
            print(filename,end=",")
            data = json.load(f)
            mine(all_text_blocks(data))
#            print(get_table_csv_results(data))

