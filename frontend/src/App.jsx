import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DashboardPage from "./pages/DashboardPage";
import ComparePage from "./pages/ComparePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/compare" element={<ComparePage />} />
        <Route
          path="/dashboard/:platform/:handle"
          element={<DashboardPage />}
        />
      </Routes>
    </Router>
  );
}

export default App;