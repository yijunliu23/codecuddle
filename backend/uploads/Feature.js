import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import './Feature.css';
import 'semantic-ui-css/semantic.min.css';
import { Form, TextArea, Button, Checkbox, Loader } from 'semantic-ui-react';

export function Feature () {
    // Optional: State management for form inputs
    const [formData, setFormData] = useState({
        pageAbout: '',
        goal: '',
        functionality: '',
        layoutDesc: ''
    });
    const initialFeatures = [
      
    ];

    const [features, setFeatures] = useState(initialFeatures);

    const handleChange = (event) => {
        setFormData({ ...formData, [event.target.name]: event.target.value });
    };

    const [selectedFeature, setSelectedFeature] = useState(null);

    const [isGenerated, setIsGenerated] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);


    const handleCheckboxChange = (index) => {
        setSelectedFeature(index);
    };
    const handleSubmit = async (event) => {
        event.preventDefault();
        setIsGenerating(true); // Set generating state to true

        try {
            const response = await fetch('/submit-form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            const responseData = await response.json();

            if (Array.isArray(responseData.features)) {
                setFeatures(responseData.features);
            } else {
                console.error('Expected an array for features, received:', responseData.features);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setIsGenerating(false); // Reset generating state
            setIsGenerated(true);  // Set generated state to true
        }
    };

    const navigate = useNavigate(); // Initialize useNavigate

    const handleNext = () => {
        if (selectedFeature === null) {
            alert('Please select a feature before proceeding.');
            return;
        }

        // Navigate to the next page with the selected feature data
        navigate('/webpage', { state: { selectedFeature: features[selectedFeature] } });
    };
    

    return (

        <section className='feature'>
            <section className='form'>
            <Form onSubmit={handleSubmit}>
                <Form.Field>
                    <label htmlFor="pageAbout">What's your website about?</label>
                    <TextArea 
                        id="pageAbout" 
                        name="pageAbout" 
                        onChange={handleChange} 
                        value={formData.pageAbout} 
                        required
                        placeholder="The website is a scheduling app.." />
                </Form.Field>
                <Form.Field>
                    <label htmlFor="goal">What's the main goal for this website?</label>
                    <TextArea 
                        id="goal" 
                        name="goal" 
                        onChange={handleChange} 
                        value={formData.goal} 
                        placeholder="The main goal is to find a common avaliable time for all users..." />
                </Form.Field>
                <Form.Field>
                    <label htmlFor="functionality">What are the key functionalities?</label>
                    <TextArea 
                        id="functionality" 
                        name="functionality" 
                        onChange={handleChange} 
                        value={formData.functionality} 
                        required
                        placeholder="1. Input names and select a time 2. Find commonly avaliable time 3...." />
                </Form.Field>
                <Button type="submit">{isGenerated ? 'Regenerate' : 'Generate'}</Button>
                
                {isGenerating && <Loader active inline='centered' className='generating'>Generating, please wait...</Loader>}
            </Form>

            </section>
            

            {isGenerated && (
                <section className="features">
                <h2>Features</h2>
                    <Form>
                        {features.map((feature, index) => (
                            <Form.Field key={index}>
                                <Checkbox
                                className='feature_list'
                                    radio
                                    label={<label><strong>{feature.feature}:</strong> {feature.description}</label>}
                                    name='checkboxRadioGroup'
                                    value={index}
                                    checked={selectedFeature === index}
                                    onChange={() => handleCheckboxChange(index)}
                                />
                            </Form.Field>
                        ))}
                        <Button onClick={handleNext} className='next_feature'>Next</Button>
                    </Form>
                </section>
                )}
            
        </section>


        
    );
}

export default Feature;
