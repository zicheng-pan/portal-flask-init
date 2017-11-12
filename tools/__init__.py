import os
import json
def parseJsonFile_cutdowntime():
    file_path = 'json/cutdowntime.json'
    rep = None
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            rep = f.read()
        pass
    else:
        open(file_path,"w").close()
    return rep
