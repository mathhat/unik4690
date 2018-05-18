# -*- coding:utf-8 -*-
import common
import cv2
import numpy as np
import read


def draw_head(npimg,Centers,col,bol,k=[0]):
    tryvar = lambda varpos: Centers[varpos] if varpos in Centers.keys() else None
    lear = tryvar(17)
    rear = tryvar(16)
    leye = tryvar(15)
    reye = tryvar(14)
    nose = tryvar(0)
    neck = tryvar(1)

    if bol:
        k1,k2,k6 = read.k1()
        k3,k4,k5,k7,k8 = read.k2()
    else:
        k1,k2,k3,k4,k5,k6,k7,k8 = k
    
    if (neck and nose):
            
        if (lear and rear): #head circle if both ears are present
            lx = lear[0]
            rx = rear[0]
            hx = (lx + rx)/2 #Nope
            #taneyes = 0 #Bruker heller tangens her for å få en relativ vinkel.
            # Plasser etterpå "midpunktet" "over" basert på vinkel. 
            dx = int(np.linalg.norm(np.array(lear)-np.array(rear)))
            #^relation for headsize, distance between ears
            hy =  int((rear[1]+lear[1])/2)#-dx/k2) #nope  #fight me
            hy2 = hy - int(dx / 2.5)
            #limblen= int(dx/4)+1
            l =8.*dx/(abs(nose[1]-neck[1])+1)
            #cv2.circle(npimg, (hx,hy), int(abs(dx*k1)), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k1/1.3),int(dx*k1*1.5+l))  ,0,180,360,col,-1)
            cv2.ellipse(npimg,(hx,hy2),(int(dx*k1/1.),int(dx*k1/1.3))  ,0,180,360,col,-1)
            
        #head pointing left (left eye hidden)
        elif rear and leye:#head circle if right ear is present + faceline
            rx = rear[0]          
            dx = abs(leye[0]-rx)/10+1 #dist between ear n eye
            hx = int(rx+dx*4*k7*0.9) #- dx*20 / (rx-leye[0]))
            #Jacob's magic circle coord (next to ear) ?? wtf. fight me
            hy = int((rear[1]+leye[1])/2+dx*k3*1.6)
            hy2 = hy - dx

            #limblen = int((dx+abs(rx-leye[0])/2)*0.4)+1
            #cv2.circle(npimg, (hx,hy), int(abs(nose[0]-rx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(abs(nose[0]-rx)*k4*0.85),int(abs(nose[0]-rx)*k4*0.65))  ,-20,0,360,col,-1)
            cv2.ellipse(npimg,(hx,hy2),(int(abs(nose[0]-rx)*k4*0.85),int(abs(nose[0]-rx)*k4*0.65))  ,-20,0,360,col,-1)
                
        elif lear and reye:#head circle if left ear is present + faceline
            lx = lear[0]
            reyex = reye[0] 
            dx = abs(lx-reyex)/10+1
            hx = int(lx - dx*4*k7*0.9) #+ dx*20. /(lx-reyex))#circle center, next to ear
            hy = int((lear[1]+reye[1])/2+dx*k3*1.6)               #circle center, slightly above ear
            hy2 = hy - dx
            #limblen = int((abs(lx-reyex)/2+dx)*k5)
            #cv2.circle(npimg, (hx,hy), int(abs(nose[0]-lx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(abs(nose[0]-lx)*k4*0.85),int(abs(nose[0]-lx)*k4*0.65))  ,20,0,360,col,-1)
            cv2.ellipse(npimg,(hx,hy2),(int(abs(nose[0]-lx)*k4*0.85),int(abs(nose[0]-lx)*k4*0.65))  ,20,0,360,col,-1)

    return npimg




def draw_limbs(npimg,Centers,col,parts):
    for pair_order, pair in enumerate(common.CocoPairsRender):
        if pair[0] not in parts or pair[1] not in parts:
            continue
        x0 = Centers[pair[0]][0]
        x1 = Centers[pair[1]][0]
        y0 = Centers[pair[0]][1]
        y1 = Centers[pair[1]][1]
        
        d = int(np.sqrt((y1-y0)**2+(x1-x0)**2)/2.5)

        npimg = cv2.line(npimg, (x0,y0), (x1,y1), col, d)
    return npimg

def draw_torso(npimg,Centers,col,parts):
    #i = 0
    torso = []
    tryvar = lambda varpos: Centers[varpos] if varpos in Centers.keys() else None
    lshould = tryvar(5)
    rshould = tryvar(2)
    neck = tryvar(1)
    minus = -1
    
    if lshould and rshould and neck:
        dx = (lshould[0] - rshould[0])
        dy = (lshould[1] - rshould[1])

        torso.append([lshould[0],lshould[1]])
        torso.append([rshould[0],rshould[1]])
        torso.append([neck[0]-dy,neck[1]+int(dx*1.5)]) #normal
        torso = np.asarray(torso)
        torso = torso.reshape((-1,1,2),)   
        npimg = cv2.fillPoly(npimg,[torso],col)
        torso[-1] = [neck[0]+dy,neck[1]-int(dx*0.35)]
        npimg = cv2.fillPoly(npimg,[torso],col)
        return npimg
    elif neck and lshould:
        should = lshould 
        minus = 1
    elif neck and rshould:
        should = rshould
        
    else:
        return npimg
    dx = (should[0] - neck[0])*2
    dy = (should[1] - neck[1])*2

    torso.append([should[0],should[1]])
    torso.append([should[0]-dx,should[1]-dy])
    torso.append([neck[0]-dy*minus,neck[1]+int(dx*1.5)*minus]) #normal
    torso = np.asarray(torso)
    torso = torso.reshape((-1,1,2),)   
    npimg = cv2.fillPoly(npimg,[torso],col)
    torso[-1] = [neck[0]+dy*minus,neck[1]-int(dx*0.35)*minus]
    npimg = cv2.fillPoly(npimg,[torso],col)

    return npimg

def draw_humans(npimg, humans,bol=1,k=[0]): #main function
    npimg *=0
    image_h, image_w = npimg.shape[:2]
    centers = {}
    col = [255,255,255]
    for human in humans:
        # draw point
        Centers={}
        parts = human.body_parts.keys()
        for i in range(common.CocoPart.Background.value):
            if i not in parts:
                continue

            body_part = human.body_parts[i]
            center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
            centers[i] = center
            Centers[i] = center
        npimg = draw_head(npimg,Centers,col,bol,k) #draws head
        npimg = draw_limbs(npimg,Centers,col,parts) #draws arms and legs
        npimg = draw_torso(npimg,Centers,col,parts) #sigh
    return npimg, centers
