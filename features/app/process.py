"""
Process EEG data
"""
import mne
import numpy as np
import os
import pandas as pd
import matplotlib
import yasa
from scipy import stats, signal

matplotlib.use('Agg')
mne.set_log_level(verbose=None, return_old_level=False)
mne.set_log_level('ERROR')

bands=[(1, 4, 'Delta'), (4, 8, 'Theta'), (8, 12, 'Alpha'), (12, 30, 'Beta'), (30, 70, 'Gamma')]

def perform_extraction(task_id, subject_id, params):
    """
    Performs feature extraction from the processed data.
    task_id (string): the unique identifier assigned to the file processing request.
    subject_id (string): the subject number formatted according to BIDS.
    params (json): user parameter selections stored as a json string.
    """
    file_dir = f'tmp/{task_id}/results/{subject_id}/'
    for file_name in os.listdir(file_dir):
        file_parts = os.path.splitext(file_name)
        if file_parts[1] == '.fif':
            data = mne.io.read_raw_fif(f'{file_dir}{file_name}', preload=True)
            extract_features(data, params, file_parts[0], file_dir)

def extract_features(data, params, filename, file_dir):
    """
        Performs feature extraction from the processed data.
        data (Raw): the unique identifier assigned to the file processing request.
        subject_id (string): the subject number formatted according to BIDS.
        filename (string): The name of the file being processed.
        file_dir (string): The directory any files produced should be stored in.
    """
    sf = data.info["sfreq"]
    window = 4 * sf
    chan = data.ch_names
    data_uv = data.get_data(units="uV")

    features_dict = {}
    features_dict['channels'] = chan
    features_dict['mean'] = np.mean(data_uv, axis=-1)
    features_dict['std'] = np.std(data_uv,axis=-1)
    features_dict['ptp'] = np.ptp(data_uv,axis=-1)
    features_dict['var'] = np.var(data_uv,axis=-1)
    features_dict['minim'] = np.min(data_uv,axis=-1)
    features_dict['maxim'] = np.max(data_uv,axis=-1)
    features_dict['argminim'] = np.argmin(data_uv,axis=-1)
    features_dict['argmaxim'] = np.argmax(data_uv,axis=-1)
    features_dict['mean_square'] = np.mean(data_uv**2,axis=-1)
    features_dict['rms'] = np.sqrt(np.mean(data_uv**2,axis=-1))  
    features_dict['abs_diffs_signal'] = np.sum(np.abs(np.diff(data_uv,axis=-1)),axis=-1)
    features_dict['skewness'] = stats.skew(data_uv,axis=-1)
    features_dict['kurtosis'] = stats.kurtosis(data_uv,axis=-1)
    pd.DataFrame.from_dict(features_dict).to_csv(f'{file_dir}{filename}_time_domain.csv', index=False, header=True)

    freqs, psd = signal.welch(data_uv, sf, nperseg=window, average='median')
    
    relative_power = yasa.bandpower_from_psd(psd, freqs, ch_names=chan)
    relative_power.to_csv(f'{file_dir}{filename}_relative_power.csv', index=False, mode='w+')
    
    absolute_power = yasa.bandpower_from_psd(psd, freqs, ch_names=chan, bands=bands, relative=False)
    absolute_power.to_csv(f'{file_dir}{filename}_absolute_power.csv', index=False, mode='w+')

    # EEG spindle (sleep) is a burst of brain activity 
    spindles = yasa.spindles_detect(data_uv, sf)
    if spindles is not None:
        spindles.summary().to_csv(f'{file_dir}{filename}_spindles.csv', index=False, mode='w+')

    events, event_dict = mne.events_from_annotations(data)
    if len(events) != 0:
        try: 
            epochs = mne.Epochs(data, events, event_id=event_dict, preload=True)
            epochs.plot(block=True).savefig(f'{file_dir}{filename}_epochs_plot.png')
            averages = []
            for event in event_dict.keys():
                if event != 'New Segment/':
                    averages.append(epochs[event].average())
            mne.combine_evoked(averages, weights='equal').plot_joint(title='Combined Evoked').savefig(f'{file_dir}{filename}_avg_plot.png')
        except Exception:
            print(f'Could not process epochs for {filename}')
