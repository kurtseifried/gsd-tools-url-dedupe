#!/usr/bin/env python3

import dns.resolver

filename = "domains.txt"

with open(filename) as domain_file:
    for domain in domain_file:
        #try:
        NS = dns.resolver.resolve(domain, 'NS')
        print(domain + " VALID")
        #except Exception as e:
        #    print(domain + " ERROR: NO NS RECORD")
