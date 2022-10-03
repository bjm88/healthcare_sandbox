
import { Route, Routes, BrowserRouter } from "react-router-dom";
import Home from "./pages/home";
import Demo1 from "./pages/demo1";
import { Grid } from "@mui/material";
import logo from './mcrenderlogoCropped.png';
import './App.css';

function App() {
  return (
    <Grid container spacing={0} className="App">
      <Grid item lg={12} xm={12} className="App-header">
        <Grid container spacing={0}>
          <Grid item lg={2} xm={2} className="HeaderLogoContainer">
            <img src={logo} className="App-logo" alt="logo" />
          </Grid>
          <Grid item lg={8} xm={8} className="HeaderWrods">
            AWS hackathon: <span className="App-logo-mc">Medical Comprehend Render</span>.
          </Grid>
        </Grid>
      </Grid>
      <Grid lg={12} item xs={12} className="App-body">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/demo1" element={<Demo1 />} />
          </Routes>
        </BrowserRouter>
      </Grid>
      <Grid lg={12} item>
        <br />
        <br />
      </Grid>
    </Grid>
  );
}

export default App;
