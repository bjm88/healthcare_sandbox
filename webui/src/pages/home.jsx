
import React from "react";
import { Grid } from "@mui/material"

function Home() {
    return (
        <Grid containerclassName="HomeLinks">
            <Grid item lg={10} xm={10} >
                <div className="HomeContentHeader">
                    <p>A visualization engine for NLP entity extractions to help clinicians quickly rampup on a patient's situation.</p>
                </div>
            </Grid>
            <Grid item lg={10} xm={10} >
                <a href="/demo1">Demo 1:  Maternity</a>
            </Grid>
            <Grid item lg={10} xm={10} >
                <a href="/demo1">Demo 2:  Emergency Room</a>
            </Grid>
            <Grid item lg={10} xm={10} >
                <a href="/demo1">Demo 3:  Discharge to Home Care</a>
            </Grid>
        </Grid>
    );
}

export default Home;
