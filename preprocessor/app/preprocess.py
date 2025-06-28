"""
Research code - use mne and pyprep libraries to process EEG data
"""
import matplotlib
import matplotlib.pyplot as plt
import mne
import numpy as np
import os
from mne.utils import logger
from pyprep.prep_pipeline import PrepPipeline

matplotlib.use('Agg')
mne.set_log_level(verbose=None, return_old_level=False)
mne.set_log_level('WARNING')

def preprocess_subject_data(task_id, subject_id, user_params={}):
    raw = None
    logger.info(f'Preprocessing {subject_id} for task {task_id}')

    task_dir = f'tmp/{task_id}/{subject_id}/'
    # Create output directory
    out_dir = f'tmp/{task_id}/results/{subject_id}/'
    os.makedirs(out_dir, exist_ok=True)

    # For each EEG file in the directory, read in using MNE
    for file_name in os.listdir(task_dir):
        filename_parts = os.path.splitext(file_name)
        file_extension = filename_parts[1]
        # Load data into an instance of mne.io.Raw based on file extension
        in_file = f'{task_dir}/{file_name}'
        if file_extension == '.vhdr':
            raw = mne.io.read_raw_brainvision(in_file, preload=True)
        elif file_extension == '.bdf':
            raw = mne.io.read_raw_bdf(in_file, preload=True)
        elif file_extension == '.edf':
            raw = mne.io.read_raw_edf(in_file, preload=True)
        elif file_extension == '.set':
            raw = mne.io.read_raw_eeglab(in_file, preload=True)
        else:
            continue

        # Use montage specified in the user parameters
        montage = 'standard_1005'
        if 'montage' in user_params:
            user_montage = user_params.get('montage').get('S')
            if user_montage is not None:
                montage = user_montage

        # Drop montage channels if not found in the data set
        drop_channels = []
        m_channels = mne.channels.make_standard_montage(montage).ch_names
        for c in raw.ch_names:
            if c not in m_channels:
                drop_channels.append(c)
        logger.info(f'Dropping channels {drop_channels}')
        raw.drop_channels(drop_channels)

        raw.pick_types(meg=False, eeg=True, eog=False)
        raw.set_montage(montage, on_missing='ignore')

        # Process data and create a plot of the clean data
        processed_data = preprocess_data_with_prep(raw, montage, user_params)
        if processed_data is not None:
        
            # Create visualizations
            raw.plot().savefig(f'{out_dir}{filename_parts[0]}_raw_plot.png')
            del raw

            processed_data.plot().savefig(f'{out_dir}{filename_parts[0]}_clean_plot.png')
            processed_data.plot_psd_topomap(normalize=True).savefig(f'{out_dir}{filename_parts[0]}_psd_plot.png')

            # Save data to FIF file
            processed_data.save(f'{out_dir}{filename_parts[0]}_clean_eeg.fif', overwrite=True)
            plt.close('all')

            # Save data to CSV file
            df = processed_data.to_data_frame()
            df.to_csv(f'{out_dir}{filename_parts[0]}_clean_eeg.csv', index=False, mode='w+')
            del processed_data
            return True
        return False


def preprocess_data_with_prep(raw, montage_name, user_params):
    """ 
    Perform preprocessing of raw EEG signal data using the PREP pipeline. Simplified
    processing follows; can become complex

    Parameters:
        raw (Raw) : the raw EEG signal data.
        user_params (dict) : parameters submitted by the user

    Returns:
        Raw : the preprocessed EEG data as a mne.io.Raw object
    """
    # Logging some data
    logger.info(str(raw.info["sfreq"]) + ' original sampling frequency.')
    logger.info(str(raw.times[len(raw)-1]) + ' second recording')


    high_pass, low_pass, resample = 1.0, 45.0, 500
    if 'highpass' in user_params:
        high_pass = float(user_params.get('highpass').get('S'))
    if 'lowpass' in user_params:
        low_pass = float(user_params.get('lowpass').get('S'))
    if 'downsample' in user_params:
        resample = float(user_params.get('downsample').get('S'))
    
    raw_copy = raw.copy()
    
    # Alway filter first and apply filters to continuous, raw EEG data before any segmenting
    if high_pass is not None:
        if low_pass is None:
            # Remove low frequency baseline drift with a Hz high-pass filter 
            raw_copy = raw_copy.filter(high_pass, None, fir_design='firwin')
        else:
            # Use band pass filter (both low and high)
            raw_copy = raw_copy.filter(l_freq=high_pass, h_freq=low_pass, h_trans_bandwidth=0.1)
    elif low_pass is not None:
        raw_copy = raw_copy.filter(None, low_pass, fir_design='firwin')

    # The notch filter is used to remove power line noise
    if low_pass is None or low_pass > 59:
        raw_copy = raw_copy.notch_filter(np.arange(60, 241, 60), filter_length='auto')

    # resample to reduce computation time
    if raw_copy.info["sfreq"] > resample:
        raw_copy.resample(resample)
    
    prep_params = {
        "ref_chs": "eeg",
        "reref_chs": "eeg",
        "line_freqs": {}
    }

    # Python version of PREP pipeline; finds bad channels, interpolates, re-references
    montage = mne.channels.make_standard_montage(montage_name)
    prep = PrepPipeline(raw_copy, prep_params, montage, ransac=False)
    prep.fit()

    # raw_eeg contains processed data if fit() method has been called
    return prep.raw_eeg 

 
if __name__=="__main__":
    preprocess_subject_data('test212', '', {})