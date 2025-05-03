import React from "react";
import { Route, Routes } from "react-router-dom";
import AuthLayout from "./components/Layout/AuthLayout";
import Button from "./components/ui/Button";
import EmailConfirmation from "./pages/EmailConfirmation";

const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<Button>Home</Button>} />
          <Route path="features" element={<div>Features</div>} />
          <Route path="how-it-works" element={<div>How It Works</div>} />
          <Route path="contact-us" element={<div>Contact Us</div>} />
          <Route path="/email-confirmation" element={<EmailConfirmation />} />
        </Route>
      </Routes>
    </div>
  );
};

export default App;
