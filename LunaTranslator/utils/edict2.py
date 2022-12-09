from utils.config import globalconfig
import sqlite3,os
import Levenshtein,re
from utils.argsort import argsort
from traceback import print_exc
class edict2():
    def __init__(self):
        self.sql=None
        try:
            path=(globalconfig['edict2']['path'] )
            if os.path.exists(path):
                with open(path,'r',encoding='euc-jp') as ff:
                    _=ff.read()
                _=_.split('\n')[1:]
                self.save={}
                for _l in _:
                    try:
                        _s=_l.index(' ')
                    except:
                        continue
                    self.save[_l[:_s]]=_l[_s:]
        except:
            print_exc()
    
    def search(self,word):
         
            try:
                 
                dis=9999
                dis=[]
                savew=[]
                for w in self.save: 
                    if word in w or w in word:
                        d=Levenshtein.distance(w,word)
                        dis.append(d)
                        savew.append(w)
                saveres=[]
                srt=argsort(dis) 
                for ii in srt: 
                    saveres.append(savew[ii]+'<br>'+re.sub('/EntL.*/','', self.save[savew[ii]][1:]))
                    if len(saveres)>=10:
                        break
                return '<hr>'.join(saveres)
            except: 
                print_exc()
                return None
         