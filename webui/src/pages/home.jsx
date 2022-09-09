import logo from '../mcrenderlogoCropped.png';
import '../App.css';
import React from "react";

function Home() {
    return (
        <div className="App">
            <header className="App-header">
                <p>
                    AWS hackathon demo of <span className="App-logo-mc">Medical Comprehend Render</span>.

                    <br />
                    <img src={logo} className="App-logo" alt="logo" />
                    <br />
                    <span className="App-logo-mc">MC</span><span>Render</span>
                </p>

                <p>A visualization engine for NLP entity extractions to help clinicians quickly rampup on a patient's situation.</p>
            </header>
        </div>
    );
}

export default Home;
