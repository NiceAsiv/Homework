import binascii
import gmpy2
import math
n=[]#模数集合
e=[]#公钥指数集合
c=[]#密文集合
m={zip(['Frame'+str(i) for i in range(0,21)],'')}
# Path: code\main.py
sloved={}#已解密的密文集合
filename=['data\Frame'+str(i) for i in range(0,21)]#文件名集合
# print(filename)
for i in range(0,21):
        f=open(filename[i],'r')
        data=f.read()
        #str->hex->int
        n.append(int(data[:256],16))
        e.append(int(data[256:512],16))
        c.append(int(data[512:],16))
#输出e的值
# for i in range(0,21):
#     print('e['+str(i)+']='+str(e[i]))
# #输出n的值
# for i in range(0,21):
#     print('n['+str(i)+']='+str(n[i]))
# #输出c的
# for i in range(0,21):
#     print('c['+str(i)+']='+str(c[i]))

#遍历所有模数,找到模数相同的加密密文
for i  in range(0,21):
    for j in range(i+1,21):
        if n[i]==n[j]:
            print('n['+str(i)+']=='+'n['+str(j)+']')

#遍历寻找任意两个模数N的公因子，如果得到不为1的公因子则可以成功分解这两个模数
for i in range(0,21):
        for j in range(i+1,21):
            if n[i]==n[j]:
                continue
            else:
                rem=math.gcd(n[i],n[j])
                if rem!=1:
                        print('gcd(n['+str(i)+'],n['+str(j)+'])='+str(rem))

#公共模数攻击
#扩展欧几里得算法
def exgcd(a,b):
        if b==0:
                return 1,0,a
        else:
                x,y,r=exgcd(b,a%b)
                x,y=y,(x-(a//b)*y)
                return x,y,r
def same_mod_attack(n,e1,e2,c1,c2):
    x,y,r=exgcd(e1,e2)
    #求模逆元
    if x<0:
        x=-x;
        c1=gmpy2.invert(c1,n)
    elif y<0:
        y=-y;
        c2=gmpy2.invert(c2,n) 
    #求解明文
    m=pow(c1,x,n)*pow(c2,y,n)%n
    #将明文转换为hex
    m=hex(m)[2:]#去掉0x
    #将hex转换为str
    m=binascii.unhexlify(m)[-8:]#hex->str
    return m




#公因数碰撞攻击
def same_factor_attack():
        p_of_prime=gmpy2.gcd(n[1],n[18])
        q1=n[1]//p_of_prime
        q18=n[18]//p_of_prime
        phi1=(p_of_prime-1)*(q1-1)#计算欧拉函数
        phi18=(p_of_prime-1)*(q18-1)#计算欧拉函数
        d1=gmpy2.invert(e[1],phi1)#计算私钥
        d18=gmpy2.invert(e[18],phi18)#计算私钥
        m1=pow(c[1],d1,n[1])#解密
        m18=pow(c[18],d18,n[18])#解密
        m1=hex(m1)[2:]#去掉0x
        m18=hex(m18)[2:]#去掉0x
        m1=binascii.unhexlify(m1)[-8:]#hex->str
        m18=binascii.unhexlify(m18)[-8:]#hex->str
        sloved['Frame1']=m1
        sloved['Frame18']=m18
#中国剩余定理
def chinese_remainder_theorem(backup):
        #计算N的乘积
        N=1
        for a,n in backup:
                N*=n
        #计算Ni
        Ni=[]
        for a,n in backup:
                Ni.append(N//n)
        #计算Ni的模逆元
        Ni_inverse=[]
        for i in range(0,len(Ni)):
                Ni_inverse.append(gmpy2.invert(Ni[i],backup[i][1]))
        #计算x
        x=0
        for i in range(0,len(Ni)):
                x+=backup[i][0]*Ni[i]*Ni_inverse[i]
        x=x%N
        return x,N



#低指数3
def low_exponent_attack3():
        frame_range=[7,11,15]
        backup=[]
        for i in frame_range:
                backup.append([c[i],n[i]])
        x,N=chinese_remainder_theorem(backup)
        #开三次方根
        m=gmpy2.iroot(x,3)[0]
        m=hex(m)[2:]#去掉0x
        m=binascii.unhexlify(m)[-8:]#hex->str
        sloved['Frame7']=m
        sloved['Frame11']=m
        sloved['Frame15']=m

#低指数5
def low_exponent_attack5():
        frame_range=[3,8,12,16,20]
        backup=[]
        for i in frame_range:
                backup.append([c[i],n[i]])
        x,N=chinese_remainder_theorem(backup)
        #开五次方根
        m=gmpy2.iroot(x,5)[0]
        m=hex(m)[2:]#去掉0x
        m=binascii.unhexlify(m)[-8:]#hex->str
        sloved['Frame3']=m
        sloved['Frame8']=m
        sloved['Frame12']=m
        sloved['Frame16']=m
        sloved['Frame20']=m
        
# 费马分解
def fermat_factorization(n):
        a=gmpy2.iroot(n,2)[0]+1
        max=200000
        for i in range(0,max):
                b2=a*a-n
                b=gmpy2.iroot(b2,2)[0]
                if gmpy2.is_square(b2):
                        p=a-b
                        q=a+b
                        return p,q
                a+=1
def fermat_data():
        frame_range=[10]
        for i in frame_range:
                p,q=fermat_factorization(n[i])
                phi=(p-1)*(q-1)#计算欧拉函数
                d=gmpy2.invert(e[i],phi)#计算私钥
                m=pow(c[i],d,n[i])#解密
                m=hex(m)[2:]#去掉0x
                m=binascii.unhexlify(m)[-8:]#hex->str
                sloved['Frame'+str(i)]=m

   

#Pollard's p-1算法
def pollard_p_1(n):
        b=2**20
        a=2
        # while True:
        #         a=gmpy2.powmod(a,b,n)
        #         d=gmpy2.gcd(a-1,n)
        #         if d!=1 and d!=n:
        #                 return d
        #         a+=1
        for i in range(2,b+1):
                a=gmpy2.powmod(a,i,n)
                d=gmpy2.gcd(a-1,n)
                if d!=1 and d!=n:
                        q=n//d
                        n=q*d
        return d
def pollard_data(n):
        frame_range=[2,6,19]
        for i in frame_range:
                temp_n=n[i]
                temp_c=c[i]
                temp_e=e[i]
                p=pollard_p_1(temp_n)
                q=temp_n//p
                phi=(p-1)*(q-1)
                d=gmpy2.invert(temp_e,phi)
                m=pow(temp_c,d,temp_n)
                m=hex(m)[2:]#去掉0x
                m=binascii.unhexlify(m)[-8:]#hex->str
                sloved['Frame'+str(i)]=m

if __name__ == '__main__':
    #公共模数攻击
    for i in range(0,21):
        for j in range(i+1,21):
            if n[i]==n[j]:
                m2=same_mod_attack(n[i],e[i],e[j],c[i],c[j])
                sloved['Frame'+str(i)]=m2
                sloved['Frame'+str(j)]=m2
     #公因数碰撞攻击
    same_factor_attack()
    print(sloved)
     #低指数攻击
    low_exponent_attack3()
    low_exponent_attack5()
    print(sloved)
    #费马分解
    fermat_data()
    print(sloved)
    #Pollard's p-1算法
    pollard_data(n)

    print(sloved)
    #输出将地点按照帧数排序
    for i in range(1,21):
            Frame_name='Frame'+str(i)
            if Frame_name in sloved:
                    print(Frame_name+':')
                    print(sloved[Frame_name])
            else:
                    print(Frame_name+':Not sloved')
                        