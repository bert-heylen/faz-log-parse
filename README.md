This script parses a FortiAnalyzer log file for either of 2 things:
- Occurence of unique sessions (a sessions is the combination of srcip, dstip, app, dstport and proto)
- Occurence of a specific field.

The default behavior of the script is to count unique sessions, for which it only needs the log file as parameter:<br>
#python faz_log_parse.py <log_file>
        
Use the -c <column> parameter to count and sort on a specific field:<br>
#python faz_log_parse.py <log_file> -c <field><br>
Common fields: policyid, srcip, dstip, dstport

Optional parameters:<br>
- -t (top): only prints the top x 
- -f (filter) & -v (value): can be used to filter the report on specific fields and values.
        For example, look up all unique sessions for srcip 1.1.1.1 only:<br>
        #python faz_log_parse.py <log_file> -f srcip -v 1.1.1.1<br>
        The value takes IP CIDR notation for srcip/dstip filters so you can look up subnets as well: 1.1.1.0/24.


To fetch the log file to parse, log into your FortiAnalyzer, Log View.
Create a filter if required, click on the wrench symbol in the upper right corner.
Click Download.  Select CSV as the log file format, do no compress and Download.

You can download it as a compressed file but will need to unzip before running the script: <br>
"unzip -d <file>"
