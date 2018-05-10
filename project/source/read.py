def Tol():
    tol1=tol2=tol=i=0
    with open('thresdata.txt','r') as File:
        File.readline()
        for line in File:
            print line.split(' ')
            l = map(float,line.split(' ')[:-1])
            tol1 += l[0]
            tol2 += l[1]
            tol  += l[2]
            i+=1
    tol1 /= i
    tol2 /= i
    tol  = int(tol/i)
    return tol1,tol2,tol
def k1():
    k1=k2=k6=i=0
    with open('k126data.txt','r') as File:
        File.readline()
        for line in File:
            l = map(float,line.split(' ')[:-1])
            k1 += l[0]
            k2 += l[1]
            k6 += l[2]
            i+=1
    k1 /= i
    k2 /= i
    k6 /= i
    return k1,k2,k6
def k2():
    k3=k4=k5=k7=k8=i=0
    with open('k34578data.txt','r') as File:
        File.readline()
        for line in File:
            l = map(float,line.split(' '))
            k3 += l[0]
            k4 += l[1]
            k5 += l[2]
            k7 += l[3]
            k8 += l[4]
            i+=1
    k3 /= i
    k4 /= i
    k5 /= i
    k7 /= i
    k8 /= i
    return k3,k4,k5,k7,k8
    