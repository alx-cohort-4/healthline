import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import EmailConfirmation from "./components/auth/EmailConfirmation";
import AuthLayout from "./components/Layout/AuthLayout";
import LandingPage from "./pages/LandingPage";
import HardworkingSection from "./components/landing-page/HardworkingSection";
import Testimonials from "./components/landing-page/TestimonialSection";
const App = () => {
  return (
    <div className="min-h-screen">
      <Routes>
        {/* Public Routes */}
        <Route path="/testimonials" element={<Testimonials />} />
        <Route path="/home" element={<LandingPage />} />
        <Route path="/features" element={<div>Features Page</div>} />
        <Route path="/hardworking" element={<HardworkingSection />} />
        <Route path="/email-confirmation" element={<EmailConfirmation />} />

        {/* Auth Routes under shared layout */}
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<Navigate to="/login" replace />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="signup" element={<SignupPage />} />
        </Route>
      </Routes>
    </div>
  );
};

export default App;
