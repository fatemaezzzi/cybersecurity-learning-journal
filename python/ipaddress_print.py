ipaddress = ["28.82.242.118", "79.107.215.28", "245.214.254.244","230.247.54.245","13.159.91.134"] #Lists are used to store multiple items in a single variable.
map_port = {"28.82.242.118": 80,
            "79.107.215.28": 443,
            "245.214.254.244" : 22,
            "230.247.54.245" : 53,
            "13.159.91.134" : 8080} #Dictionaries are used to store data values in key:value pairs. A dictionary is a collection which is ordered*, changeable and do not allow duplicates.
ip_sets = {"28.82.242.118", "79.107.215.28", "245.214.254.244","230.247.54.245","13.159.91.134"} #Sets are used to store multiple items in a single variable.
print(ipaddress)
print(map_port)
print(ip_sets)