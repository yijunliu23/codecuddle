import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import './Webpage.css';
import 'semantic-ui-css/semantic.min.css';
import { Button, Form, Input, Segment, Loader } from 'semantic-ui-react';


export function Webpage () {
    const location = useLocation();
    const selectedFeature = location.state?.selectedFeature;

    const [file, setFile] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleImprove = async (event) => {
        event.preventDefault();
        if (!file) {
            alert('Please upload a file before submitting.');
            return;
        }

        setIsGenerating(true);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('feature', JSON.stringify(selectedFeature));

        try {
            const response = await fetch('/improve-feature', {
                method: 'POST',
                body: formData,
            });
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', 'improved_feature.jsx');
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error('Error submitting file:', error);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <section className='webpage'>
            <section className='feature_selected'>
                <p><i>You have selected:</i></p>
                <p><strong>{selectedFeature?.feature || 'No feature selected'}:</strong> {selectedFeature?.description || 'No feature selected'}</p>
            </section>

            <Segment className='upload'>
                <p>Please upload your JSX file. The complete file will automatically be downloaded. The process might take a few minutes.</p>
                <Form>
                    <Form.Field>
                        <label htmlFor="myFile">JSX File Upload</label>
                        <Input className='input_jsx' type="file" onChange={handleFileChange} id="myFile" name="filename" accept=".jsx, .js" />
                    </Form.Field>
                    <Button onClick={handleImprove}>Improve</Button>
                </Form>
                {isGenerating && <Loader active inline='centered'>Generating, please wait...</Loader>}
            </Segment>
        </section>
    );
}

export default Webpage;
