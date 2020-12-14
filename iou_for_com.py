import os
import datetime
import json
import xml.etree.ElementTree as ET
import time
import numpy as np


def gtaxis(path):
    dict = {}
    for filename in os.listdir(path):
        tree = ET.parse(os.path.join(path, filename))  # 解析读取xml函数
        file = tree.find('filename').text
        bbox = tree.findall('object')[0].find('bndbox')
        list = [int(bbox.find('xmin').text),
                int(bbox.find('ymin').text),
                int(bbox.find('xmax').text),
                int(bbox.find('ymax').text)]
        dict[file] = list
    return dict


def testaxis(path):
    objects = {}
    for filename in os.listdir(path):
        if filename.split('.')[-1] == 'manifest':
            continue
        if filename.split('.')[1] == 'jpg_1_result':
            continue
        jpgfile = filename.split('.')[0] + '.jpg'
        file = open(os.path.join(path, filename), "r").readline()
        list = []
        file = json.loads(file)
        detection = file["detection_boxes"]
        confidence = file["detection_scores"]
        for i, x in enumerate(detection):
            tmp = {"bbox": [float(x[1]), float(x[0]), float(x[3]), float(x[2])], "confidence": confidence[i]}
            list.append(tmp)
        objects[jpgfile] = list
    return objects


def iou(bb_test, bb_gt):
    xx1 = max(bb_test[0], bb_gt[0])
    yy1 = max(bb_test[1], bb_gt[1])
    xx2 = min(bb_test[2], bb_gt[2])
    yy2 = min(bb_test[3], bb_gt[3])
    w = max(0., xx2 - xx1)
    h = max(0., yy2 - yy1)
    area = w * h
    score = area / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1])
                    + (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - area)
    return score


def takeconf(elem):
    return elem["confidence"]


threshold = 0.9
bottledict = {"circle": 'circle_annotations', "ellipse": 'ellipse_annotations', "waterdrop": 'waterdrop_annotations'}
root = "D:\my university\computer vision\\final"
gtdir = os.path.join(root, "bottle")
testdir = os.path.join(root, "common_exp")
outputdir = os.path.join(root, "result-threshold-" + str(threshold) + ".json")
# outputdir = os.path.join(root, "result-" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".json")
_, dirs, _ = next(os.walk(testdir))
list1, list2, list3 = [], [], []
for dir in dirs:
    if (dir == 'allfile') or (dir == 'drawrec'):
        continue
    if dir.split("-")[-1] == "cir" or dir.split("-")[-1] == "circle":
        list1.append(dir)
    if dir.split("-")[-1] == "elli" or dir.split("-")[-1] == "ellipse":
        list2.append(dir)
    if dir.split("-")[-1] == "water" or dir.split("-")[-1] == "waterdrop":
        list3.append(dir)
dict = {"circle": list1, "ellipse": list2, "waterdrop": list3}
outdict = {}

for key, value in bottledict.items():
    gtdict = gtaxis(os.path.join(gtdir, value))
    allgt = len(gtdict)
    for tval in dict[key]:
        print(tval)
        testdict = testaxis(os.path.join(testdir, tval))
        maxscore, maxpos = 0, -1
        list = []
        sumiou = 0.0
        times = 0
        for img, gtbox in gtdict.items():
            testboxes = testdict[img]
            # print(img,testboxes,gtbox)
            for i, testbox in enumerate(testboxes):
                detection = testbox["bbox"]
                score = iou(detection, gtbox)
                if score > maxscore:
                    maxscore = score
                    maxpos = i
            # print(maxscore)
            for i, x in enumerate(testboxes):
                if (i == maxpos) and (maxscore > threshold):
                    list.append({"confidence": x["confidence"], "tp": 1})
                    sumiou += maxscore
                    times += 1
                else:
                    list.append({"confidence": x["confidence"], "tp": 0})

        sumiou = 0 if times == 0 else sumiou / times
        print("mIoU = %f" % round(sumiou, 4))
        list.sort(reverse=True, key=takeconf)
        Plist, Rlist = [], []
        sumTP = 0
        for i, x in enumerate(list):
            if x["tp"] == 1:
                sumTP += 1
            Plist.append(sumTP / (i + 1))
            Rlist.append(sumTP / allgt)
        pnp = np.array(Plist)
        rnp = np.array(Rlist)
        ap = 0
        pre = 0
        for t in np.arange(0.0, 1.1, 0.1):
            if np.sum(rnp >= t) == 0:
                pre = 0
            else:
                pre = np.max(pnp[rnp >= t])
            # print(pre)
            ap += pre / 11
        print("AP = %f" % round(ap, 4))
        outdict[tval] = {"mIoU": round(sumiou, 4), "AP": round(ap, 4)}

writes = open(outputdir, "w")
writes.write(str(outdict))
writes.close()
