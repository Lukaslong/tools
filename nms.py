import torch

def area_of(left_top,right_bottom)->torch.Tensor:
    """Compute the areas of rectangles given two corners.

    Args:
        left_top (N, 2): left top corner.
        right_bottom (N, 2): right bottom corner.

    Returns:
        area (N): return the area.
    """

    # clamp: make result between min and max
    # here to ensure h&w >0
    hw=torch.clamp(right_bottom-left_top,min=0.0)
    return hw[...,0]*hw[...,1]

def iou_of(boxes0,boxes1,eps=1e-5):
    """Return intersection-over-union (Jaccard index) of boxes.

    Args:
        boxes0 (N, 4): ground truth boxes.
        boxes1 (N or 1, 4): predicted boxes.
        eps: a small number to avoid 0 as denominator.
    Returns:
        iou (N): IoU values.
    """

    left_top=torch.max(boxes0[...,:2],boxes1[...,:2])
    right_bottom=torch.min(boxes0[...,2:],boxes1[...,2:])
    area_boxes0=area_of(boxes0[...,:2],boxes0[...,2:])
    area_boxes1=area_of(boxes1[...,:2],boxes1[...,2:])
    area_iou=area_of(left_top,right_bottom)
    
    return area_iou/(area_boxes0+area_boxes1-area_iou+eps)

def hard_nms(boxes_scores,iou_threshold,top_k=-1,candidate_size=200):
    scores=boxes_scores[:,-1]
    boxes=boxes_scores[:,:-1]
    picked=[]
    _,indexes=scores.sort(descending=True)
    indexes=indexes[:candidate_size]
    while len(indexes)>0:
        current=indexes[0]
        current_box=boxes[current,:]

        #current is a tensor, use item() get value
        picked.append(current.item()) 
        if len(picked)==top_k or len(indexes)==1:
            break
        indexes=indexes[1:]
        rest_boxes=boxes[indexes,:]
        iou=iou_of(rest_boxes,current_box.unsqueeze(0))
        indexes=indexes[iou<=iou_threshold]
    return boxes_scores[picked,:]
