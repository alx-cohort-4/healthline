import { useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import AuthLayout from "./components/Layout/AuthLayout";
import LandingPage from "./pages/LandingPage";
import NotFoundPage from "./pages/NotFoundPage";
import { fetchCountries } from "./api/countries";
import useCountriesStore from "./store/useCountries";
import {
  CheckEmail,
  PasswordResetSuccess,
  TwoFactorAuthPage,
  EmailVerify,
  EmailConfirmation,
  ForgetPassword,
} from "./components/auth/index";

const App = () => {
  const setCountries = useCountriesStore((state) => state.setCountries);

  useEffect(() => {
    const loadCountries = async () => {
      try {
        const data = await fetchCountries();

        const preferredLayout = data.map((country) => {
          return {
            label: country.name.common,
            value: country.cca2,
            icon: country.flags?.svg || country.flags?.png,
          };
        });
        setCountries(preferredLayout);
      } catch (err) {
        console.error(
          err instanceof Error ? err.message : "Failed to fetch countries"
        );
      }
    };
    loadCountries();
  }, [setCountries]);

  return (
    <div className="min-h-screen">
      <Routes>
        <Route index element={<LandingPage />} />
        <Route path="/" element={<AuthLayout />}>
          <Route index element={<LoginPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="signup" element={<SignupPage />} />
          <Route path="otp" element={<TwoFactorAuthPage />} />
          <Route path="resetsuccess" element={<PasswordResetSuccess />} />
          <Route path="check" element={<CheckEmail />} />
          <Route path="forgot-password" element={<ForgetPassword />} />
        </Route>

        <Route path="/email-confirmation" element={<EmailConfirmation />} />
        <Route path="/verify-email" element={<EmailVerify />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  );
};

export default App;
