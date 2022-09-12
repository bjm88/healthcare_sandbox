import React, { useEffect, useState } from 'react'
import logo from '../mcrenderlogoCropped.png';
import '../App.css';
import MCRenderContainer from '../components/mcrender_visialization';

function Demo1() {
    const [medicalNote, setMedicalNote] = useState(true);

    const loadMedicalNote = async (medNoteId) => {
        if (!medNoteId) {
            return;
        }

        const apiHost = "http://healthsandboxc-api-dev.healthsandbox.org:5001";
        try {
            const resp = await fetch(`${apiHost}/api/medical_notes/load?mn_id=${medNoteId}`);
            if (resp.status !== 200) {
                console.log("failed to load medical note");
                return;
            }
            const json = await resp.json();
            if (json && json["data"]) {
                setMedicalNote(json["data"]);
            }
        } catch (error) {
            console.log("Could not load medical note, error" + error);
            return
        }

    };
    useEffect(() => {
        const md_id_maternity_ultrasound_ob = "8daefb13-ea72-4985-aa99-25cb90bc0ba0"
        loadMedicalNote(md_id_maternity_ultrasound_ob);

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

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

                {medicalNote && (
                    <div>
                        <h3>{medicalNote.medical_specialty}</h3>
                        <h3>{medicalNote.description}</h3>
                        <p>{medicalNote.transcription}</p>
                        <MCRenderContainer medicalNote={medicalNote} />
                    </div>
                   
                )}
                {!medicalNote && (
                    <p>Please select a medical note.</p>
                )}
            </header>
            <br/>
            
        </div>
    );
}

export default Demo1;
