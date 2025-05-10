import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import AuthLayout from "./components/Layout/AuthLayout";
import LandingPage from "./pages/LandingPage";

const App = () => {
  return (
    <div className="min-h-screen">
      <Routes>
        <Route path="/home" element={<LandingPage />} />
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<Navigate to="/" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
        </Route>
      </Routes>
    </div>
  );
};

export default App;
