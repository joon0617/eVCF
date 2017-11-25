import mmap
import contextlib
from Crypto.Cipher import AES
import base64
import time

FILENAME='ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.evcf'
FINDTHIS='10177'   #POS
for i in range(16-len(FINDTHIS)):
    FINDTHIS='0'+FINDTHIS #zero padding
    
KEY='This is a key123'



with open(FILENAME, 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        
        while True:
            line=m.readline()
            if line.split('\t')[0]=='#CHROM':
                break
        start_time = time.time()
        totalsize=m.size()
        base=m.rfind('\n',0,m.tell()-1)
        datasize=totalsize-base
        m.seek(base)

        middle = base+datasize/2 ##
        mrange = datasize
        tempdec=0
        while True:
            mrange=mrange/2
            m.seek(middle)
            m.readline()#flushing
            line = m.readline()
            b64= line.split('\t')[1]
            
            ciphertext=base64.b64decode(b64)
            obj2 = AES.new(KEY)
            dec=obj2.decrypt(ciphertext)

            if dec == tempdec:
                print 'NO MATCH'
                break
            if dec == FINDTHIS:
                print 'MATCH FOUND AT '+str(m.tell()) +'th byte'
                break
            elif dec < FINDTHIS:
                #print '<'
                middle=middle+mrange/2
            else:
                #print '>'
                middle=middle-mrange/2
            tempdec=dec

        
print("--- %s seconds ---" % (time.time() - start_time))
