import React, { useRef, useEffect, useState } from 'react'
import * as Muicon from "@mui/icons-material";
import '../App.css';
import Tooltip from '@mui/material/Tooltip';
import pregnancy_t1 from '../images/pregnancy_t1.png'
import IconButton from '@mui/material/IconButton';
import { Typography } from '@mui/material';
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

        if (medicalNote) {
            if (medicalNote.derived_data && medicalNote.derived_data.base_image) {
                if (medicalNote.derived_data.base_image === 'pregnancy_t1') {
                    setBaseImg(pregnancy_t1);
                    calcOverlaysPregnancy();
                }
            }
            
        };
        // eslint-disable-next-line
    }, [baseImg, medicalNote]); //, [renderer, setRenderer]

    // TODO make much more dynamic over time, move to backend to calc helpers and consumer friendly text
    const calcOverlaysPregnancy = () => {
        if (medicalNote && medicalNote.entity_extraction) {
            var overlaysArray = []

            for (var e of medicalNote.entity_extraction) {
                if (e.Category === "MEDICAL_CONDITION" && e.Type === "DX_NAME") {
                    if (e.Text === "abdominal pain") {
                        overlaysArray.push({ "icon": "Warning", bot: 95, left: 255, text: e.Text, color:'#f44336' })
                    }
                }
                if (e.Category === "MEDICAL_CONDITION" && e.Type === "DX_NAME") {
                    if (e.Text === "hemostatic") {
                        if (e.Attributes && e.Attributes[0]["Type"] === "SYSTEM_ORGAN_SITE") {
                            if (e.Attributes[0]["Text"] === "fallopian tube") {
                                overlaysArray.push({ "icon": "Bloodtype", bot: 0, left: 205, text: "fallopian tube bleeding", color:'#f44336' })
                            }
                        }
                    }
                }
                if (e.Category === "MEDICAL_CONDITION" && e.Type === "DX_NAME") {
                    if (e.Text === "Tachycardia") {
                        overlaysArray.push({ "icon": "MonitorHeart", bot: 510, left: 160, text: e.Text + ": Hearrate > 100", color:'#f44336' })
                    }
                }

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
