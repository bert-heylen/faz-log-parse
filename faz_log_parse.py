import sys
import argparse
from argparse import RawTextHelpFormatter

dict_count = {}

parser = argparse.ArgumentParser(
    prog="faz_log_parse.py",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
        This script parses a FortiAnalyzer log file for various things.
        Requires at minimum the -f (logfile) as input, which by default
        will look for unique sessions and counts their occurence.
        A sessions is the combination of srcip, dstip, app, dstport and proto.
        
        Use the -f <field> parameter to count and sort on a specific field.
            Common ones: policyid, srcip, dstip
            
        Use the -t <int> parameter to limit the output to the top X.
            Default = 50
        ''')
parser.add_argument("log", help="Log file for input of the script.")
parser.add_argument("-f", "--field", dest="field", help="Find unique field")
parser.add_argument("-t", "--top", dest="top", type=int, default=50, help ="OPTIONAL - Limit output to top x values. Default = unlimited")

args = parser.parse_args()

def generate_dict(line):
    line_clean = line.replace('\n','').split(',')
    for entry in line_clean:
      if entry == '""':
        continue
      else:
        key = entry.replace('"','').split('=')[0]
        value = entry.replace('"','').split('=')[1]
        dict_temp[key] = value
    return;

def count_session(srcip, dstip, app, dstport, proto):
    tuple_temp = (srcip, dstip, app, dstport, proto)
    
    if tuple_temp in dict_count.keys():
        dict_count[tuple_temp] += 1
    else:
        dict_count[tuple_temp] = 1
    return;

def print_sorted_session(top):
    i = 0
    for k in sorted(dict_count, key=dict_count.get, reverse=True):
      if i < int(top):
        print(k, dict_count[k])
        i += 1

def count(value):
    if value in dict_count.keys():
        dict_count[value] += 1
    else:
        dict_count[value] = 1
    return;

# Sort the dictionary high to low and print to stdout
def print_sorted(top):
    i = 0
    for k in sorted(dict_count, key=dict_count.get, reverse=True):
      if i < int(top):
        print(k, dict_count[k])
        i += 1

if not args.field:
    print("Parsing log file {}".format(args.log))
    print("Parsing for unique sessions.")
    
    with open(args.log) as f:
        for line in f:
            dict_temp = {}
            generate_dict(line)
            if not 'dstport' in dict_temp.keys():
              dict_temp['dstport'] = ""
            if not 'app' in dict_temp.keys():
              dict_temp['app'] = ""
            
            count_session(dict_temp['srcip'], dict_temp['dstip'], dict_temp['app'], dict_temp['dstport'], dict_temp['proto'])
    print_sorted_session(args.top)
            
else:
    print("Parsing log file {}".format(args.log))
    print("Parsing for field: {}".format(args.field))
    
    with open(args.log) as f:
        for line in f:
          dict_temp = {}
          generate_dict(line)
          count(dict_temp[args.field])
    print_sorted(args.top)

