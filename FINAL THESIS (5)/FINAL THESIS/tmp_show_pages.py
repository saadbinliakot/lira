import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

pages = open('tmp_full.txt', encoding='utf-8', errors='replace').read().split('\f')

def show(idx, label):
    p = pages[idx - 1]
    print(f'===== physical {idx} ({label}) =====')
    print(p.rstrip())
    print()

# List of Tables (printed ix)
show(10, 'printed ix, List of Tables')
# Table 5.3 printed 48
show(58, 'printed 48, Table 5.3 area')
# sections 5.6.2 / 5.6.3 current printed 55-57
show(65, 'printed 55')
show(66, 'printed 56')
show(67, 'printed 57')
