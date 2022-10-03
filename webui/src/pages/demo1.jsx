import React, { useEffect, useState } from 'react'
import '../App.css';
import MCRenderContainer from '../components/mcrender_visialization';
import MedicalNoteDisplay from '../components/medical_note_display';
import { Grid } from "@mui/material"
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
// /Straighten

function Demo1() {
    const [medicalNoteId, setMedicalNoteId] = useState("fdf0813f-6d23-43d3-82fc-948bd9cc2bb4");
    const [medicalNote, setMedicalNote] = useState();

    const handleMedicalNoteChange = (event) => {
        setMedicalNoteId(event.target.value);
    };

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
        loadMedicalNote(medicalNoteId);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [medicalNoteId]);

    return (
        <Grid container className="MCRenderDemo1" justifyContent="center">
            <Grid item xs={12} >

                <Box sx={{ minWidth: 120 }}>
                    <br />
                    <FormControl >
                        <InputLabel id="inputSelectMedicalNote">Select Medical Note</InputLabel>
                        <Select
                            labelId="demo-simple-select-label"
                            id="medicalNodeSelectionId"
                            value={medicalNoteId}
                            label="Select Medical Note"
                            onChange={handleMedicalNoteChange}
                        >
                            <MenuItem value='fdf0813f-6d23-43d3-82fc-948bd9cc2bb4'>OB/GYN, pregnancy ER issue</MenuItem>
                            <MenuItem value="6bb29d28-c05f-46c1-8d90-ec7fe4d0145f">OB/GYN, pregnancy ultrasound scan</MenuItem>

                        </Select>
                    </FormControl>
                </Box>
            </Grid>
            {medicalNote && (
                <React.Fragment>
                    <Grid item xs={12}>
                        <h4>{medicalNote.medical_specialty}: &nbsp;&nbsp; {medicalNote.description}</h4>

                        <Stack direction="row" spacing={1} justifyContent="center">
                            {medicalNote.keywords && medicalNote.keywords.split(",").map(keyword => {
                                if (keyword && keyword.trim().length > 0) {
                                    return <Chip label={keyword} key={keyword} variant="outlined" />
                                } else {
                                    return null;
                                }

                            })}
                        </Stack>
                        <br />
                    </Grid>
                    <Grid item xs={12}>
                        <Grid container justifyContent="center" spacing={3}>
                            <Grid item xs={5}>
                                <MedicalNoteDisplay medicalNote={medicalNote} />
                            </Grid>
                            <Divider orientation="vertical" flexItem>

                            </Divider>
                            <Grid item xs={6}>
                                <MCRenderContainer medicalNote={medicalNote} />
                            </Grid>
                        </Grid>
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
