from model import YOLOv4
import cv2
from torch.backends import cudnn
import argparse
import torch
import utils
import time

coco_dict = {0: 'person',
            1: 'bicycle',
            2: 'car',
            3: 'motorbike',
            4: 'aeroplane',
            5: 'bus',
            6: 'train',
            7: 'truck',
            8: 'boat',
            9: 'traffic light',
            10: 'fire hydrant',
            11: 'stop sign',
            12: 'parking meter',
            13: 'bench',
            14: 'bird',
            15: 'cat',
            16: 'dog',
            17: 'horse',
            18: 'sheep',
            19: 'cow',
            20: 'elephant',
            21: 'bear',
            22: 'zebra',
            23: 'giraffe',
            24: 'backpack',
            25: 'umbrella',
            26: 'handbag',
            27: 'tie',
            28: 'suitcase',
            29: 'frisbee',
            30: 'skis',
            31: 'snowboard',
            32: 'sports ball',
            33: 'kite',
            34: 'baseball bat',
            35: 'baseball glove',
            36: 'skateboard',
            37: 'surfboard',
            38: 'tennis racket',
            39: 'bottle',
            40: 'wine glass',
            41: 'cup',
            42: 'fork',
            43: 'knife',
            44: 'spoon',
            45: 'bowl',
            46: 'banana',
            47: 'apple',
            48: 'sandwich',
            49: 'orange',
            50: 'broccoli',
            51: 'carrot',
            52: 'hot dog',
            53: 'pizza',
            54: 'donut',
            55: 'cake',
            56: 'chair',
            57: 'sofa',
            58: 'pottedplant',
            59: 'bed',
            60: 'diningtable',
            61: 'toilet',
            62: 'tvmonitor',
            63: 'laptop',
            64: 'mouse',
            65: 'remote',
            66: 'keyboard',
            67: 'cell phone',
            68: 'microwave',
            69: 'oven',
            70: 'toaster',
            71: 'sink',
            72: 'refrigerator',
            73: 'book',
            74: 'clock',
            75: 'vase',
            76: 'scissors',
            77: 'teddy bear',
            78: 'hair drier',
            79: 'toothbrush'}

cudnn.fastest = True
cudnn.benchmark = True
global confidence_threshold, iou_threshold
confidence_threshold = 0.5
iou_threshold = 0.5


def run_visualisation(x, bboxes, labels, h, w):
    arr = utils.get_img_with_bboxes(x.cpu(), bboxes[0].cpu(), resize=False, labels=labels[0])
    arr =  cv2.resize(arr,(w, h))
    arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    cv2.imshow("test", arr)
    cv2.imwrite('prediction.png', arr)

def run_inference(model, img):
    anchors, _ = model(img[None].cuda())
    bboxes, labels = utils.get_bboxes_from_anchors(anchors, confidence_threshold, iou_threshold, coco_dict)

    return bboxes, labels


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, help='an integer for the accumulator')
    args = parser.parse_args()
    
    m = YOLOv4(pretrained=True, sam=False, eca=False)
    m.requires_grad_(False)
    m.eval()

    m = m.cuda()
    #To warm up JIT
    m(torch.zeros((1, 3, 608, 608)).cuda())

    #reading and preprocessing image
    img = cv2.imread(args.img_path)
    h, w, _ = img.shape
    sized = cv2.resize(img, (m.img_dim, m.img_dim))
    sized = cv2.cvtColor(sized, cv2.COLOR_BGR2RGB)
    x = torch.from_numpy(sized)
    x = x.permute(2, 0, 1)
    x = x.float()
    x /= 255  

    bboxes, labels = run_inference(m, x)
    run_visualisation(x, bboxes, labels, h, w)



