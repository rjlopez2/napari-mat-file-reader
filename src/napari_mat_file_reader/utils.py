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

def extract_stack_array(data_dict, stack_name_list):
    """
    extract np.array data and metadata from the data dict returned by the mat73.loadmat function

    Parameters
    ----------
    data_dict : dict
        data dictionary obtained from the function mat73.loadmat.
    
    stack_name_list: list
        Key names accepted that contain the image array raw data.
    
    
    Returns
    -------
    data : np.ndarray
       Image array raw data.
    data : np.ndarray
    data_dict : metadata harvested from the original data_dic excluding the image raw data.

    """
    metadata = {}
    # special_names = ["roi_positions", "processed_data_int", "data_int"]
    # for name in stack_name_list:
    for key, value in data_dict.copy().items():
        
        ########## handeling the ROIS mat files ##########
        if key == 'roi_positions':
            shape_data = value
            data = transform_mat_to_python_rois_func(shape_data)
            # data_dict.pop(key, None)
            metadata.update(data_dict)
        
        ########## handeling the workspace mat files ##########
        if key == 'processed_data_int':
            data = value.get("image_stack")[0]
            data = np.swapaxes(data, 0, 2)
            data = np.swapaxes(data, 1,2)
        ### adding metadata ###
        if key == 'data_int':
            metadata.update(value)
            
        ########## handeling other mat files ##########
        if (key == 'RegisteredImage' ) | (key == "stack"):
            data = value
            data = data.transpose(2, 0, 1) # transpose the array so it looks the same orientation as in the matlab app
            # extract everything you want to add as metadata but the actual data
            data_dict.pop(key, None)
            if len(data_dict) != 0:
                metadata.update(data_dict)

            
    return (data, metadata)