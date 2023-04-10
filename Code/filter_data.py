import os
from mne.io import read_raw_eeglab
import warnings; warnings.filterwarnings(action='ignore') # ignore warning for eeglab -----> yup
from utils import filter_signal
import numpy as np
import mne
import sys # for supressing the stdout
import time

path = input('Enter the full path for the hardrive where the "mouse_eeg" folder is: ')
today = round(time.time())
os.chdir(path)
sessions = {1:'BL',2:'SR1',3:'SR2',4:'SR3',5:'SR4',6:'SR5',7:'R1',8:'R2',9:'R3'}


def load_filter_export(subid,sessid,time):
    SAMPLING_RATE = 500'
    path = path + f'/data_BIDS/sub-0{subid}/ses-0{sessid}/eeg/fixed/'
    file = f'sub-0{subid}-{sessions[sessid]}_screew_fixed_{time}-{time+1}'

    raw = read_raw_eeglab(path +'hours/' + file + '.set', preload=True)
    eeg_data = raw.get_data().T

    acc = eeg_data[:,2].reshape(-1,1)
    sd = 13 # number of standard deviation away from the mean
    idx = filter_signal(acc, num_std=sd, padding_before_noise=2*SAMPLING_RATE, padding_after_noise=2*SAMPLING_RATE, max_or_sum=True, abs_or_pow=True)
    mask = np.ones(eeg_data.shape[0], dtype=bool)
    mask[idx] = False
    data = eeg_data[mask,:].T  # 4 channels, m time points
    info = mne.create_info(['Frontal','Parietal','Acceleration','Event'][:eeg_data.shape[1]], sfreq=500, ch_types='eeg')
    # create a RawArray object from the NumPy array and MNE Info object
    raw = mne.io.RawArray(data, info)
    try:
        os.mkdir(path + f'filtered_{today}')
    except FileExistsError:
        print('Folder already exists')

    export_path = path + f'/filtered_{today}/' + file + '_filtered.fdt'
    mne.export.export_raw(export_path,raw,'EEGLAB', overwrite=True)
    # Signal to Noise Ratio
    return data.shape[1]/eeg_data.shape[0]


if __name__ == "__main__":
    cnt = 0
    for subid in range(1,10):
        subject_log = np.zeros((9,24))
        for sessid in range(1,10):
            for t in range(24):
                # Save the original stdout stream
                original_stdout = sys.stdout

                # Redirect stdout to the null device
                sys.stdout = open(os.devnull, 'w')

                # Load, filter, export
                subject_log[sessid-1,t]= load_filter_export(subid,sessid,t)
                
                # Restore the original stdout stream
                sys.stdout = original_stdout
                cnt+=1
                
                print(f'{cnt} / {9*9*24} session is filtered')
        # save the log as a csv file
        np.savetxt(f'logs/subjectlog_{today}_{subid}.csv', subject_log, delimiter=',')
    print('Done!')
