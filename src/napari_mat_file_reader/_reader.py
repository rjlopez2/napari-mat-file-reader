"""
This module is an example of a barebones numpy reader plugin for napari.

It implements the Reader specification, but your plugin may choose to
implement multiple readers or even other plugin contributions. see:
https://napari.org/stable/plugins/guides.html?#readers
"""
import mat73
import scipy.io as sio
from .utils import *


def napari_get_reader(path):
    """A basic implementation of a Reader contribution.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # if we know we cannot read the file, we immediately return None.
    if not path.endswith(".mat"):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will
        default to layer_type=="image" if not provided
    """
    # # handle both a string and a list of strings
    # paths = [path] if isinstance(path, str) else path
    # # load all files into array
    # arrays = [np.load(_path) for _path in paths]
    # # stack arrays into single array
    # data = np.squeeze(np.stack(arrays))
    try:
        data_dict = mat73.loadmat(path)   
        # with mat73.loadmat(path) as data_dict: # this apporach is not working, no sure why
        #     data_dict = data_dict
    except:
        data_dict = sio.loadmat(path)
       


    data_names = ['RegisteredImage', 'stack', 'roi_positions', 'processed_data_int', 'data_int']
    data, metadata = extract_stack_array(data_dict = data_dict, stack_name_list=data_names)
    
    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {
        "colormap" : "turbo",
        "gamma" : 0.15,
        "metadata": metadata

    }

    layer_type = "image"  


    if 'roi_positions' in metadata:
        
        add_kwargs = {
             "edge_width":1,
             "metadata": metadata
             }
        layer_type = 'shapes'


    return [(data, add_kwargs, layer_type)]