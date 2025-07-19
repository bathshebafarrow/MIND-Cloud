"""
Author: Bathsheba Jackson
Date Created: 2025-07-18
"""
from crud.crud_repo import retrieve_repositories
from models.repo import Repository, Study
from sqlalchemy.orm import Session


def prefill_repos(db: Session):
    """
    Prefill repository information in database table.

    Parameters
    ----------
    db: Session
        The database session used to insert data.
    """
    repos = [
        Repository(id=1, 
                   bucket_name='openneuro.org', 
                   display_name='OpenNeuro', 
                   description=""
                   )
    ]
    db.add_all(repos)
    db.commit()

def prefill_studies(db: Session):
    """
    Prefill study information in database table.

    Parameters
    ----------
    db: Session
        The database session used to insert data.
    """
    studies = [
        Study(study_id='ds002034',
              repository_id=1,
              description='ds002034: Real-time EEG feedback on alpha power lateralization leads to behavioral improvements in a covert attention task'
              ),
        Study(study_id='ds002721',
              repository_id=1,
              description='ds002721: An EEG dataset recorded during affective music listening'
              ),
        Study(study_id='ds003061',
              repository_id=1,
              description='ds003061: EEG data from an auditory oddball task'
              ),
        Study(study_id='ds003523',
              repository_id=1,
              description='ds003523: EEG: Visual Working Memory in Acute TBI'
              ),
        Study(study_id='ds003555',
              repository_id=1,
              description='ds003555: Dataset of EEG recordings containing HFO markings for 30 pediatric patients with epilepsy'
              ),
        Study(study_id='ds003638',
              repository_id=1,
              description='ds003638: EEG: Electrophysiological biomarkers of behavioral dimensions from cross-species paradigms'
              ),
        Study(study_id='ds003690',
              repository_id=1,
              description='ds003690: EEG, ECG and pupil data from young and older adults: rest and auditory cued reaction time tasks'
              ),
        Study(study_id='ds003768',
              repository_id=1,
              description='ds003768: Simultaneous EEG and fMRI signals during sleep from humans'
              ),
        Study(study_id='ds003775',
              repository_id=1,
              description='ds003775: SRM Resting-state EEG'
              ),
        Study(study_id='ds004040',
              repository_id=1,
              description='ds004040: Trance channeling EEG study'
              ),
        Study(study_id='ds004067',
              repository_id=1,
              description='ds004067: Moral conviction and metacognitive ability shape multiple stages of information processing'
              ),
        Study(study_id='ds004148',
              repository_id=1,
              description='ds004148: A test-retest resting and cognitive state EEG dataset'
              ),
        Study(study_id='ds004348',
              repository_id=1,
              description='ds004348: Ear-EEG Sleep Monitoring 2017 (EESM17)'
              ),
        Study(study_id='ds004504',
              repository_id=1,
              description='ds004504: A dataset of EEG recordings from: Alzheimer\'s disease, Frontotemporal dementia and Healthy subjects'
              )
    ]
    db.add_all(studies)
    db.commit()

def prefill_data(db: Session):
    """
    Prefill data in database tables. Load from JSON files if necessary.

    Parameters
    ----------
    db: Session
        The database session used to insert data.
    """
    if len(retrieve_repositories(db)) == 0:
        try:
            prefill_repos(db)
            prefill_studies(db)
        except Exception as ex:
            print(ex)
            db.rollback()
