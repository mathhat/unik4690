# -*- coding:utf-8 -*-
import common
import cv2
import numpy as np

    

def draw_humans(npimg, humans, imgcopy=False,):
    if imgcopy:
        npimg = np.copy(npimg)
    npimg = npimg*0
    image_h, image_w = npimg.shape[:2]
    centers = {}
    limblen = 45
    col=[255,255,255]
    for human in humans:
        # draw point
        
        Centers={}
        for i in range(common.CocoPart.Background.value):
            if i not in human.body_parts.keys():
                continue

            body_part = human.body_parts[i]
            center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
            centers[i] = center
            Centers[i] = center
            #cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)


        #this is we're we customize the lines and circles around the human    
        
        #BRRRÆPP
        # Generell rekkefølge for testser: (begge ører)
        #                                  (øre motsatt øye)
        #                                  (øye øye)
        #                                  (ett øye)
        # Som cond-ish liste:
        tryvar = lambda varpos: Centers[varpos] if varpos in Centers.keys() else None
        lear = tryvar(17)
        rear = tryvar(16)
        leye = tryvar(15)
        reye = tryvar(14)
        nose = tryvar(0)
        neck = tryvar(1)
        lshould = tryvar(5)
        rshould = tryvar(2)
        lhip = tryvar(11)
        rhip = tryvar(8)
        lelb = tryvar(6)
        relb = tryvar(3)
        lwrist = tryvar(7)
        rwrist = tryvar(4)
        lankle = tryvar(13)
        rankle = tryvar(10)
        lknee = tryvar(12)
        rknee = tryvar(9) 
        #head and neck
        if (lear and rear): #head circle if both ears are present
            lx = lear[0]
            rx = rear[0]
            hx = (lx + rx)/2 #Nope
            taneyes = 0 #Bruker heller tangens her for å få en relativ vinkel.
            # Plasser etterpå "midpunktet" "over" basert på vinkel. 
            dx = int(np.linalg.norm(np.array(lear)-np.array(rear)))
            #^relation for headsize, distance between ears
            nx = neck[0] 
            hy =  int((rear[1]+lear[1])/2-dx/2.7) #nope  #fight me
            earringsxl = int((lx+nx)/1.95)
            earringsxr = int((rx+nx)/2.05)  
            earringsy = (nose[1]+neck[1])/2 #neck nose mid
            limblen= int(dx/5.5)
            cv2.circle(npimg, (hx,hy), int(abs(dx*0.5)), col, thickness=limblen, lineType=8, shift=0)
            limblen=dx/4
            cv2.line(npimg, (lx,lear[1]), (earringsxl,earringsy) , col, limblen)
            cv2.line(npimg, (rx,rear[1]), (earringsxr,earringsy) , col, limblen)

        #head pointing left (left eye hidden)
        elif rear :#head circle if right ear is present + faceline
            rx = rear[0]          
            dx = int(leye[0]-reye[0])/4#dist between eyes
            earringsxr = (rx+neck[0])/2
            earringsy = (nose[1]+neck[1])/2 #neck nose mid

            hx = rx+abs(rx-leye[0])/2 #- dx*20 / (rx-leye[0]))
            #Jacob's magic circle coord (next to ear) ?? wtf. fight me
            hy = int((rear[1]+leye[1])/2-dx*3.5)
            limblen = int((dx+abs(rx-leye[0])/2)*0.45)
            cv2.circle(npimg, (hx,hy), int(abs(nose[0]-rx)*0.8), col, thickness=limblen, lineType=8, shift=0)
            limblen = dx
            cv2.line(npimg, (leye[0]+dx,leye[1]), (leye[0]+dx,(nose[1]+neck[1])/2) , col, limblen)
            cv2.line(npimg, (rx,rear[1]), (earringsxr,earringsy) , col,limblen)

                
        elif lear:#head circle if right eye is present + faceline
            lx = lear[0]
            reyex = reye[0] 
            dx = int((leye[0]-reyex)/4)
            earringsxl = int((lx+neck[0])/1.9)
            earringsy = (nose[1]+neck[1])/2 #neck nose mid
            hx = lx - abs(lx-reyex)/2 #+ dx*20. /(lx-reyex))#circle center, next to ear
            hy = int((lear[1]+reye[1])/2-dx*3.5)               #circle center, slightly above ear
            limblen = int((abs(lx-reyex)/2+dx)*0.45)
            cv2.circle(npimg, (hx,hy), int(abs(nose[0]-lx)*0.8), col, thickness=limblen, lineType=8, shift=0)
            limblen=dx
            cv2.line(npimg, (reyex+dx,leye[1]), (reyex+dx,(nose[1]+neck[1])/2) , col, limblen)
            cv2.line(npimg, (lx,leye[1]), (earringsxl,earringsy) ,col, limblen)
    
        
        #shoulder throat connections
        if nose and neck and rshould and lshould: 
            #right shoulder to throat    
            throaty = (nose[1]+neck[1])/2 #neck nose mid
            throatx = (nose[0]+neck[0])/2 #neck nose mid
            limblen = int(abs(rshould[0]-lshould[0]))/6
            #left shoulder to throat
            cv2.line(npimg, (rshould[0],rshould[1]-limblen/2), (throatx,throaty) , col, limblen)
            cv2.line(npimg, (lshould[0],lshould[1]-limblen/2), (throatx,throaty) , col, limblen)


        #shoulder hip connections
        if rhip and rshould: #right hip
            hipy = rhip[1] #neck nose mid
            hipx = rhip[0] #neck nose mid
            shouldx = rshould[0]
            shouldy = rshould[1]
            cv2.line(npimg, (hipx,hipy), (shouldx,shouldy) , col, limblen)

        if lhip and lshould: #left hip
            hipy = lhip[1] #neck nose mid
            hipx = lhip[0] #neck nose mid
            shouldx = lshould[0]
            shouldy = lshould[1]                    
            cv2.line(npimg, (hipx,hipy), (shouldx,shouldy) ,col, limblen)

        if relb and rshould: #right bicep
            
            bowy = relb[1] #neck nose mid
            bowx = relb[0] #neck nose mid
            shouldx = rshould[0]
            shouldy = rshould[1]
            limblen = d*2
            d = int(np.sqrt((bowy-shouldy)*(bowy-shouldy)+(bowx-shouldx)*(bowx-shouldx))/10)
            cv2.line(npimg, (shouldx+2*d,shouldy+2*d), (bowx+2*d,bowy+2*d) , col, limblen)
            cv2.line(npimg, (bowx-d,bowy-d), (shouldx-d,shouldy-d) , col,limblen)

        if lelb and lshould: #left bicep
            
            bowy = lelb[1] #neck nose mid
            bowx = lelb[0] #neck nose mid
            shouldx = lshould[0]
            shouldy = lshould[1]
            d = int(np.sqrt((bowy-shouldy)*(bowy-shouldy)+(bowx-shouldx)*(bowx-shouldx))/10)
            limblen = d*2
            cv2.line(npimg, (shouldx+2*d,shouldy+2*d), (bowx+2*d,bowy+2*d) , col, limblen)
            cv2.line(npimg, (bowx-d,bowy-d), (shouldx-d,shouldy-d) , col, limblen)

        if relb and rwrist: #right elbow-wrist
            bowy = relb[1] #neck nose mid
            bowx = relb[0] #neck nose mid
            wristx = rwrist[0]
            wristy = rwrist[1]
            d = int(np.sqrt((bowy-wristy)*(bowy-wristy)+(bowx-wristx)*(bowx-wristx))/10)
            limblen = d*2
            cv2.line(npimg, (wristx+2*d,wristx+2*d), (bowx+2*d,bowy+2*d) , col, limblen)
            cv2.line(npimg, (bowx-d,bowy-d), (wristx-d,wristy-d) , col,limblen)

        if lelb and lwrist: #left elbow-wrist
            bowy = lelb[1] #neck nose mid
            bowx = lelb[0] #neck nose mid
            wristx = lwrist[0]
            wristy = lwrist[1]
            d = int(np.sqrt((bowy-wristy)*(bowy-wristy)+(bowx-wristx)*(bowx-wristx))/10)
            limblen = d*2

            cv2.line(npimg, (wristx+2*d,wristx+2*d), (bowx+2*d,bowy+2*d) , col, limblen)
            cv2.line(npimg, (bowx-d,bowy-d), (wristx-d,wristy-d) , col,limblen)


    return npimg, centers
