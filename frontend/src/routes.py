"""
Basic routes for processing and viewing EEG data files.
"""
import forms
import os
import task_manager
import application as app
import json
from application import application
from flask import request, render_template, redirect, Response, url_for, flash, jsonify


@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html')

@application.route('/results')
def results():
    taskId = request.args.get('taskid')
    file_name = f'{taskId}/eeg_processed_data.zip'
    # User to download file
    s3 = app.get_s3_client()
    file = s3.get_object(Bucket='eeg-data-clean', Key=file_name)
    return Response(
        file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": f'attachment;filename={os.path.basename(file_name)}'}
    )

@application.route('/viewtasks')
def view_tasks():
    tasks = task_manager.retreive_all_tasks()
    return render_template('viewtasks.html', data=tasks)

@application.route('/deleteTask')
def delete_tasks():
    task_id = request.args.get('taskid')
    task_manager.delete_task(task_id)
    return redirect(url_for('view_tasks'))

@application.route('/update_status', methods=['GET', 'POST'])
def update_task_status(id):
    content = request.json
    task_id = content['task_id']
    status = content['status']
    task_manager.update_task_status(task_id, status)
    return {
        'statusCode': 200,
        'body': json.dumps('Task completed')
    }

@application.route('/processfile', methods=['GET', 'POST'])
def process_file():
    form = forms.ProcessFileForm()
    
    if form.validate_on_submit():
        bucket = request.form.get('bucket')
        study = request.form.get('study')
        subjects = request.form.getlist('subjects')
        usr = request.form.get('user_name')
        params = request.form.to_dict(flat=True)
        del params['csrf_token']
        del params['submit']
        del params['subjects']
        task_manager.create_task(usr, bucket, study, subjects, params)
        
        flash('Subject(s) from study ' + study + 
              ' in ' + bucket + ' submitted for processing')
        form.bucket.data = ''
        form.study.choices = []
        form.subjects.choices = []
    return render_template('processfile.html', form=form)


@application.route('/study/<bucket_id>')
def study_by_bucket(bucket_id):
    # Query from a database instead of hard-coded lists if time permits
    studies = get_study_choices(bucket_id)
    return jsonify({'studies': studies})

def get_study_choices(bucket_id):
    if bucket_id == 'nirdslab-eeg':
        return forms.nl_choices
    elif bucket_id == 'openneuro.org':
        return forms.on_choices
    return []

@application.route('/subjects/<study_id>/<bucket>')
def subjects_for_study(study_id, bucket):
    subjects = task_manager.get_subject_list(bucket, study_id)
    return jsonify({'subjects': subjects})
        
def valid_subject(subject_id):
    values = subject_id.replace(" ", "").split('-')
    if len(values) == 1 and values[0].isdigit():
        return True
    elif len(values) == 2:
        if values[0].isdigit() and values[1].isdigit():
            if int(values[0]) < int(values[1]):
                return True
    return False