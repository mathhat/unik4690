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
    x_ear = ear[0]
    y_ear = ear[1]
    x_eye = eye[0]
    y_eye = eye[1] 
    #h,w = img.shape # maximal indices for h and w. 
    #proportion = lambda (x_diff,y_diff) :   
    # rotation matrix = [cos t, - sin t],[sin t, cos t]
    # rot 90 c-clockwise => x,y => y,-x -- (x - x0, y - y_0)
    # rot 90   clockwise => x,y => -y,x -- (y - y_0, x - x0)
    # dependency on orientation:
    # matrix count x left->right , y top->bottom
    if x_ear < x_eye:
        #facing right (on screen/in matrix) re: good call, fakin hate the mirror effect
        #x - x_0 = x_eye - x_ear = dx
        #y - y_0 = y_eye - y_ear = dy
        dx = x_eye - x_ear
        dy = y_eye - y_ear # to get specific distance
        dd = int(np.sqrt(dx*dx+dy*dy))
        bottom_left = (x_ear - dy, 
                       y_ear + dx)
        bottom_right = (x_eye - dy - int(dd*1./5), #correctional term - joe
                        y_eye + dx  - int(dd*1./5))
        #order, ear - bl - br - eye
        
        vertices = np.asarray([[ear, 
                                bottom_left,
                                bottom_right, 
                                (eye[0]+dd/10,eye[1])]])
        cv2.fillPoly(img, vertices, col)

    elif x_ear > x_eye: 
        #facing left (on screen/in matrix)
        #x - x_0 = x_ear - x_eye = dx
        #y - y_0 = y_ear - y_eye = dy
        dx = x_ear - x_eye
        dy = y_ear - y_eye
        dd = int(np.sqrt(dx*dx+dy*dy))
        #L = len(img[0])
        
        bottom_left = (x_eye - dy+int(dd*1./5), 
                       y_eye + dx - int(dd*1./5))
        bottom_right = (x_ear - dy,
                        y_ear + dx)
        #order, ear - br - bl - eye
        vertices = np.asarray([[ear, 
                                bottom_right,
                                bottom_left, 
                                (eye[0]-dd/10,eye[1])]])
        cv2.fillPoly(img, vertices, col)
    #Check not outside image: 
    #if bottom_[0] > img[0][-1]: 
    #    eye_down[0] = img[0][-1]
    #elif ear_down[0] > img[0][-1]: 
    #    ear_down[0] = img[0][-1]
  

    #cv2.fillPoly(img, vertices, col)
    return img
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
            dx = float(lx-rx)
            if dy and dx: 
                taneyes = dy/dx #Bruker heller tangens her for å få en relativ vinkel.
                angle = np.arctan(taneyes)*180/np.pi

            # Plasser etterpå "midpunktet" "over" basert på vinkel. 
            dx = int(np.linalg.norm(np.array(lear)-np.array(rear)))
            #^relation for headsize, distance between ears
            hy =  int((rear[1]+lear[1])/2)#-dx/k2) #nope  #fight me
            hy2 = hy - int(dx / 2.5)
            #limblen= int(dx/4)+1
            l =8.*dx/(abs(nose[1]-neck[1])+1)
            #cv2.circle(npimg, (hx,hy), int(abs(dx*k1)), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k1/1.3),int(dx*k1*1.5+l)) ,angle,180,360,col,-1)
            cv2.ellipse(npimg,(hx+int(angle),hy2),(int(dx*k1/1.2),int(dx*k1/1.3))  ,angle,180,360,col,-1)
            
        #head pointing left (left eye hidden)
        elif rear and leye:#head circle if right ear is present + faceline
            rx = rear[0]          
            dx = leye[0]-rx#/10+1 #dist between ear n eye
            dy = (leye[1]-rear[1])
            angle = 0
            if dy and dx:
                tan = dy/float(dx)
                angle = np.arctan(tan)*180/np.pi
            dx = int(np.linalg.norm(np.array(rear)-np.array(leye)))
          
          
            
            hx = int(rx+dx/10.*4*k7*0.95) #- dx*20 / (rx-leye[0]))
            #Jacob's magic circle coord (next to ear) ?? wtf. fight me
            hy = int((rear[1]+leye[1])/2+dx/10.*k3*1.6)
            hy2 = hy - dx/10

            #limblen = int((dx+abs(rx-leye[0])/2)*0.4)+1
            #cv2.circle(npimg, (hx,hy), int(abs(nose[0]-rx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k4*0.85),int(dx*k4*0.73))  ,-angle-20,0,360,col,-1)
            #cv2.ellipse(npimg,(hx,hy2),(int(abs(nose[0]-rx)*k4*0.85),int(abs(nose[0]-rx)*k4*0.65))  ,-20,0,360,col,-1)
            eye_jaw(npimg,leye,rear, col)
        elif lear and reye:#head circle if left ear is present + faceline
            lx = lear[0]
            reyex = reye[0] 
            dx = (lx-reyex)#/10+1
            dy = (lear[1]-reye[1])
            angle = 0
            if dy and dx:
                tan = dy/float(dx)
                angle = np.arctan(tan)*180/np.pi
            dx = int(np.linalg.norm(np.array(lear)-np.array(reye)))
            hx = int(lx - dx/10.*4*k7*0.9) #+ dx*20. /(lx-reyex))#circle center, next to ear
            hy = int((lear[1]+reye[1])/2+dx/10.*k3*1.6)               #circle center, slightly above ear
            hy2 = hy - dx/10
            #limblen = int((abs(lx-reyex)/2+dx)*k5)
            #cv2.circle(npimg, (hx,hy), int(abs(nose[0]-lx)*k4), col, thickness=-limblen, lineType=8, shift=0)
            cv2.ellipse(npimg,(hx,hy),(int(dx*k4*0.85),int(dx*k4*0.73))  ,-angle+20,0,360,col,-1)
            #cv2.ellipse(npimg,(hx,hy2),(int(abs(nose[0]-lx)*k4*0.85),int(abs(nose[0]-lx)*k4*0.65))  ,20,0,360,col,-1)
            eye_jaw(npimg,reye,lear, col)

    
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
    angle = 0

    if lshould and rshould and neck:
        dx = (lshould[0] - rshould[0])
        dy = (lshould[1] - rshould[1])
        d  = int(np.sqrt(dx*dx+dy*dy))
        if dx and dy:
            angle = np.arctan(dy*1./dx)*180/np.pi
        cv2.ellipse(npimg,(neck[0],(lshould[1]+rshould[1])/2),(d/2,int(d*1.5)),angle,0,180,col,-20)
        
        torso.append([lshould[0],lshould[1]])
        torso.append([rshould[0],rshould[1]])
        #torso.append([neck[0]-dy,neck[1]+int(dx*1.5)]) #normal
        torso.append([neck[0]+dy/2,neck[1]-int(dx*0.35)])
        torso = np.asarray(torso)
        torso = torso.reshape((-1,1,2),)
        #npimg = cv2.fillPoly(npimg,[torso],col)
        npimg = cv2.fillPoly(npimg,[torso],col)
        cv2.line(npimg,(rshould[0]-dy/15,rshould[1]+dx/15),(lshould[0]-dy/15,lshould[1]+dx/15),col,d/6)

        return npimg
    elif neck and lshould:
        should = lshould 
        minus = 1
    elif neck and rshould:
        should = rshould
    else:
        return npimg
    #this code runs if only one shoulder is observed
    dx = (should[0] - neck[0])*2
    dy = (should[1] - neck[1])*2
    d  = int(np.sqrt(dx*dx+dy*dy))
    if dx and dy:
        angle = np.arctan(dy*1./dx)*180/np.pi
    #cv2.ellipse(npimg,(neck[0]+dy/5*minus,neck[1]+dx/5*minus),(d/2,int(d*1.5)),angle,0,180,col,-1)
    cv2.ellipse(npimg,(should[0] - dx/2,should[1] + dy/2),(d/2,int(d*1.5)),angle,0,180,col,-1)
    

    torso.append([should[0],should[1]])
    torso.append([should[0]-dx,should[1]-dy])
    #torso.append([neck[0]-dy*minus,neck[1]+int(dx*1.5)*minus]) #normal
    torso.append([neck[0]+dy/2*minus,neck[1]-int(dx*0.35)*minus])
    
    torso = np.asarray(torso)
    torso = torso.reshape((-1,1,2),)   
    #npimg = cv2.fillPoly(npimg,[torso],col)
    npimg = cv2.fillPoly(npimg,[torso],col)
    cv2.line(npimg,(should[0],should[1]),(should[0]-dx,should[1]-dy),col,d/7)

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

            #cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=7, lineType=8, shift=0)

        npimg = draw_head(npimg,Centers,col,bol,k) #draws head (with internal jaw-line)
        npimg = draw_limbs(npimg,Centers,col,parts) #draws arms and legs
        npimg = draw_torso(npimg,Centers,col,parts) #sigh
    return npimg, centers
