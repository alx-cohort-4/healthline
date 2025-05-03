import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import HeroSection from "./components/landing-page/HeroSection";
import AuthLayout from "./components/Layout/AuthLayout";
import EmailConfirmation from "./components/auth/EmailConfirmation";

const App = () => {
  return (
    <div className="min-h-screen">
      <Routes>
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<div>Signup Page</div>} />
          <Route path="/login" element={<div>Login Page</div>} />
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
