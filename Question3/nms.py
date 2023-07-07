import numpy as np
from lca import BinaryLCA

def nms_with_class_hierarchy(boxes, scores, classes, lca, score_thresh, iou_thresh):
    # Filter boxes based on confidence threshold
    filtered_boxes = [box for box, score in zip(boxes, scores) if score >= score_thresh]
    
    # Sort the filtered boxes by confidence score in descending order
    sorted_indices = sorted(range(len(filtered_boxes)), key=lambda i: scores[i], reverse=True)
    sorted_boxes = [filtered_boxes[i] for i in sorted_indices]
    sorted_scores = [scores[i] for i in sorted_indices]
    sorted_classes = [classes[i] for i in sorted_indices]
    
    selected_indices = np.zeros(len(sorted_boxes), dtype=np.int32)
    
    for i in range(len(sorted_boxes)):
        if selected_indices[i] == -1:
            continue
        selected_indices[i] = 1
        
        # Compare with remaining boxes
        for j in range(i + 1, len(sorted_boxes)):            
            box_i = sorted_boxes[i]

            box_j = sorted_boxes[j]
            iou = calculate_iou(box_i, box_j)
            
            if iou >= iou_thresh:
                class_i = sorted_classes[i]
                class_j = sorted_classes[j]
                
                # Check if one class is the parent of the other
                if lca.find_parent(class_i) == class_j:
                    selected_indices[j] = -1
                elif lca.find_parent(class_j) == class_i:
                    selected_indices[i] = -1
                else:
                   # Compare confidence scores for same class
                    if class_i == class_j:
                        selected_indices[j] = -1
    
    # Return the selected boxes and their corresponding scores and classes
    selected_indices = np.where(selected_indices==1)[0]
    selected_boxes = [sorted_boxes[i] for i in selected_indices]
    selected_scores = [sorted_scores[i] for i in selected_indices]
    selected_classes = [sorted_classes[i] for i in selected_indices]
    
    return selected_boxes, selected_scores, selected_classes

def calculate_iou(box1, box2):
    def box_area(box):
        return (box[2] - box[0]) * (box[3] - box[1])

    area_a = box_area(box1)
    area_b = box_area(box2)

    top_left = np.maximum(box1[:2], box2[:2])
    bottom_right = np.minimum(box1[2:], box2[2:])


    area_inter = np.prod(
    	np.clip(bottom_right - top_left, a_min=0, a_max=None))
        
    return area_inter / (area_a + area_b - area_inter)
    

if __name__ == "__main__":
    lca = BinaryLCA("asset/hierarchy.txt")
    bounding_boxes = [[0, 0, 100, 100], [0, 0, 90, 90], [0, 0, 80, 80], [0, 0, 10, 10]]
    confidence_scores = [0.9, 0.8, 0.7, 0.6]
    class_labels = ["n02118333", "n02119477", "n02119477", "n02119789"]
    score_threshold = 0.5
    iou_threshold = 0.5
    selected_boxes, selected_scores, selected_classes = nms_with_class_hierarchy(bounding_boxes, confidence_scores,
                                                                                 class_labels, lca,
                                                                                 score_threshold, iou_threshold)
    
    print(selected_boxes)
    print(selected_scores)
    print(selected_classes)