        This script parses a FortiAnalyzer log file for various things.
        Requires at minimum the -f (logfile) as input, which by default
        will look for unique sessions and counts their occurence.
        A sessions is the combination of srcip, dstip, app, dstport and proto.
        
        Use the -f <field> parameter to count and sort on a specific field.
            Common ones: policyid, srcip, dstip
            
        Use the -t <int> parameter to limit the output to the top X.
            Default = 50
