import docx
import argparse
from os import path
import os
import textract

def remove_index_doc(doc):
    i = doc.find(")")
    return doc[i+1 : ].strip()

def readDocFromFile(file_path):
    doc = textract.process(file_path)
    return doc.decode('utf-8')

def get_list_docFromFile(path_file):

    doc = readDocFromFile(path_file)

    lines = doc.split("\n")
    lines = [t.strip() for t in lines if t != '']
    count = 0
    list_index_doc = []
    for i, p in enumerate(lines):
        if p[:4].lower() == "(doc" and p[4].isdigit() == True :
            count += 1
            list_index_doc.append(i)
    list_index_doc.append(len(lines))

    result = []
    for index in range(len(list_index_doc) - 1):
        list_content_doc = [t for t in lines[list_index_doc[index] : list_index_doc[index+1]]]
        result.append(remove_index_doc("\n".join(list_content_doc)))

    return result

def crate_pair_file(args):

    #create folder if it not exist before
    if path.exists(args.folder) == False:
        os.mkdir(args.folder)

    #read name of pair files
    file_vi = args.input_vi
    file_km = args.input_km
    index_out = args.index_out

    list_vi = get_list_docFromFile(path_file = file_vi)
    list_km = get_list_docFromFile(path_file = file_km)

    if len(list_vi) != len(list_km):
        print("2 Doc not equal align")
        return 

    for i in range(len(list_vi)):
        with open(args.folder + "/" + "vi" + str(index_out+i) + ".txt" , "w") as f_vi:
            f_vi.write(list_vi[i])
        with open(args.folder + "/" + "km" + str(index_out+i) +".txt" , "w") as f_km:
            f_km.write(list_km[i])

parser = argparse.ArgumentParser(description='This module is used for parse file ')
parser.add_argument('--input_vi', type=str, help='input vietnam' , required=True)
parser.add_argument('--input_km', type=str, help='input khmer' , required=True)
parser.add_argument('--index_out', type=int, help='index doc start to create output file' , required=True)
parser.add_argument('--folder', type=str, help='path folder to save new file' , required=True)

args = parser.parse_args()

crate_pair_file(args)

# import textract
# path = "23.12-Khmer.docx"
# # text = textract.process(path)
# # text = text.decode('utf-8')
# # print(text.split("\n"))
# print(readDocFromFile(path))
