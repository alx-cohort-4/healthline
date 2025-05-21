import { useState } from "react";
import { ArrowLeft } from "lucide-react";
import Button from "../ui/Button";
import Input from "../ui/Input";
import { useNavigate } from "react-router-dom";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const navigate = useNavigate();

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email.trim()) {
      setError("Email address is required");
      return;
    }

    if (!validateEmail(email)) {
      setError("Please enter a valid email address");
      return;
    }

    setError("");
    setIsSubmitting(true);

    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
    }, 1500);
  };

  return (
    <div className="flex md:mt-20 flex-col items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md bg-white p-8 rounded-lg ">
        {isSubmitted ? (
          <div className="text-center">
            <h1 className="text-2xl font-semibold text-gray-900 mb-2">
              Check your email
            </h1>
            <p className="text-gray-600 mb-6">
              We've sent password reset instructions to{" "}
              <span className="font-medium">{email}</span>
            </p>
            <Button onClick={() => setIsSubmitted(false)} fullWidth>
              Back to reset password
            </Button>
          </div>
        ) : (
          <>
            <div className="text-center mb-6">
              <h1 className="text-2xl font-semibold text-gray-900 mb-2">
                Forgot password?
              </h1>
              <p className="text-gray-600">
                Don't worry, we'll send you reset instructions.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <Input
                label="Email Address"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address"
                required
                error={error}
                autoFocus
              />

              <Button
                type="submit"
                className="w-full py-3"
                isLoading={isSubmitting}
              >
                Reset your password
              </Button>
            </form>
          </>
        )}

        <div className="mt-6 text-center">
          <a
            href="#"
            className="inline-flex items-center text-blue-600 hover:text-blue-800 transition-colors"
            onClick={(e) => {
              e.preventDefault();
              navigate("/login");
            }}
          >
            <ArrowLeft size={16} className="mr-1" />
            Back to Login
          </a>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
