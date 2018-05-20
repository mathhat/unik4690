# -*- coding:utf-8 -*-
import common
import cv2
import numpy as np
import read

def eye_jaw(img, eye, ear): 
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
    vertices = np.asarray((ear, ear_down, eye_down, eye)) #corners in order.
    return cv2.fillPoly(img, vertices.T)
    #meat of situation: 
    # if eye and ear, construct square/poly from the vertices 
    # imposed of translation "downwards" and some angles. 
    
    

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
            nx = neck[0] 
            hy =  int((rear[1]+lear[1])/2-dx/k2) #nope  #fight me
            earringsxl = int((lx+nx)/2.)
            earringsxr = int((rx+nx)/2.)  
            earringsy = (nose[1]+neck[1])/2 #neck nose mid
            limblen= int(dx/4)+1
            cv2.circle(npimg, (hx,hy), int(abs(dx*k1)), col, thickness=-limblen, lineType=8, shift=0)
            #limblen= int((dx/8+1)*k6)
            #cv2.line(npimg, (lx,lear[1]), (earringsxl,earringsy) , col, limblen)
            #cv2.line(npimg, (rx,rear[1]), (earringsxr,earringsy) , col, limblen)

        #head pointing left (left eye hidden)
        elif rear and leye:#head circle if right ear is present + faceline
            rx = rear[0]          
            dx = abs(leye[0]-rx)/10+1 #dist between ear n eye
            earringsxr = (rx+neck[0])/2
            earringsy = (nose[1]+neck[1])/2 #neck nose mid

            hx = int(rx+dx*4*k7) #- dx*20 / (rx-leye[0]))
            #Jacob's magic circle coord (next to ear) ?? wtf. fight me
            hy = int((rear[1]+leye[1])/2+dx*k3)
            limblen = int((dx+abs(rx-leye[0])/2)*0.4)+1
            cv2.circle(npimg, (hx,hy), int(abs(nose[0]-rx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            #limblen = int((dx+1)*k5)
            #cv2.line(npimg, (leye[0]+dx,leye[1]), (leye[0]+dx,(nose[1]+neck[1])/2) , col, limblen)
            #cv2.line(npimg, (rx-int(dx*k8),rear[1]), (earringsxr-int(dx*k8),earringsy) , col,limblen)

                
        elif lear and reye:#head circle if left ear is present + faceline
            lx = lear[0]
            reyex = reye[0] 
            dx = abs(lx-reyex)/10+1
            earringsxl =(lx+neck[0])/2
            earringsy = (nose[1]+neck[1])/2 #neck nose mid
            hx = int(lx - dx*4*k7) #+ dx*20. /(lx-reyex))#circle center, next to ear
            hy = int((lear[1]+reye[1])/2+dx*k3)               #circle center, slightly above ear
            limblen = int((abs(lx-reyex)/2+dx)*k5)
            cv2.circle(npimg, (hx,hy), int(abs(nose[0]-lx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            #limblen= int((dx+1)*k5)
            #cv2.line(npimg, (reyex+dx,reye[1]), (reyex+dx,(nose[1]+neck[1])/2) , col, limblen)
            #cv2.line(npimg, (lx+int(dx*k8),reye[1]), (earringsxl+int(dx*k8),earringsy) ,col, limblen)
        #NECK SIRCLE
        r = ((neck[0]-nose[0])*(neck[0]-nose[0])+(neck[1]-nose[1])*(neck[1]-nose[1]))/200
        cv2.circle(npimg, (neck[0],neck[1]), r, col, thickness=-1, lineType=8, shift=0)

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
    i = 0
    torso = []
    for part in common.CocoTorso:
        if part not in parts:
            continue 
        torso.append([Centers[part][0],Centers[part][1]])
        i += 1
    if i == 4:
        torso = np.asarray(torso)
        torso = torso.reshape((-1,1,2),)
        #print torso

        #npimg = cv2.polylines(npimg,[torso],1,col,10)

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
