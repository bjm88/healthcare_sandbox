import React, { useEffect, useState } from 'react'
import '../App.css';
import MCRenderContainer from '../components/mcrender_visialization';
import { Grid } from "@mui/material"

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
        <Grid container className="MCRenderDemo1">
            {medicalNote && (
                <React.Fragment>
                    <Grid item>
                        <h3>{medicalNote.medical_specialty}</h3>
                        <h3>{medicalNote.description}</h3>
                        <p>{medicalNote.transcription}</p>
                    </Grid>
                    <Grid item>
                        <MCRenderContainer medicalNote={medicalNote} />
                    </Grid>
                </React.Fragment>
            )}
            {!medicalNote && (
                <Grid item>
                    <p>Please select a medical note.</p>
                </Grid>
            )}
        </Grid>
    );
}

export default Demo1;
