import numpy as np

def filter_signal(quality_control,num_std,padding_before_noise=1,padding_after_noise=1,max_or_sum=True, abs_or_pow=True):
    '''If quality_control has abnormal values than those values and the region around it will be cut out.

    Parameters
    ----------
    quality_control:
        quality_control.shape = (number_of_samples,p) # p should not be 0
    num_std:
        The number of standard deviations away from the mean that will be treated as abnormal
    padding_before_noise:
        The number of samples before the abnormal value that will be cut out
    padding_after_noise:
        The number of samples after the abnormal value that will be cut out
    max_or_sum:
        Only relevant if quality_control has multiple dimensions.
        If True then the maximum of the quality_control along axis 1 will be used to calculate the mean and standard deviation.
        If False then the sum of the quality_control along axis 1 will be used to calculate the mean and standard deviation.
    abs_or_pow:
        If True then the absolute value of quality_control will be used to calculate the mean and standard deviation.
        If False then the square of quality_control will be used to calculate the mean and standard deviation.
    
    Returns
    -------
    idx:
        The indices of the samples that should be cut out
    '''
    # can decide what operations to use to preprocess quality_control
    if max_or_sum:
        f = lambda x: np.max(x,axis=1)
    else:
        f = lambda x: np.sum(x,axis=1)

    if abs_or_pow:
        g = lambda x: np.abs(x)
    else:
        g = lambda x: np.power(x,2)

    # if it has multiple dimension choose the maximum along them at each sample 
    quality_control = f(g(quality_control))

    # calculate the mean of quality_control:
    mean = np.mean(quality_control)

    # calculate the standard deviaton of quality_control
    std = np.std(quality_control)

    # if a point in signal is further away from the mean than 3 sd than add it to mask
    mask = (quality_control > mean+num_std*std) | (quality_control < mean-num_std*std)

    # get the inidices where mask is True
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return idx
    # remove indeces that are too close to the edge from idx to avoid edge effects
    idx = idx[(idx > padding_before_noise) & (idx < quality_control.shape[0]-padding_after_noise)]
    idx = np.concatenate([np.arange(i-padding_before_noise,i+padding_after_noise) for i in idx])
    
    return idx


def split_array(array, idx):
    '''
    Splits an array into segments where the indices are not present.
    Parameters
    ----------
    array:
        The array to be split
    idx:
        The indices of the samples that should be cut out
    
    Returns
    -------
    list
        A list of numpy.array()s that contain the signal segments that were not cut out.
    '''
    # sort the indices
    list_of_all_segments = np.split(array, idx)
    # if an element has a length of 1, it is a noise segment
    list_of_good_segments = [el for el in list_of_all_segments if len(el)>1]
    return list_of_good_segments