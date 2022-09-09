
import { Route, Routes, BrowserRouter } from "react-router-dom";
import Home from "./pages/home";
import Demo1 from "./pages/demo1";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/demo1" element={<Demo1 />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
