import regex
from tempfile import NamedTemporaryFile

from common import PO_DIR, pofile, humansortkey


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
        return False

def renumber_zeros(po):
    i = 1
    for unit in po.units:
        msgctxt = unit.msgctxt
        if not msgctxt:
            continue
        uid, num = msgctxt[0][1:-1].split(':')
        
        if num.startswith('0'):
            unit.msgctxt[0] = f'"{uid}:0.{i}"'
            i += 1
        else:
            return i > 1

def renumber_segments(po):
    changed = False
    last_nums = None
    for unit in po.units:
        msgctxt = unit.msgctxt
        if not msgctxt:
            continue
        uid, num = msgctxt[0][1:-1].split(':')
        
        nums = num.split('.')
        
        if last_nums and len(last_nums) in {2, 3} and len(last_nums) == len(nums):
            should_be_1 = False
            # try:
                # if int(nums[-2]) - int(last_nums[-2]) == 1:
                    # should_be_1 = True
            # except ValueError:
                # continue
            
            if nums[:-1] == last_nums[:-1]:
                m = regex.match(r'(\d+)([a-z]*)', last_nums[-1])
                last_num, last_alpha = m[1], m[2]
                m = regex.match(r'(\d+)([a-z]*)', nums[-1])
                num, alpha = m[1], m[2]

                if alpha:
                    continue
                if should_be_1:
                    new_num = '1'
                else:
                    new_num = str(int(last_num) + 1)
                if new_num != nums[-1]:
                    nums[-1] = new_num
                    new_ctxt = f'"{uid}:{".".join(nums)}"'
                    if msgctxt[0] != new_ctxt:
                        print(f'Replace: {msgctxt[0]} -> {new_ctxt}, {msgctxt[0] == new_ctxt}')
                        unit.msgctxt = [new_ctxt]
                        changed = True
        last_nums = nums
    return changed
            
            
            
            
        

def compare_order(a, b):
    nums_a = [l[1] for l in a]
    nums_b = [l[1] for l in b]
    if nums_a == nums_b:
        return False
    for i, j in zip(nums_a, nums_b):
        if i != j:
            print(f'{a[0][0]}: Sort Mismatch {i} != {j}')
            return



def check_ordering(contexts, file):
    
    compare_order(contexts, sorted(contexts, key=humansortkey))
    compare_order(contexts, sorted(reversed(contexts), key=humansortkey))
    

def is_data_intact(file, po):
    with file.open('r') as f:
        original = f.read()
    
    with NamedTemporaryFile('wb', delete=False) as f:
        po.savefile(f)
        # pofile closes the file object so we need to reopen
        with open(f.name) as f2:
            new = f2.read()
    
    old_strings = regex.findall('(?:msgid|msgctxt )?".*"', original)
    new_strings = regex.findall('(?:msgid|msgctxt )?".*"', new)
    
    len_diff = len(old_strings) - len(new_strings)
    if len_diff != 0:
        print(f'{file.name}: Missing strings')
        return False
    return True

for file in sorted(PO_DIR.glob('pli-tv/**/*.po')):
    
    with file.open('r') as f:
        po = pofile(f)  
    
    if po.header() is None:
        print(f'{file.name}: Header not readable!')
        with file.open('r') as f:
            lines = []
            for line in f:
                if line.startswith('msgid'):
                    break
                lines.append(line)
        cruft = '\n'.join(lines)
        print(f'File starts with: {cruft}')
    
    
    changed = False
    if 'np' in file.name:
        changed = renumber_zeros(po)
    
    changed = renumber_segments(po) or changed 
    
    contexts = []
    for unit in po.units:    
        msgctxt = unit.msgctxt
        if msgctxt:
            contexts.append(msgctxt[0][1:-1].split(':'))
    
    
    check_ordering(contexts, file)
    
    file_uid = regex.sub(r'(\D)(0+)', r'\1', file.stem)
    nums = []
    last_nums = None
    for uid, con in contexts:
        if file_uid != uid:
            print(f'Mismatched UID: {uid} in {file_uid}')
        
        con2 = regex.sub(r'[a-z]$', lambda m: '.'+str(ord(m[0])-96), con )
        nums = [Num(num) for num in con2.split('.')]
        if last_nums is not None:
            is_1_greater(last_nums, nums, uid, con)
            
        
        last_nums = nums
    intact = is_data_intact(file, po)
    
    if changed and intact:
        po.save()
