"""
Research code - use mne and pyprep libraries to process EEG data
"""
import matplotlib
import matplotlib.pyplot as plt
import mne
import numpy as np
import os
from config import settings
from mne.io import Raw
from mne.utils import logger
from models import Job
from pyprep.prep_pipeline import PrepPipeline
from typing import Any

matplotlib.use('Agg')
mne.set_log_level(verbose=None, return_old_level=False)
mne.set_log_level('WARNING')

def preprocess_subject(job: Job, input_dir: str) -> None:
    """
    Processes the subject's EEG data files as referenced in the job.

    job (Job): 
        Contains details of the job (study processing request).
    input_dir (str):
        The path to the files to be processed.
    """
    logger.info(f'Preprocessing {job.subject_id} for job {job.id}')
    output_dir = f'{input_dir}/results/'
    os.makedirs(output_dir, exist_ok=True)
    
    raw = None
    # For each EEG file in the directory, read in using MNE
    for file_name in os.listdir(input_dir):
        filename_parts = os.path.splitext(file_name)
        file_name = filename_parts[0]
        file_extension = filename_parts[1]
        
        # Load data into an instance of mne.io.Raw based on file extension
        in_file = f'{input_dir}/{file_name}'
        if file_extension == '.vhdr':
            raw_data = mne.io.read_raw_brainvision(in_file, preload=True)
        elif file_extension == '.bdf':
            raw_data = mne.io.read_raw_bdf(in_file, preload=True)
        elif file_extension == '.edf':
            raw_data = mne.io.read_raw_edf(in_file, preload=True)
        elif file_extension == '.set':
            raw_data = mne.io.read_raw_eeglab(in_file, preload=True)
        else:
            continue

        montage = create_montage(job, raw_data)
        processed_data = preprocess_data_with_prep(raw, montage, job.parameters)
        if processed_data is not None:
            processed_data.save(f'{output_dir}{file_name}_clean_eeg.fif', overwrite=True)
            plt.close('all')
            del processed_data
        del raw_data

def preprocess_data_with_prep(raw_data: Raw, montage, parameters: dict):
    """ 
    Perform preprocessing of raw EEG signal data using the PREP pipeline. Simplified
    processing follows; can become complex

    Parameters
    ----------
    raw_data (Raw):
        The raw EEG signal data.
    parameters (dict):
        Parameters submitted by the user

    Returns
    -------
        Raw : the preprocessed EEG data as a mne.io.Raw object
    """
    high_pass, low_pass, resample = 1.0, 45.0, 500
    if 'highpass' in parameters:
        high_pass = float(parameters.get('highpass'))
    if 'lowpass' in parameters:
        low_pass = float(parameters.get('lowpass'))
    if 'downsample' in parameters:
        resample = float(parameters.get('downsample'))
    
    raw_copy = raw_data.copy()
    
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
    prep = PrepPipeline(raw_copy, prep_params, montage, ransac=False)
    prep.fit()

    # raw_eeg contains processed data if fit() method has been called
    return prep.raw_eeg 


def create_montage(job: Job, raw_data: Raw) -> Any:
    """
    Use montage specified in the user parameters

    Parameters
    ----------
    job (Job):
        The job to be processed.
    raw_data (Raw):
        The raw EEG data.
    """
    montage_name = settings.DEFAULT_MONTAGE
    if 'montage' in job.parameters:
        user_montage = job.parameters.get('montage')
        if user_montage is not None:
            montage_name = user_montage

    drop_channels = []
    montage = mne.channels.make_standard_montage(montage_name)
    m_channels = montage.ch_names
    for c in raw_data.ch_names:
        if c not in m_channels:
            drop_channels.append(c)
    logger.info(f'Dropping channels {drop_channels}')
    raw_data.drop_channels(drop_channels)

    raw_data.pick_types(meg=False, eeg=True, eog=False)
    raw_data.set_montage(montage_name, on_missing='ignore')
    return montage


def create_raw_plots(raw_data, file_prefix: str, output_dir: str):
    """
    Create visualizations from raw data files.
    """
    raw_data.plot().savefig(f'{output_dir}{file_prefix}_raw_plot.png')


def create_processed_data_plots(processed_data, file_prefix: str, output_dir: str):
    """
    Creates visualization for processed data.
    """
    processed_data.plot().savefig(f'{output_dir}{file_prefix}_clean_plot.png')
    processed_data.plot_psd_topomap(normalize=True).savefig(f'{output_dir}{file_prefix}_psd_plot.png')
