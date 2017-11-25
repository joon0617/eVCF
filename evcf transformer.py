from Crypto.Cipher import AES
import base64
import time

FILENAME='ALL.chr7.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf'

KEY='This is a key123'
f=open(FILENAME)
f2=open('.'.join(FILENAME.split('.')[:-1])+'.evcf','w')

while True:
    line=f.readline()
    f2.write(line)
    if line.strip().split('\t')[0] == '#CHROM':
        break

print 'start'

start_time = time.time()


while True:
    line = f.readline()
    if not line: break
    li=line.split('\t')
    POS=li[1]
    for i in range(16-len(POS)):
        POS='0'+POS #zero padding

    obj = AES.new(KEY)

    ciphertext = obj.encrypt(POS)
    b64=base64.b64encode(ciphertext)
    li[1]=b64
    f2.write('\t'.join(li))
    f2.flush()


f.close()
f2.flush()
f2.close()
print("--- %s seconds ---" % (time.time() - start_time))
