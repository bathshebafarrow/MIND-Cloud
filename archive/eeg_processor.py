"""
Used to run code locally instead of in AWS.
"""
import argparse
import logging
import os
import time
import warnings
import logging
from preprocess import preprocess_subject_data
from process import perform_extraction

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__) 
logger.propagate = False
logging.basicConfig(filename='application.log', level=logging.ERROR)

def process_file_dir(file_dir, user_data):
    for filename in os.listdir(file_dir):
        file_ext = os.path.splitext(os.path.basename(filename))[1]
        if file_ext in ['.vhdr', '.bdf', '.edf', '.set']:
            process_file(f'{file_dir}/{filename}', user_data)

def process_file(filename, user_data):
    """
    Process the user data.
    user_data (json): user parameter selections in JSON format.
    """
    out_dir = f'results/{os.path.splitext(os.path.basename(filename))[0]}/'
    os.makedirs(out_dir, exist_ok=True)
    print(f'Results are saved to {os.path.abspath(out_dir)}')
    try:
        if preprocess_subject_data(filename, out_dir, user_data):
            perform_extraction(out_dir, user_data)
            return True
        else:
            return False 
    except Exception as ex:
        print("Could not complete processing for file %s: %s", filename, ex)
        return False

def get_user_data(args):
    user_data = {}
    if args.montage:
        user_data['montage'] = args.montage
    if args.highpass:
        user_data['highpass'] = args.highpass
    if args.lowpass:
        user_data['lowpass'] = args.lowpass
    if args.downsample:
        user_data['downsample'] = args.downsample
    return user_data

if __name__=="__main__":
    # Usage python eeg_processor.py tmp/names.txt
    parser = argparse.ArgumentParser(prog='EEG Data Preprocessor',
                    description='Used to removed unwanted artifacts from EEG data')
    parser.add_argument('filename')
    parser.add_argument('--montage', dest='montage', type=str, help='Montage file type')
    parser.add_argument('--highpass', dest='highpass', type=float, help='High pass filter threshold')
    parser.add_argument('--lowpass', dest='lowpass', type=float, help='Low pass filter threshold')
    parser.add_argument('--downsample', dest='downsample', type=float, help='Downsample frequency')
    args = parser.parse_args()

    start = time.time()
    path_name = args.filename
    print(f'Processing {path_name}')
    if os.path.isdir(path_name):
        process_file_dir(path_name, get_user_data(args))
    else:
        process_file(path_name, get_user_data(args))
    end = time.time()
    print(f'Processing completed in {end-start} sec')
