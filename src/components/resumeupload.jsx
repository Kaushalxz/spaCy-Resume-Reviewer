import React, { useState } from 'react';
import axios from 'axios';

const ResumeUpload = () => {
    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleJobDescriptionChange = (e) => {
        setJobDescription(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);
        formData.append('job_description', jobDescription);

        try {
            const response = await axios.post('http://localhost:8000/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log('File uploaded successfully', response.data);
        } catch (error) {
            console.error('There was an error uploading the file!', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Upload Resume:</label>
                <br></br>
                <input type="file" onChange={handleFileChange} />
            </div>
            <div>
                <label>Job Description:</label>
                <br></br>
                <textarea value={jobDescription} onChange={handleJobDescriptionChange} />
            </div>
            <button type="submit">Upload</button>
        </form>
    );
};

export default ResumeUpload;
