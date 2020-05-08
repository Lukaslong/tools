'''
Used for writing detecting results into xml just like annotation file
Usage: from xml_generate import gen_xml
Created by ZhaoYinglong
'''
import os
import mmcv
import numpy as np
from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString

def gen_xml(result,names_class,score_thr,image_path,outfolder):
    '''
    Args:
        result(n, 4 or 5): detecting results
        names_class: list of class names
        score_thr(float): threshold of score
        image_path: full path of detected image
        outfolder: folder to store xmls
    '''

    img=mmcv.imread(image_path)

    img_name=image_path.split('/')[-1]
    xml_name=os.path.splitext(img_name)[0]+'.xml'
    folder_name=image_path.split('/')[-2]
    out_xml=os.path.join(outfolder,xml_name)

    # define title and fundamental info about xml
    node_root=Element('prediction')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = folder_name
    
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = img_name

    node_path=SubElement(node_root, 'path')
    node_path.text=image_path

    node_source=SubElement(node_root,'source')
    node_source_database=SubElement(node_source,'database')
    node_source_database.text='Unknown'

    # size info
    node_size=SubElement(node_root,'size')
    node_size_width=SubElement(node_size,'width')
    node_size_width.text=str(img.shape[1])
    node_size_height=SubElement(node_size,'height')
    node_size_height.text=str(img.shape[0])
    node_size_depth=SubElement(node_size,'depth')
    node_size_depth.text=str(img.shape[2])

    # segmented
    node_segmented=SubElement(node_root,'segmented')
    node_segmented.text='0'

    # detection results processing
    if isinstance(result, tuple):
        bbox_result, segm_result = result
    else:
        bbox_result, segm_result = result, None
    bboxes = np.vstack(bbox_result)

    if isinstance(bbox_result, np.ndarray):
        labels = np.zeros(bbox_result.shape[0], dtype=np.int32)
    else:
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)

    if score_thr > 0:
        assert bboxes.shape[1] == 5
        scores = bboxes[:, -1]
        inds = scores > score_thr
        bboxes = bboxes[inds, :]
        labels = labels[inds]

    # store filtered objects
    for bbox, label in zip(bboxes, labels):
        if label in [14, 15]:
            continue

        bbox_int = bbox.astype(np.int32)
        label_text = names_class[label] if names_class is not None else 'cls {}'.format(label)

        node_object=SubElement(node_root,'object')
        object_name=SubElement(node_object,'name')
        object_name.text=label_text
        object_pose=SubElement(node_object,'pose')
        object_pose.text='Unspecified'
        object_truncated=SubElement(node_object,'truncated')
        object_truncated.text='0'
        object_difficult=SubElement(node_object,'difficult')
        object_difficult.text='0'
        object_objectId=SubElement(node_object,'objectId')
        object_objectId.text='None'
        object_angle=SubElement(node_object,'angle')
        object_angle.text='None'
        object_occlusion=SubElement(node_object,'occlusion')
        object_occlusion.text='None'
        object_truncation=SubElement(node_object,'truncation')
        object_truncation.text='None'
        object_constraint=SubElement(node_object,'constraint')
        object_constraint.text='0'
        

        object_bndbox=SubElement(node_object,'bndbox')
        bndbox_xmin=SubElement(object_bndbox,'xmin')
        bndbox_xmin.text=str(bbox_int[0])
        bndbox_ymin=SubElement(object_bndbox,'ymin')
        bndbox_ymin.text=str(bbox_int[1])
        bndbox_xmax=SubElement(object_bndbox,'xmax')
        bndbox_xmax.text=str(bbox_int[2])
        bndbox_ymax=SubElement(object_bndbox,'ymax')
        bndbox_ymax.text=str(bbox_int[3])

    xml = tostring(node_root, pretty_print=True) 
    dom = parseString(xml)
    with open(out_xml,'w') as f:
        dom.writexml(f)