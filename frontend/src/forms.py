import mne
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired

nl_choices = [{'id':'','name':'-- Select --'},{'id':'asd00002','name':'Autism Spectrum Disorder'}]
 
# Does not currently pull all studies from the S3 bucket; could do that in the future; TODO: add these to DynamoDB                
on_choices = [{'id':'','name':'-- Select --'},
              {'id':'ds002034','name':'ds002034: Real-time EEG feedback on alpha power lateralization leads to behavioral improvements in a covert attention task'},
              {'id':'ds002721','name':'ds002721: An EEG dataset recorded during affective music listening'},
              {'id':'ds003061','name':'ds003061: EEG data from an auditory oddball task'},
              {'id':'ds003523','name':'ds003523: EEG: Visual Working Memory in Acute TBI'},
              {'id':'ds003555','name':'ds003555: Dataset of EEG recordings containing HFO markings for 30 pediatric patients with epilepsy'},
              {'id':'ds003638','name':'ds003638: EEG: Electrophysiological biomarkers of behavioral dimensions from cross-species paradigms'},
              {'id':'ds003690','name':'ds003690: EEG, ECG and pupil data from young and older adults: rest and auditory cued reaction time tasks'},
              {'id':'ds003768','name':'ds003768: Simultaneous EEG and fMRI signals during sleep from humans'},
              {'id':'ds003775','name':'ds003775: SRM Resting-state EEG'},
              {'id':'ds004040','name':'ds004040: Trance channeling EEG study'},
              {'id':'ds004067','name':'ds004067: Moral conviction and metacognitive ability shape multiple stages of information processing'},
              {'id':'ds004148','name':'ds004148: A test-retest resting and cognitive state EEG dataset'},
              {'id':'ds004348','name':'ds004348: Ear-EEG Sleep Monitoring 2017 (EESM17)'},
              {'id':'ds004504','name':'ds004504: A dataset of EEG recordings from: Alzheimer\'s disease, Frontotemporal dementia and Healthy subjects'}]

class ProcessFileForm(FlaskForm):
    bucket = SelectField(u'S3 Bucket', 
                         choices=[('', '-- Select --'),('nirdslab-eeg', 'NirdsLab EEG'),('openneuro.org', 'Open Neuro')], 
                         default='')
    study = SelectField('Study', choices=[], validate_choice=False)
    subjects = SelectMultipleField('Subjects', choices=[], validate_choice=False)
    user_name = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Process')

    # Non-required parameters; more can be added as needed
    montage = SelectField("Montage",
                                 choices=[(m, m) for m in mne.channels.get_builtin_montages()],
                                 default="standard_1020")
    highpass = IntegerField('High Pass Filter (Hz)', default="1")
    lowpass = IntegerField('Low Pass Filter (Hz)', default="45")
    downsample = IntegerField('Downsample (Hz)', default="500")
    time_window = IntegerField('Time Window (s)', default="2")


