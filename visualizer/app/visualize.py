"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
import os
import mne
from mne.io import read_raw_brainvision, read_raw_bdf, read_raw_edf, read_raw_eeglab

def visualize(filename: str):
    filename_parts = os.path.splitext(os.path.basename(filename))
    file_extension = filename_parts[1]

    if file_extension == '.vhdr':
        raw = read_raw_brainvision(filename, preload=True)
    elif file_extension == '.bdf':
        raw = read_raw_bdf(filename, preload=True)
    elif file_extension == '.edf':
        raw = read_raw_edf(filename, preload=True)
    elif file_extension == '.set':
        raw = read_raw_eeglab(filename, preload=True)
    else:
        print(f"Not currently coded to read {file_extension}")
    print(mne.channels.get_builtin_montages())

    raw.pick_types(meg=False, eeg=True, eog=False)
    raw.set_montage('standard_1020')
    raw.plot().savefig(f'{filename_parts[0]}_raw_plot.png')
    raw.plot_sensors(show_names=True).savefig(f'{filename_parts[0]}_sensors.png')
    raw.plot_psd_topomap(normalize=True).savefig(f'{filename_parts[0]}_psd_plot.png')
    mne.viz.plot_layout("standard_1020")

    trans = mne.read_trans(filename)
