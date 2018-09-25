import regex
import pathlib


def zfiller(start_dir):
    print(start_dir)
    files = list(start_dir.glob('*'))
    nums = []
    
    for file in files:
        m = regex.search(r'\d+', file.name)
        if m:
            nums.append(m[0])
    
    if nums:
        max_len = max(len(n) for n in nums)
        print(nums, max_len)
        
        def repl(m):
            print(m)
            return m[0].zfill(max_len)
        
        for file in files:
            new_file = file.parent / regex.sub(r'\d+', repl, file.name)
            print(f'renaming {file.relative_to(start_dir)} to {new_file.relative_to(start_dir)}')
            file.rename(new_file)
        
    for file in start_dir.glob('*'):
        if file.is_dir():
            zfiller(file)
        

        
    
