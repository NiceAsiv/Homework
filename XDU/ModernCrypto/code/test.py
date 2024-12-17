list=[1,2,3,4,5,6,7,8,9,10]
out=[]
for i in range(2):
    for j in range(5):
        if j==0:
            out.append([])#初始化一个list空间
        out[i].append(list[i*5+j])
print(out)