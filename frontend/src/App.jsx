import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import HeroSection from "./components/landing-page/HeroSection";
import LoginPage from "./pages/LoginPage";
import EmailConfirmation from "./components/auth/EmailConfirmation";
import AuthLayout from "./components/Layout/AuthLayout";

const App = () => {
  return (
    <div className="min-h-screen">
      <Routes>
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<div>Signup Page</div>} />
        </Route>
        <Route path="/email-confirmation" element={<EmailConfirmation />} />
        <Route path="/features" element={<div>Features Page</div>} />
        <Route path="/" element={<Navigate to="/hero" replace />} />
        <Route path="/hero" element={<HeroSection />} />
      </Routes>
    </div>
  );
};

export default App;
