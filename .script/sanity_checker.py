import regex

from common import PO_DIR, pofile


class Num:
    def __init__(self, string):
        if '-' in string:
            self.start, self.end = [int(num) for num in string.split('-')]
        else:
            self.start = self.end = int(string)
    
    def __repr__(self):
        if self.start == self.end:
            return str(self.start)
        return f'{self.start}-{self.end}'
    
    

def is_1_greater(a, b, uid, original_con):
    ones_count = 0
    
    if len(b) > len(a):
        a += [Num('0')]

    for i in range(0, min(len(a), len(b))):
        num_a = a[i]
        num_b = b[i]
        
        diff = num_b.start - num_a.end
        if diff == 1:
            ones_count += 1
    if ones_count != 1:
        if original_con.endswith('.0a'):
            return
        print(f"{uid}:{original_con}   {'.'.join(str(n) for n in a)} -> {'.'.join(str(n) for n in b)}")


for file in sorted(PO_DIR.glob('pli-tv/**/*.po')):
    with file.open('r') as f:
        po = pofile(f)
    
    contexts = []
    for unit in po.units:
        
        msgctxt = unit.msgctxt
        if msgctxt:
            contexts.append(msgctxt[0][1:-1].split(':'))
    nums = []
    last_nums = None
    for uid, con in contexts:
        
        con2 = regex.sub(r'[a-z]$', lambda m: '.'+str(ord(m[0])-96), con )
        nums = [Num(num) for num in con2.split('.')]
        if last_nums is not None:
            is_1_greater(last_nums, nums, uid, con)
            
        
        last_nums = nums
