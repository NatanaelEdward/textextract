// src/components/ImageUpload.js
import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = () => {
    const [file, setFile] = useState(null);
    const [extractedText, setExtractedText] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/imagetexts/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setExtractedText(response.data.extracted_text);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload</button>
            </form>
            {extractedText && (
                <div className="extracted-text">
                    <h2>Extracted Text:</h2>
                    <p>{extractedText}</p>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
