import numpy as np


def transform_mat_to_python_rois_func(ROI_matlab_object):
    # print(ROI_matlab_object)
    my_ROIs_list = []
    # print(f"the size and type of the ROI_matlab_object >>>{len(ROI_matlab_object)}<<<and >>>{type(ROI_matlab_object)}<<<")
    
    for roi in ROI_matlab_object:
        # print(f"the type of the roi >>>{type(roi)}<<<and>>>{roi}<<<")
        xmin = roi[0]
        ymin = roi[1]
        width = roi[2]
        height = roi[3]
        
        v1 = [xmin, ymin]
        v2 = [xmin, ymin + height]
        v3 = [xmin + width, ymin + height]
        v4 = [xmin + width, ymin]

        my_new_shape = np.array([v1, v2, v3, v4])
        my_new_shape = np.flip(my_new_shape, (1))
        my_ROIs_list.append(my_new_shape)
    
    return my_ROIs_list