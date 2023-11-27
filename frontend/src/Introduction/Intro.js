import './Intro.css';
import 'semantic-ui-css/semantic.min.css'; // Import Semantic UI CSS
import { Button } from 'semantic-ui-react'; // Import the Button component

export function Intro () {
   

    return (

        <section className='intro'>
            <h3>Welcome to <span className="char-color-1">C</span><span className="char-color-2">o</span><span className="char-color-3">d</span><span className="char-color-1">e</span><span className="char-color-2">C</span><span className="char-color-3">u</span><span className="char-color-1">d</span><span className="char-color-2">d</span><span className="char-color-3">l</span><span className="char-color-1">e</span></h3>
            <h4>Empowering Inclusivity in Web Design</h4>
            <p>In the digital age, inclusivity isn't just a value; it's a necessity. At CodeCuddle, we understand this and have created a revolutionary tool that transforms your webpages into bastions of inclusivity and accessibility.</p>

            <section className='intro_desc'>
            <h4>How It Works:</h4>
            <li>📝 <b>Share Your Webpage Details</b>: Begin by providing essential information about your existing webpage.</li>
            <li>🌈 <b>Explore Inclusive Features</b>: Our AI will suggest a range of inclusive features tailored to enhance your webpage's accessibility and user-friendliness.</li>
            <li>📤 <b>Upload Your File</b>: Simply upload your webpage's JSX file. Our tool seamlessly integrates the selected inclusive features into your design.</li>
            <li>📥 <b>Download and Deploy</b>: Receive an enhanced, inclusivity-focused JSX file, ready for deployment. Elevate your website's accessibility and appeal with just a few clicks.</li>

            </section>
            
            <Button className="custom-button" href="./feature">Get Started</Button>
        </section>
        
    );
}

export default Intro;
