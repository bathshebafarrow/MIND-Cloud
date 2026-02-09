import React, { useState, useEffect } from 'react';

function ViewJobsTable() {
    const [jobs, setJobs] = useState([]);

    function getJobs() {
        fetch('http://localhost:8000/job')
            .then(response => response.json())
            .then(data => setJobs(data))
            .catch(err => console.error('Error retrieving jobs:', err));
    };

    useEffect(() => {
        getJobs();
    }, []);
    return (
        <div>
            <h3>Under Construction....</h3>
            <table border="1" cellPadding="10">
                <thead>
                <tr>
                    <th>Created By</th>
                    <th>Created At</th>
                    <th>Source DB</th>
                    <th>Study ID</th>
                    <th>Total Subjects</th>	
                    <th>Total Processed</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {jobs.map(job => (
                    <tr key={job.id}>
                        <td>{job.username}</td>
                        <td>{job.created_at}</td>
                        <td>{job.source_db}</td>
                        <td>{job.study_id}</td>
                        <td>{job.subjects}</td>
                        <td>{job.total_processed}</td>
                        <td>{job.status}</td>
                        <td>&nbsp;</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default ViewJobsTable;