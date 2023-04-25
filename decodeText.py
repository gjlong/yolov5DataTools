import cv2
import os
import json
import base64
import xml.etree.ElementTree as ET


def convert_yolo_value(box, img):
    '''
        yolo value convert to labelme value
    '''
    x, y, w, h = box[0], box[1], box[2], box[3]
    # math x1 x2 y1 y2
    x2 = (2 * x + w) * img.shape[1] / 2
    x1 = x2 - w * img.shape[1]

    y2 = (2 * y + h) * img.shape[0] / 2
    y1 = y2 - h * img.shape[0]
    new_box = [x1, y1, x2, y2]
    new_box = list(map(int, new_box))
    return new_box


def parse_img_txt(img_path, txt_path):
    '''
        parse the txt file
    '''
    name_label = ['dog']  # class name list example:'dog'
    img = cv2.imread(img_path)
    f = open(txt_path)
    bboxes = []
    for line in f.readlines():
        line = line.split(" ")
        if len(line) == 5:
            obj_label = name_label[int(line[0])]
            x = float(line[1])
            y = float(line[2])
            w = float(line[3])
            h = float(line[4])
            box = convert_yolo_value([x, y, w, h], img)
            box.append(obj_label)
            bboxes.append(box)
    return img, bboxes

def get_json(img_path, txt_path):
    """
    build json data
    """
    label_dict = {}
    label_dict["version"] = "5.2.0" # labelme version
    label_dict["flags"] = {}
    img, bboxes = parse_img_txt(img_path, txt_path)
    shape_list = []
    for box in bboxes:
        shape_dict = {}
        shape_dict["label"] = box[-1]  # label name
        shape_dict["points"] = [[box[0], box[1]], [box[2], box[3]]]
        shape_dict["group_id"] = None
        shape_dict["description"] = ""
        shape_dict["shape_type"] = "rectangle"  # labelme type 'rectangle'
        shape_dict["flags"] = {}
        shape_list.append(shape_dict)
    label_dict["shapes"] = shape_list
    label_dict["imagePath"] = os.path.basename(img_path)  # image file path
    # 读取图像的的数据并转成base64编码格式
    with open(img_path, "rb") as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        base64_str = str(base64_data, 'utf-8')
        label_dict["imageData"] = base64_str  # labelme的json文件默认存放了图像的base64编码。这样的设计可以保证，如果图像路径有问题仍然能够打开文件

    label_dict["imageHeight"] = img.shape[0]  # image height
    label_dict["imageWidth"] = img.shape[1]  # image width

    return label_dict


def generateJsonFile(img_files_path, txt_files_path, save_jsons_path):
    if os.path.exists(save_jsons_path) is False:
        os.makedirs(save_jsons_path)
    img_list = os.listdir(img_files_path)
    for nums, filename in enumerate(img_list):
        if os.path.splitext(filename)[-1][1:] == "jpg":
            img_path = os.path.join(img_files_path, filename)
            txt_name = os.path.splitext(filename)[0] + ".txt"  # 默认jpg和txt文件同名
            txt_path = os.path.join(txt_files_path, txt_name)
            if os.path.exists(txt_path) is False:  # 判断是否有txt文件的数据，没有就直接创建一个空的txt文件
                with open(txt_path, 'w') as f:
                    f.write("")

            json_path = os.path.join(save_jsons_path, filename.replace("jpg", "json"))
            with open(json_path, 'w') as f:
                f.write(json.dumps(get_json(img_path, txt_path), ensure_ascii=False, indent=4, separators=(',', ':')))


if __name__ == '__main__':
    img_files_path = "/images"  # 图片文件夹路径
    txt_files_path = "/labels"  # txt文件夹路径
    save_jsons_path = "/jsons"  # 要保存的json文件夹路径
    generateJsonFile(img_files_path, txt_files_path, save_jsons_path)