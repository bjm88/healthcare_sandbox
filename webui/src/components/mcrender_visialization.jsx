import React, { useRef, useEffect, useState } from 'react'
import * as Muicon from "@mui/icons-material";
import '../App.css';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import { Typography } from '@mui/material';
const images = require.context('../images', true); 

//const images = require.context('../images', true);  //import pregnancy_t1 from '../images/pregnancy_t1.png'
//  future, look to do full 3D rendering using three.js
//import * as THREE from 'three'; // causes warning of duplicate imports of three.js
//import * as THREE from "https://unpkg.com/three@0.125.1/build/three.module.js";
// import { OrbitControls } from "https://unpkg.com/three@0.125.1/examples/jsm/controls/OrbitControls.js";

function MCRenderContainer(props) {
    const medicalNote = props.medicalNote;
    const refContainer = useRef();
    // eslint-disable-next-line 
    const { current: container } = refContainer;

    const [baseImg, setBaseImg] = useState(null);
    const [overlays, setOverlays] = useState([]);
    useEffect(() => {
        setOverlays([])
        if (medicalNote) {
            if (medicalNote.derived_data && medicalNote.derived_data.base_image) {
                var img = images(`./${medicalNote.derived_data.base_image}.png`)  //.default not needed
                setBaseImg(img);
                if (medicalNote.derived_data.base_image.startsWith('pregnancy')) {
                    calcOverlaysPregnancy();
                } 
            }
            
        };
        // eslint-disable-next-line
    }, [medicalNote]); //, [renderer, setRenderer]

    // TODO make much more dynamic over time, move to backend to calc helpers and consumer friendly text
    const calcOverlaysPregnancy = () => {
        if (medicalNote && medicalNote.entity_extraction) {
            var overlaysArray = []

            //common pregnancy issues
            for (var e of medicalNote.entity_extraction) {
                if (e.Category === "MEDICAL_CONDITION" && e.Type === "DX_NAME") {
                    if (e.Text === "abdominal pain") {
                        overlaysArray.push({ "icon": "Warning", bot: 115, left: 225, text: e.Text, color:'#f44336' })
                    }
                }
                if (e.Category === "MEDICAL_CONDITION" && e.Type === "DX_NAME") {
                    if (e.Text === "hemostatic") {
                        if (e.Attributes && e.Attributes[0]["Type"] === "SYSTEM_ORGAN_SITE") {
                            if (e.Attributes[0]["Text"] === "fallopian tube") {
                                overlaysArray.push({ "icon": "Bloodtype", bot: 30, left: 205, text: "fallopian tube bleeding", color:'#f44336' })
                            }
                        }
                    }
                }
                if (e.Category === "MEDICAL_CONDITION" && e.Type === "DX_NAME") {
                    if (e.Text === "Tachycardia") {
                        overlaysArray.push({ "icon": "MonitorHeart", bot: 510, left: 160, text: e.Text + ": Hearrate > 100", color:'#f44336' })
                    }
                }
                // pregnancy vitals
                if (e.Category === "TEST_TREATMENT_PROCEDURE" && e.Text === "heart rate" && e.Type==="TEST_NAME") {
                    if (e.Attributes && e.Attributes[0]["Type"] === "TEST_VALUE") {
                        overlaysArray.push({ "icon": "MonitorHeart", bot: 165, left: 125, text: e.Attributes[0]["Text"], color:'#f44336' })
                    }
                }
            }

            //pregnancy measurements
            if (medicalNote.derived_data["pregnancyMeasurements"]){
                overlaysArray.push({ "icon": "Straighten", bot: 55, left: 175, text: "BPD (biparietal head diameter) " + medicalNote.derived_data["pregnancyMeasurements"]["BPD"] + " - " + "HC (head circumference) " + medicalNote.derived_data["pregnancyMeasurements"]["HC"] + "cm", color:'black' })
                overlaysArray.push({ "icon": "Straighten", bot: 155, left: 80, text: "AC (abdominal circumference) " + medicalNote.derived_data["pregnancyMeasurements"]["AC"]+ "cm", color:'black' })
                overlaysArray.push({ "icon": "Straighten", bot: 215, left: 75, text: "Femur Length (FL) " + medicalNote.derived_data["pregnancyMeasurements"]["FL"]+ "cm", color:'black' })
            }

            setOverlays(overlaysArray);
        }
    }
    return (
        <div className="MCRenderContainer" >
            {baseImg && (
                <div className="App-imgContainer" ref={refContainer}>
                    <img className="App-baseimg" src={baseImg} alt="Medical Render"/>
                    {overlays && overlays.map((overlay, index) => {
                        const Icon = Muicon[overlay.icon] //allows to dynamically get MUI v5 icons
                        
                        return (
                            <Tooltip  title={<Typography fontSize={22}>{overlay.text}</Typography>}  arrow className="App-img0verlay" sx={{  position: 'absolute', bottom: overlay.bot, left: overlay.left }}>
                                <IconButton><Icon sx={{ color: overlay.color, fontSize: 40 }} ></Icon></IconButton>
                            </Tooltip>
                        )
                    })}
                </div>
            )}
        </div>
    );

}

export default MCRenderContainer;
