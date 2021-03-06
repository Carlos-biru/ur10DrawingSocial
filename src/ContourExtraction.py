import cv2


def ImageContoursCustomSet1(img, isTesting=False):
    try:
        cimg2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        gray = cv2.cvtColor(cimg2, cv2.COLOR_BGR2GRAY)
    except:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = 255 - gray
    _, cnts, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lstcont = []
    for i in cnts:
        cont = []
        for y in i:
            cont.append([y[0][0], y[0][1]])
        lstcont.append(cont)
    return lstcont


def ImageContoursCustomSet2(img, isTesting=False):
    try:
        cimg2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        gray = cv2.cvtColor(cimg2, cv2.COLOR_BGR2GRAY)
    except:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = 255 - gray
    cv2.imshow('', gray)
    cv2.waitKey(2020202)
    # _,cnts,_=cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findNonZero(gray)
    lstcont = []
    for i in cnts:
        lstcont.append([i[0, 0], i[0, 1]])
    return lstcont


# print ImageContoursCustomSet2(cv2.imread('/home/naodev/Documents/default_ROSws/src/ur10DrawingSocial/robot_img_v2/human_2.png'))


def JamesContourAlg(img):
    import math, numpy as np
    # dist thesh == 14, ep_val == 0.0015
    dist_thresh = 14  # 8 #14
    ep_val = 0.00015
    retval, gray = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV)
    print('James contour code')
    #  cv2.imshow('',gray)
    # cv2.waitKey(200)
    # Code to find contours
    cnts, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lstcont = []
    approx = []

    for c in cnts:
        # Simplify
        epsilon = ep_val * cv2.arcLength(c, False)
        approx.append(cv2.approxPolyDP(c, epsilon, False))

    for c in approx:
        isEmpty = True
        cont = []
        pv = c[0][0]
        for p in c:
            point = np.array([p[0, 0], p[0, 1]])
            # print point
            if math.sqrt((pv[0] - point[0]) * (pv[0] - point[0]) + (pv[1] - point[1]) * (
                pv[1] - point[1])) >= dist_thresh:
                cont.append(point)
                isEmpty = False
                pv = point
        if isEmpty == False:
            lstcont.append(cont)

    temp_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    c_i = 0
    for c in lstcont:
        # print(lstcont)
        print('____________________________________________________________')
        print(c)
        print('____________________________________________________________')
        # pv = c
        isFirst = True
        for p in c:
            cn = (p[0], p[1])
            # print(cn)
            if isFirst == True:
                pv = cn
                isFirst = False
            # if euclidean_dist(pv, cn) > dist_thresh:
            if (c_i == 0):
                cv2.line(temp_img, pv, cn, color=(255, 0, 0), thickness=1)
            elif (c_i == 1):
                cv2.line(temp_img, pv, cn, color=(0, 255, 0), thickness=1)
            else:
                cv2.line(temp_img, pv, cn, color=(0, 0, 255), thickness=1)
            pv = cn

            c_i += 1
            if c_i >= 3:
                c_i = 0

    cv2.imshow('Results', temp_img)
    cv2.waitKey(500)


    return lstcont