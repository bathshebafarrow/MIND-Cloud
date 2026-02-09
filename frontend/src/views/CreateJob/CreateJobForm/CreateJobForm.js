import React, { useState } from 'react';

function CreateJobForm() {
    const [formData, setFormData] = useState({
      user_name: '',
      source_db: '',
    });

    const db_sources = [
        { value: '', label: '-- Select the Source DB --' },
        { value: 'openneuro', label: 'OpenNeuro' }
    ];
  
    const [submitted, setSubmitted] = useState(false);

    // Handle input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
        ...prevData,
        [name]: value
        }));
    };

    // Handle form submission
    const handleSubmit = (e) => {
      e.preventDefault();
      console.log('Form submitted:', formData);
      setSubmitted(true);
    };
  
    return (
      <div style={{ padding: '20px', maxWidth: '400px', margin: 'auto' }}>
        <h3>Under Construction....</h3>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '10px' }}>
            <label>User Name:</label><br />
            <input
              type="text"
              name="name"
              value={formData.user_name}
              required
              style={{ width: '100%', padding: '8px' }}
            />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label>Data Repo:</label><br />
            <select name="source_db"
                value={formData.source_db}
                onChange={handleChange}
                required
                style={{ width: '100%', padding: '8px' }}
            >
                {db_sources.map(data_source => (
                    <option key={data_source.value} value={data_source.value}>{data_source.label}</option>
                ))}
            </select>
          </div>

          <button type="submit" style={{ padding: '10px 20px' }}>Submit</button>
        </form>
  
        {submitted && (
          <div style={{ marginTop: '20px', color: 'green' }}>
            <strong>The job was successfully submitted processing.</strong>
          </div>
        )}
      </div>
    );
  }
  
  export default CreateJobForm;