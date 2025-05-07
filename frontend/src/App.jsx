import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import EmailConfirmation from "./components/auth/EmailConfirmation";
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
        <Route path="/email-confirmation" element={<EmailConfirmation />} />
        <Route path="/features" element={<div>Features Page</div>} />
      </Routes>
    </div>
  );
};

export default App;
