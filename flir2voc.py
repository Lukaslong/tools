'''
Used to convert FLIR annotations to pascal voc format.
Usage:
    python flir2voc.py --jsonpath xxxx --savepath xxxx
Created by ZhaoYinglong
'''
import os
import cv2
import glob
import lxml
import json
import pprint
import argparse
from xml.dom.minidom import parseString
from lxml.etree import Element, SubElement, tostring

def json_voc(jsonfile,savepath):
    with open(jsonfile) as jf:
        data = json.load(jf)
        images = data['images']
        annotations = data['annotations']
        classes=data['categories']
    
    # labels
    labels=[]
    for dic in classes:
        labels.append(dic['name'])
    
    path='/'.join(jsonfile.split('/')[:-1])
    folder_name=images[0]['file_name'].split('/')[0]
    
    j=0
    for i in range(len(images)):
        img_path=images[i]['file_name']
        img_name=img_path.split('/')[-1]
        img=cv2.imread(os.path.join(path,img_path))

        # Create Tree Node
        node_root=Element('annotation')
        node_folder = SubElement(node_root, 'folder')
        node_folder.text = folder_name
        # filename
        node_filename=SubElement(node_root,'filename')
        node_filename.text=img_name
        # path
        node_path=SubElement(node_root,'path')
        node_path.text=img_path
        # source
        node_source=SubElement(node_root,'source')
        node_source.text='FLIR'
        # size
        node_size=SubElement(node_root,'size')
        size_width=SubElement(node_size,'width')
        size_width.text=str(img.shape[1])
        size_height=SubElement(node_size,'height')
        size_height.text=str(img.shape[0])
        size_depth=SubElement(node_size,'depth')
        size_depth.text=str(img.shape[2])
        # segmented
        node_seg=SubElement(node_root,'segmented')
        node_seg.text='0'

        while annotations[j]['image_id']==i:
            ann=annotations[j]
            category_id=ann['category_id']
            label=labels[category_id-1]
            bbox=ann['bbox']

            # info about annotated object
            node_object=SubElement(node_root,'object')
            object_name=SubElement(node_object,'name')
            object_name.text=label
            object_pose=SubElement(node_object,'pose')
            object_pose.text='Unspecified'
            object_truncated=SubElement(node_object,'truncated')
            object_truncated.text='0'
            object_difficult=SubElement(node_object,'difficult')
            object_difficult.text='0'

            # bounding box
            object_bndbox=SubElement(node_object,'bndbox')
            bndbox_xmin=SubElement(object_bndbox,'xmin')
            bndbox_xmin.text=str(bbox[0])
            bndbox_ymin=SubElement(object_bndbox,'ymin')
            bndbox_ymin.text=str(bbox[1])
            bndbox_xmax=SubElement(object_bndbox,'xmax')
            bndbox_xmax.text=str(bbox[0]+bbox[2])
            bndbox_ymax=SubElement(object_bndbox,'ymax')
            bndbox_ymax.text=str(bbox[1]+bbox[3])

            j+=1
            if j>=len(annotations):
                break

        xml = tostring(node_root, pretty_print=True) 
        dom = parseString(xml)
        xmlname=os.path.splitext(img_name)[0]+'.xml'
        out_xml=os.path.join(savepath,xmlname)
        with open(out_xml,'w') as xmlf:
            dom.writexml(xmlf)
            

def main(args):
    jsonpath=args.jsonpath
    savepath=args.savepath
    json_voc(jsonpath,savepath)

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='convert json annotation to voc')
    parser.add_argument('--jsonpath',type=str,help='path to json file')
    parser.add_argument('--savepath',default='temp',type=str,help='path to save output')
    args=parser.parse_args()

    main(args)