# -*- coding:utf-8 -*-
import common
import cv2
import numpy as np
import read


def eye_jaw(img, eye, ear, col): 
    # let's test some shit: 
    #shoudl be general for both right or left. 
    # points to vector (x, y) (x', y')
    # (x' - x) = dist in x-direction 
    # (y' - y) = dist in y-direrction 
    # v' - v = vector from v to v'
    x0 = ear[0]
    y0 = ear[1]
    x_eye = eye[0]
    y_eye = eye[1]
    #proportion = lambda (x_diff,y_diff) :   
    ear_down = (x0 - (y_eye - y0) , y0 + (x_eye - x0))  
    eye_down = (x_eye - (y_eye - y0) , y_eye + (x_eye - x0))
    vertices = np.asarray([[ear, ear_down, eye_down, eye]]) #corners in order.
    print vertices
    print vertices.shape
    cv2.fillPoly(img, vertices, col)
    

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
            angle = 0
            dy = lear[1]-rear[1]

            if dy: 
                taneyes = dy/float(lx-rx) #Bruker heller tangens her for å få en relativ vinkel.
                angle = np.arctan(taneyes)*180/np.pi

            # Plasser etterpå "midpunktet" "over" basert på vinkel. 
            dx = int(np.linalg.norm(np.array(lear)-np.array(rear)))
            #^relation for headsize, distance between ears
            hy =  int((rear[1]+lear[1])/2)#-dx/k2) #nope  #fight me
            hy2 = hy - int(dx / 2.5)
            #limblen= int(dx/4)+1
            l =8.*dx/(abs(nose[1]-neck[1])+1)
            #cv2.circle(npimg, (hx,hy), int(abs(dx*k1)), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k1/1.3),int(dx*k1*1.5+l)) ,angle,0,360,col,-1)
            cv2.ellipse(npimg,(hx+int(angle),hy2),(int(dx*k1/1.2),int(dx*k1/1.3))  ,angle,180,360,col,-1)
            
        #head pointing left (left eye hidden)
        elif rear and leye:#head circle if right ear is present + faceline
            rx = rear[0]          
            dx = leye[0]-rx#/10+1 #dist between ear n eye
            dy = (leye[1]-rear[1])
            angle = 0
            if dy:
                tan = dy/float(dx)
                angle = np.arctan(tan)*180/np.pi
            dx = int(np.linalg.norm(np.array(rear)-np.array(leye)))
          
          
          
            hx = int(rx+dx/10.*4*k7*0.9) #- dx*20 / (rx-leye[0]))
            #Jacob's magic circle coord (next to ear) ?? wtf. fight me
            hy = int((rear[1]+leye[1])/2+dx/10.*k3*1.6)
            hy2 = hy - dx/10

            #limblen = int((dx+abs(rx-leye[0])/2)*0.4)+1
            #cv2.circle(npimg, (hx,hy), int(abs(nose[0]-rx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k4*0.85),int(dx*k4*0.65))  ,-angle-20,0,360,col,-1)
            #cv2.ellipse(npimg,(hx,hy2),(int(abs(nose[0]-rx)*k4*0.85),int(abs(nose[0]-rx)*k4*0.65))  ,-20,0,360,col,-1)
                
        elif lear and reye:#head circle if left ear is present + faceline
            lx = lear[0]
            reyex = reye[0] 
            dx = (lx-reyex)#/10+1
            dy = (lear[1]-reye[1])
            angle = 0
            if dy:
                tan = dy/float(dx)
                angle = np.arctan(tan)*180/np.pi
            dx = int(np.linalg.norm(np.array(lear)-np.array(reye)))
            hx = int(lx - dx/10.*4*k7*0.9) #+ dx*20. /(lx-reyex))#circle center, next to ear
            hy = int((lear[1]+reye[1])/2+dx/10.*k3*1.6)               #circle center, slightly above ear
            hy2 = hy - dx/10
            #limblen = int((abs(lx-reyex)/2+dx)*k5)
            #cv2.circle(npimg, (hx,hy), int(abs(nose[0]-lx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k4*0.85),int(dx*k4*0.65))  ,-angle+20,0,360,col,-1)
            #cv2.ellipse(npimg,(hx,hy2),(int(abs(nose[0]-lx)*k4*0.85),int(abs(nose[0]-lx)*k4*0.65))  ,20,0,360,col,-1)

        else: #assume ear + eye combo 
            if (leye and lear):
                eye_jaw(npimg, leye,lear,col)
            elif (reye and rear):
                eye_jaw(npimg, reye, rear,col)
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
        d  = int(np.sqrt(dx*dx+dy*dy))
        angle = np.arctan(dy*1./dx)*180/np.pi
        cv2.ellipse(npimg,(neck[0],neck[1]),(d/2,int(d*1.5)),angle,0,180,col,-20)
        
        torso.append([lshould[0],lshould[1]])
        torso.append([rshould[0],rshould[1]])
        #torso.append([neck[0]-dy,neck[1]+int(dx*1.5)]) #normal
        torso.append([neck[0]+dy,neck[1]-int(dx*0.35)])
        torso = np.asarray(torso)
        torso = torso.reshape((-1,1,2),)   
        #npimg = cv2.fillPoly(npimg,[torso],col)
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
    d  = int(np.sqrt(dx*dx+dy*dy))
    angle = np.arctan(dy*1./dx)*180/np.pi
    cv2.ellipse(npimg,(neck[0]+dy/20,neck[1]+dx/20),(d/2,int(d*1.5)),angle,0,180,col,-20)
    
    

    torso.append([should[0],should[1]])
    torso.append([should[0]-dx,should[1]-dy])
    #torso.append([neck[0]-dy*minus,neck[1]+int(dx*1.5)*minus]) #normal
    torso.append([neck[0]+dy*minus,neck[1]-int(dx*0.35)*minus])
    
    torso = np.asarray(torso)
    torso = torso.reshape((-1,1,2),)   
    #npimg = cv2.fillPoly(npimg,[torso],col)
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
        npimg = draw_head(npimg,Centers,col,bol,k) #draws head (with internal jaw-line)
        npimg = draw_limbs(npimg,Centers,col,parts) #draws arms and legs
        npimg = draw_torso(npimg,Centers,col,parts) #sigh
    return npimg, centers
