import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const ResumeUpload = () => {
    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [recommendation, setRecommendation] = useState('');

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
            // Update the recommendation state with the response data
            setRecommendation(response.data.analysis_results.recommendations[0]);
        } catch (error) {
            console.error('There was an error uploading the file!', error);
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="mb-4">Resume Upload</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Upload Resume:</label>
                    <input type="file" className="form-control" onChange={handleFileChange} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Job Description:</label>
                    <textarea className="form-control" rows="5" value={jobDescription} onChange={handleJobDescriptionChange} />
                </div>
                <button type="submit" className="btn btn-primary">Upload</button>
            </form>
            {recommendation && (
                <div className="mt-4">
                    <h3>Recommendation:</h3>
                    <p>{recommendation}</p>
                </div>
            )}
        </div>
    );
};

export default ResumeUpload;
