import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Feature from './Feature/Feature';
import Intro from './Introduction/Intro';
import Webpage from './Webpage/Webpage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/feature" element={<Feature />} />
        <Route path="/webpage" element={<Webpage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
