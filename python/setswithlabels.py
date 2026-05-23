ip_set1={ "192.168.1.10",
    "10.0.0.5",
    "172.16.4.22",
    "8.8.8.8"}
ip_set2={"192.168.1.10",
    "172.16.4.22",
    "203.0.113.7",
    "1.1.1.1"}
inter = ip_set1.intersection(ip_set2)
print("Intersection",inter)

union = ip_set1.union(ip_set2)
print("Union",union)

dif = ip_set1.difference(ip_set2)
print("Difference",dif)