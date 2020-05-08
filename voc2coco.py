
import sys
sys.path.append('./')
import os
import json
import argparse
from tqdm import tqdm
from mmcv.annotation import parse_xml


CALMCAR_DETECTIONV2 = [
    'background',
    'car',
    'bus',
    'truck',
    'person',
    'cyclist',
    'warning',
    'prohibit',
    'indicate',
    'fingerpost',
    'travel',
    'assist',
    'signal_lamp',
    'etc_light',
    'other',
    'barricade'
]

CALMCAR_DETECTIONV3 = [
    'background',
    'car',
    'bus_whole',
    'truck_whole',
    'person',
    'cyclist',
    'warning',
    'prohibit',
    'indicate',
    'fingerpost',
    'travel',
    'assist',
    'signal_lamp',
    'etc_light',
    'other',
    'barricade',
]

CALMCAR_WHEEL = [
    'background',
    'wheel'
]


class Voc2Coco(object):
    def __init__(self, _args):
        self.m_image_set = _args.image_set
        self.m_xml_path = _args.xml_path
        self.m_pics_path = _args.pics_path
        self.m_image_ext = _args.image_ext if _args.image_ext is None else 'png'
        self.m_save_path = _args.save_path
        self.m_dataset = _args.dataset

        self.m_xml_index = None

        self.m_json_dict = {"images":[],
                            "type": "instances",
                            "annotations": [],
                            "categories": []}
        self.m_categories = None

        self._load_categories()
        self._load_xml_index()

    def _get_check_element(self, _root, _name, _length=None):
        """
        Acquire xml element, and check whether it is valid?
        :param _root: root element
        :param _name: element name
        :param _length: nums of child element
        :return: element value, xml element
        """
        elements = _root.findall(_name)

        if 0 == len(elements):
            raise ValueError('Can not find %s in %s' % (_name, _root.tag))

        if _length is not None:
            if _length > 0 and len(elements) != _length:
                raise ValueError('The nums of %s is supposed to be %d, '
                                 'but is %d' % (_name, _length, len(elements)))
            if 1 == _length:
                elements = elements[0]

        return elements

    def _load_categories(self):
        if self.m_dataset == 'CalmCar_DetectionV2':
            cats = CALMCAR_DETECTIONV2
        elif self.m_dataset == 'CalmCar_DetectionV3':
            cats = CALMCAR_DETECTIONV3
        elif self.m_dataset == 'CALMCAR_WHEEL':
            cats = CALMCAR_WHEEL
        else:
            raise ValueError("Unsupported dataset type")

        self.m_categories = dict(zip(cats, range(len(cats))))
        # self.m_categories = cats

        # base_path = os.path.dirname(__file__)
        # category_path = os.path.join(base_path, "dataset", "%s.label" % self.m_dataset)
        # with open(category_path, 'r') as fcat:
        #     cats = fcat.readlines()
        #     cats = list(map(lambda x:x.strip(), cats))
        #     self.m_categories = dict(zip(cats, range(len(cats))))

    def _load_xml_index(self):
        with open(self.m_image_set, 'r') as fsets:
            self.m_xml_index = list(map(lambda x:x.strip(), fsets.readlines()))

    def convert(self):
        # 遍历所有的XML文件
        bnd_id = 1
        image_id = 1

        for xml_idx in tqdm(range(len(self.m_xml_index)), ncols=100, desc="VOC2COCO"):
            xml = self.m_xml_index[xml_idx]
            abs_xml_path = os.path.join(self.m_xml_path, "%s.xml" % xml)
            if not os.path.exists(abs_xml_path):
                raise ValueError("Non existed xml path: %s" % abs_xml_path)

            annotaion = parse_xml(abs_xml_path)

            image_des = annotaion['image']
            image_des['id'] = image_id

            abs_image_path = os.path.join(self.m_pics_path, image_des['file_name'])
            if not os.path.exists(abs_image_path):
                tqdm.write("Non existed pic path: %s" % abs_image_path)
                continue

            self.m_json_dict['images'].append(image_des)

            # TODO: Support segmentation. Currently we do not support segmentation.
            objs = annotaion['annotation']
            if len(objs) == 0:
                tqdm.write(" There is no objects in xml : %s" % os.path.basename(xml))
            for obj in objs:
                # 所有标签均以小写格式保存，兼容xml中出现大写字母的情况
                category = obj['name'].lower()
                if category in ['tricycle', 'cyclist']:
                    category = 'cyclist'
                elif category in ['truck_head', 'truck_tail', 'truck head', 'truck tail']:
                    category = 'truck'
                elif category in ['bus_head', 'bus_tail', 'bus head', 'bus tail']:
                    category = 'bus'

                # 排除不需要的标签
                if category not in self.m_categories:
                    continue

                category_id = self.m_categories[category]
                xmin, ymin, xmax, ymax = obj['bndbox']
                area = (xmax - xmin + 1) * (ymax - ymin + 1)

                # TODO： 忽略小目标
                # FCM： 有针对的忽略部分目标
                # """
                # Barricade: 只检测面积大于40*40的目标
                # Traffic_Light: 只检测面积大于 8 * 8的目标
                # Sign: 只检测面积大于 20 * 20 的目标
                # Person: 忽略宽度小于 10 的目标
                # Truck: 忽略面积小于 20*20的目标
                # Bus: 忽略面积小于 20*20的目标, 不做任何处理
                # Car: 忽略面积小于 10*10的目标, 不做任何处理
                # Cyclist: area > 15 * 15
                # """
                # if category == "barricade":
                #     if area < 40 * 40:
                #         continue
                # elif category in ['truck_whole', 'bus_whole']:
                #     pass
                #     # if area < 20 * 20:
                #     #     continue
                # elif category == "person":
                #     if xmax - xmin + 1 < 10:
                #         continue
                # elif category in ['warning', 'prohibit', 'indicate', 'fingerpost', 'travel', 'assist', 'other']:
                #     if area < 20 * 20:
                #         continue
                # elif category == 'signal_lamp':
                #     if area < 8 * 8:
                #         continue

                # BSD
                """
                Only care about Vechiles, person, cyclist
                TrucK: area > 20 * 20
                Bus: area > 15 * 15
                Car: area > 30 * 30
                Person: width > 20
                Cyclist: area > 20 * 20
                """
                # if category in ['truck_whole', 'bus_whole']:
                #     if area < 20 * 20:
                #         continue
                # elif category == "person":
                #     if xmax - xmin + 1 < 20:
                #         continue
                # elif category == "cyclist":
                #     if xmax - xmin + 1 < 20:
                #         continue
                # elif category == 'car':
                #     if area < 30 * 30:
                #         continue
                # else:
                #     continue

                obj_annotation = {'area': area, 'iscrowd': 0,
                                   'bbox': [xmin, ymin, xmax - xmin + 1, ymax - ymin + 1],
                                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                                   'segmentation': [], 'image_id': image_id}
                self.m_json_dict['annotations'].append(obj_annotation)

                bnd_id += 1

            image_id += 1
        # category
        for category, category_id in self.m_categories.items():
            #ignore background
            if category == 'background':
                continue
            self.m_json_dict['categories'].append({'supercategory': 'none', 'id': category_id, 'name': category})

        print(len(self.m_json_dict['images']), len(self.m_xml_index))
        # save json
        with open(self.m_save_path, 'w') as fjson:
            json.dump(self.m_json_dict, fjson)


def parse_args():
    parser = argparse.ArgumentParser("Transform pascal format annotations into coco format!")
    parser.add_argument('image_set', help='xml list file.')
    parser.add_argument('xml_path', help='Path including xml files.')
    parser.add_argument('pics_path', help='Path including pictures files.')
    parser.add_argument('save_path', help='Path to save json annotation file.')
    parser.add_argument('dataset', help='Must specify the dataset, '
                                        'and script will load responding label file automaticly.')
    parser.add_argument('--check-size', dest='check_size', help="Whether to check image size")
    parser.add_argument('--image-ext', dest='image_ext', help="Image's extention")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    cvt = Voc2Coco(_args=args)
    cvt.convert()