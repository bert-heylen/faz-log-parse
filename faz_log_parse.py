import csv
import sys
import argparse
import ipaddress
from time import sleep
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
parser.add_argument("file", help="Log file for input of the script.")
parser.add_argument("-c", "--column", dest="column", help="Find unique column")
parser.add_argument("-f", "--filter", dest="filter", help="Filter on column")
parser.add_argument("-v", "--fvalue", dest="fvalue", help="Filter on this value")
parser.add_argument("-t", "--top", dest="top", type=int, default=50, help ="OPTIONAL - Limit output to top x values. Default = unlimited")
args = parser.parse_args()

def generate_dict(row, dict_temp):
    for entry in row:
      if entry == '':
        continue
      else:
        key = entry.replace('"','').split('=')[0]
        value = entry.replace('"','').split('=')[1]
        dict_temp[key] = value
    return;

def count_session(srcip, dstip, app, dstport, proto, policyid):
    tuple_temp = (srcip, dstip, app, dstport, proto, policyid)
    
    if tuple_temp in dict_count.keys():
        dict_count[tuple_temp] += 1
    else:
        dict_count[tuple_temp] = 1
    return;

def count(value):
    if value in dict_count.keys():
        dict_count[value] += 1
    else:
        dict_count[value] = 1
    return;

# Sort the dictionary high to low and print to stdout
def print_sorted(top):
    print("")
    print("Printing top {}".format(top))
    print("")
        
    i = 0
    if not args.column:
        for row in sorted(dict_count, key=dict_count.get, reverse=True):
            if i < int(top):
                for field in row:
                    print("{},".format(field), end='')
                print(dict_count[row])
                i += 1
    else:
        for row in sorted(dict_count, key=dict_count.get, reverse=True):
            if i < int(top):
                print("{},".format(row), end='')
                print(dict_count[row])
                i += 1
    return;

#Main body of code
def main():
    total_lines = sum(1 for line in open(args.file))
    current_line = 0
    
    if not args.column:
        print("")
        print("Parsing log file {}".format(args.file))
        print("{} of lines to go through.".format(total_lines))
        print("Parsing for unique sessions.")
        
        if args.filter:
            print("Filtering on '{}', value {}".format(args.filter, args.fvalue))
        
        with open(args.file) as f:
            csvfile = csv.reader(f, delimiter=',')
            for row in csvfile:
                lines_done = current_line/total_lines*100
                sys.stdout.write('\r')
                sys.stdout.write("{} % done".format(round(lines_done,2)))
                sys.stdout.flush()
                
                dict_temp = {}
                generate_dict(row, dict_temp)
                if not 'dstport' in dict_temp.keys():
                  dict_temp['dstport'] = ""
                if not 'app' in dict_temp.keys():
                  dict_temp['app'] = ""
                
                if args.filter == ("srcip" or "dstip") and ipaddress.ip_address(dict_temp[args.filter]) in ipaddress.ip_network(args.fvalue):
                    count_session(dict_temp['srcip'], dict_temp['dstip'], dict_temp['app'], dict_temp['dstport'], dict_temp['proto'], dict_temp['policyid'])
                elif args.filter and dict_temp[args.filter] == args.fvalue:
                    count_session(dict_temp['srcip'], dict_temp['dstip'], dict_temp['app'], dict_temp['dstport'], dict_temp['proto'], dict_temp['policyid'])
                elif not args.filter:
                    count_session(dict_temp['srcip'], dict_temp['dstip'], dict_temp['app'], dict_temp['dstport'], dict_temp['proto'], dict_temp['policyid'])
                current_line += 1
        print_sorted(args.top)
    else:
        print("")
        print("Parsing log file {}".format(args.file))
        print("Parsing for field: {}".format(args.column))
        
        if args.filter:
            print("Filtering on '{}', value {}".format(args.filter, args.fvalue))
        
        with open(args.file) as f:
            csvfile = csv.reader(f, delimiter=',')
            for row in csvfile:
                dict_temp = {}
                generate_dict(row, dict_temp)
                if not 'dstport' in dict_temp.keys():
                  dict_temp['dstport'] = ""
                if not 'app' in dict_temp.keys():
                  dict_temp['app'] = ""
              
                if args.filter == ("srcip" or "dstip") and ipaddress.ip_address(dict_temp[args.filter]) in ipaddress.ip_network(args.fvalue):
                    count(dict_temp[args.column])   
                if args.filter and dict_temp[args.filter] == args.fvalue:
                    count(dict_temp[args.column])
                elif not args.filter:
                    count(dict_temp[args.column])
            print_sorted(args.top)
        
        
if __name__ == '__main__':
    main()