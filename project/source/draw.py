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


        #head and neck
        if (16 in Centers.keys())*(17 in Centers.keys()): #head circle if both ears are present
            try:                                             #+ neckline
                lx = Centers[17][0]
                rx = Centers[16][0]
                hx = (lx + rx)/2 
                dx = (lx - rx) #relation for headsize, distance between ears
                nx = Centers[1][0]
                hy =  int((Centers[16][1]+Centers[17][1])/2-dx/2.7)
                earringsxl = int((lx+nx)/1.95)
                earringsxr = int((rx+nx)/2.05)  
                earringsy = (Centers[0][1]+Centers[1][1])/2 #neck nose mid
                limblen= int(dx/5.5)
                cv2.circle(npimg, (hx,hy), int(abs(dx*0.6)), col, thickness=limblen, lineType=8, shift=0)
                limblen=dx/4
                cv2.line(npimg, (lx,Centers[17][1]), (earringsxl,earringsy) , col, limblen)
                cv2.line(npimg, (rx,Centers[16][1]), (earringsxr,earringsy) , col, limblen)
            except:
                print "Observation Error: check if expression regarding both ears"

        #head pointing left (left eye hidden)
        elif (16 in Centers.keys()):#head circle if right eye is present + faceline
            try:
                rx = Centers[16][0]
                dx = (Centers[15][0]-Centers[14][0])/4#dist between eyes
                earringsxr = (rx+Centers[1][0])/2
                earringsy = (Centers[0][1]+Centers[1][1])/2 #neck nose mid

                hx = rx+abs(rx-Centers[15][0])/2 #- dx*20 / (rx-Centers[15][0])) #Jacob's magic circle coord (next to ear)
                hy = int((Centers[16][1]+Centers[15][1])/2-dx*3.5)
                limblen = int((dx+abs(rx-Centers[15][0])/2)*0.45)
                cv2.circle(npimg, (hx,hy), int(abs(Centers[0][0]-rx)*0.8), col, thickness=limblen, lineType=8, shift=0)
                limblen = dx
                cv2.line(npimg, (Centers[15][0]+dx,Centers[15][1]), (Centers[15][0]+dx,(Centers[0][1]+Centers[1][1])/2) , col, limblen)
                cv2.line(npimg, (rx,Centers[16][1]), (earringsxr,earringsy) , col,limblen)

            except:
                print "Observation Error: left eye disappeared"


        #head pointing right (right eye hidden)
        elif (17 in Centers.keys()):#head circle if right eye is present + faceline
            try:
                lx = Centers[17][0]
                dx = int((Centers[15][0]-Centers[14][0])/4)
                earringsxl = int((lx+Centers[1][0])/1.9)
                earringsy = (Centers[0][1]+Centers[1][1])/2 #neck nose mid
                hx = lx - abs(lx-Centers[14][0])/2 #+ dx*20. /(lx-Centers[14][0]))#circle center, next to ear
                hy = int((Centers[17][1]+Centers[14][1])/2-dx*3.5)               #circle center, slightly above ear
                limblen = int((abs(lx-Centers[14][0])/2+dx)*0.45)
                cv2.circle(npimg, (hx,hy), int(abs(Centers[0][0]-lx)*0.8), col, thickness=limblen, lineType=8, shift=0)
                limblen=dx
                cv2.line(npimg, (Centers[14][0]+dx,Centers[15][1]), (Centers[14][0]+dx,(Centers[0][1]+Centers[1][1])/2) , col, limblen)
                cv2.line(npimg, (lx,Centers[17][1]), (earringsxl,earringsy) ,col, limblen)

            except:
                print "Observation Error: right eye disappeared"

        #shoulder throat connection
        try:
            if (5 in Centers.keys())*(2 in Centers.keys()): #right shoulder to throat
                
                throaty = int((Centers[0][1]+Centers[1][1])/2) #neck nose mid
                throatx = (Centers[0][0]+Centers[1][0])/2 #neck nose mid
                limblen = int(abs(Centers[2][0]-Centers[5][0]))/6
                cv2.line(npimg, (Centers[2][0],Centers[2][1]-limblen/2), (throatx,throaty) , col, limblen)
            if (2 in Centers.keys())*(5 in Centers.keys()): #left shoulder to throat
                throaty = int((Centers[0][1]+Centers[1][1])/2) #neck nose mid
                throatx = (Centers[0][0]+Centers[1][0])/2 #neck nose mid
                limblen = int(abs(Centers[2][0]-Centers[5][0]))/6
                cv2.line(npimg, (Centers[5][0],Centers[5][1]-limblen/2), (throatx,throaty) , col, limblen)
        except:
            print "Observation Error: nose disappeared"
        #shoulder hip connection
        try:
            if (8 in Centers.keys())*(2 in Centers.keys()): #right hip
                hipy = Centers[8][1] #neck nose mid
                hipx = int(Centers[8][0]) #neck nose mid
                shouldx = Centers[2][0]
                shouldy = Centers[2][1]
                cv2.line(npimg, (hipx,hipy), (shouldx,shouldy) , col, limblen)
            if (11 in Centers.keys())*(5 in Centers.keys()): #left hip
                hipy = Centers[11][1] #neck nose mid
                hipx = int(Centers[11][0]) #neck nose mid
                shouldx = Centers[5][0]
                shouldy = Centers[5][1]                    
                cv2.line(npimg, (hipx,hipy), (shouldx,shouldy) ,col, limblen)
        except:
            print "'T H I C C' Error: Your hips are missing"
        
        try:
            if (2 in Centers.keys())*(3 in Centers.keys()): #right hip
                
                bowy = Centers[3][1] #neck nose mid
                bowx = int(Centers[3][0]) #neck nose mid
                shouldx = Centers[2][0]
                shouldy = Centers[2][1]
                d = int(np.sqrt((bowy-shouldy)*(bowy-shouldy)+(bowx-shouldx)*(bowx-shouldx))/6)
                cv2.line(npimg, (hipx+d,hipy+d), (shouldx+d,shouldy+d) , col, limblen)

                cv2.line(npimg, (hipx-d,hipy-d), (shouldx-d,shouldy-d) , col, limblen)
            '''if (5 in Centers.keys())*(6 in Centers.keys()): #left hip
                y = Centers[11][1] #neck nose mid
                x = int(Centers[11][0]) #neck nose mid
                shouldx = Centers[5][0]
                shouldy = Centers[5][1]                    
                cv2.line(npimg, (hipx,hipy), (shouldx,shouldy) ,col, limblen)
            '''
        except:
            print "A"
            Nose = 0
    '''        
    Neck = 1
    RShoulder = 2
    RElbow = 3
    RWrist = 4
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8
    RKnee = 9
    RAnkle = 10
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14
    LEye = 15
    REar = 16
    LEar = 17
    Background = 18
    '''
    return npimg, centers