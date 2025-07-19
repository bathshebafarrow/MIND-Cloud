"""
Author: Bathsheba Jackson
Date Created: 2025-07-18
"""
from fastapi import HTTPException
from schemas.repo import RepositoryInputModel, StudyInputModel
from models.repo import Repository, Study
from sqlalchemy.orm import Session


def create_repository(db: Session, repository: RepositoryInputModel) -> Repository:
    """
    Creates a new Repository record based on the input.

    Parameters
    ----------
    db: Session
        The database session.
    repository: RepositoryInputModel
        The validated repository data.

    Returns
    -------
    The new Repository record. 
    """
    try:
        new_repo = Repository(**repository.model_dump())
        db.add(new_repo)
        db.commit()
        db.refresh(new_repo)
        return new_repo
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail="Could not create a new Repository record: {ex}"
        )
    
def create_study(db: Session, study: StudyInputModel) -> Study:
    """
    Creates a new Study record based on the input.

    Parameters
    ----------
    db: Session
        The database session.
    study: StudyInputModel
        The validated study data.

    Returns
    -------
    The new Study record. 
    """
    try:
        new_study = Study(**study.model_dump())
        db.add(new_study)
        db.commit()
        db.refresh(new_study)
        return new_study
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail="Could not create a new Study record: {ex}"
        )
    
def retrieve_studies(db: Session) -> list[Study]:
    """
    Retrieve all Study records in the database.
    
    Parameters
    ----------
    db: Session
        The database session.

    Returns
    -------
    The list of Study records.
    """
    try:
        return db.query(Study).all()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while retrieving Study records: {ex}"
        )
    
def retrieve_repo_studies(db: Session, repo_id: int) -> list[Study]:
    """
    Retrieve all Study records associated with the specified repository.
    
    Parameters
    ----------
    db: Session
        The database session.
    repo_id: int
        The repository unique identifier.

    Returns
    -------
    The list of Study records associated with the specified repository.
    """
    try:
        return db.query(Study).where(Study.repository_id == repo_id).all()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while retrieve files: {ex}"
        )

def retrieve_repositories(db: Session) -> list[Repository]:
    """
    Retrieve all Repository records in the database.
    
    Parameters
    ----------
    db: Session
        The database session.

    Returns
    -------
    The list of Repository records.
    """
    try:
        return db.query(Repository).all()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred while retrieve Repository records: {ex}"
        )