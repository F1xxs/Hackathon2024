import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import About from "./About";
import Header from "./Header";
import Contact from "./Contact";
import WebAPI from "./webAPI";
import Collaboration from "./Collaboration";
import Main from "./main";
import Backend from "./backend";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/webAPI" element={<webAPI />} />
                <Route path="/collaboration" element={<Collaboration />} />
                <Route path="/backend" element={<Backend />} />
            </Routes>
        </Router>
    );
}

export default App;
