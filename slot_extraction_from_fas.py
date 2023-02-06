import re
import pandas as pd
import argparse

"""
Slot Extraction: 

input format (both are acceptable):
    a. from fas file: "onesemantics	settings_and_control:get:battery_level	余| <unk> 电|<name> 信|<name> 息|<name>"
    b. from staged output: "1	onesemantics	assistant:change	令|<unk> ipa|<unk> 切|<unk> 换|<unk> 吓|<unk>"

output format: <business_anaphora>=此;<name>=三湘儿女;
"""


def extract_slot_and_tag(input_file, output_file):
    df = pd.read_csv(input_file, sep="\t", header=None)
    fas_case_df = df.iloc[:, -1]  # read fas cas

    for index, value in fas_case_df.items():  # add an initial space for extracting chars via regex
        fas_case_df = fas_case_df.copy()
        value = ' ' + value
        fas_case_df[index] = value

    tag_pattern = '<\w+>'
    tag_list = []
    for i in fas_case_df:
        matched_slots = re.findall(tag_pattern, i)
        tag_list.append(matched_slots)

    char_pattern = '(?<=\s)(\w+|[\u4e00-\u9fa5]+)(?=\|)'
    char_list = []
    for i in fas_case_df:
        matched_chars = re.findall(char_pattern, i)
        char_list.append(matched_chars)

    def address_eng(d):  # segment english slots: eg. ipachart -> ipa chart
        for key in d:
            slots = d[key].replace('/', '')
            if slots.encode('utf-8').isalpha():
                slot_all_eng = ' '.join(d[key].split('/'))
                d[key] = slot_all_eng
            else:
                d[key] = slots
        return d

    def concatenate(d):  # concatenate tag and corresponding slot: eg. <label>=公司;
        slot = ''
        for key in d:
            if key == "<unk>":
                continue
            if d[key][-1] == '_':
                d[key] = d[key].replace('_','')
                temp = key + '=' + d[key] + ';'
                slot += temp
            else:
                arr = d[key].split('_')  # address fas cases eg. |<cat> |<unk> |<cat>
                temp = ''
                for each in arr:
                    intermediate = key + '=' + each + ';'
                    temp += intermediate
                slot += temp

        return slot

    result = []
    last_tag = "NULL"
    for i in range(len(char_list)):
        mapping_dict = {}
        for j in range(len(char_list[i])):  # filter out <unk> tags
            if tag_list[i][j] != last_tag and last_tag != "NULL" and last_tag in mapping_dict.keys():
                mapping_dict[last_tag] += "_"
            if tag_list[i][j] not in mapping_dict.keys():
                mapping_dict[tag_list[i][j]] = char_list[i][j]
            else:
                mapping_dict[tag_list[i][j]] += '/' + char_list[i][j]
            last_tag = tag_list[i][j]
        mapping_dict = address_eng(mapping_dict)
        slot = concatenate(mapping_dict)

        result.append(slot)
        output_df = pd.DataFrame(result)
        output_df.to_csv(output_file, index=False, header=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="input fas file name")
    parser.add_argument('--output', required=True, help="output slot file name")
    args = parser.parse_args()

    extract_slot_and_tag(args.input, args.output)
    print('The slots have been extracted to ' + args.output)
