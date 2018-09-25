import regex
import os.path

class ZFiller:
    def __init__(self, files):
        self.tree = {}
        self.seen = set()
        common_path = pathlib.Path(*os.path.commonprefix([(p if p.is_dir() else p.parent).parts for p in infiles]))
        self.add_files(files, common_path)
    
    def split(self, string):
        return [int(part) if part.isdigit() else part 
                for part
                in regex.findall(r'\p{alpha}+|\d+|[^\p{alpha}\d]+', string)]
    
    def add_files(self, files):
        for file in files:
            string = file.relative_to(common_path)
            parts = self.split(str(string))
            branch = self.tree
            for part in parts:
                if part not in branch:
                    branch[part] = {}
                branch = branch[part]
                self.seen.add(part)
    
    def zfill(self, string):
     try:
        parts = self.split(string)
        out = []
        branch = self.tree
        for part in parts:
            if isinstance(part, int):
                maxlen = len(str(max(branch.keys())))
                out.append(str(part).zfill(maxlen))
            else:
                out.append(part)
            branch = branch[part]
        return ''.join(out)
     except Exception as e:
         globals().update(locals())
         raise

def zfill(files):
    
