import { MdEmail } from "react-icons/md";
import { Link } from "react-router-dom";
import Nav from "../shared/Nav";
import { useSearchParams } from "react-router-dom";
import { useEffect } from "react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { verifyUser } from "../../api/auth";
// import useMe from "../../store/useMe";
import { CheckCircle, XCircle, Loader2 } from "lucide-react";

export default function EmailVerify() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const email = searchParams.get("email") || "your email";
  const [error, setError] = useState(null);
  const [status, setStatus] = useState("verifying");

  useEffect(() => {
    if (token) {
      const verify = async () => {
        try {
          await verifyUser(token);
          setStatus("success");
          setTimeout(() => navigate("/login"), 3000);
        } catch (error) {
          setError(error.message || "Verification failed");
          setStatus("error");
        }
      };
      verify();
    } else {
      setError("No verification token found");
      setStatus("error");
    }
  }, [token, navigate]);

  const renderContent = () => {
    switch (status) {
      case "verifying":
        return (
          <div className="text-center">
            <div className="relative mx-auto w-24 h-24 mb-8">
              <div className="absolute inset-0 bg-primary/10 rounded-full animate-ping" />
              <div className="relative flex items-center justify-center w-full h-full bg-primary/20 rounded-full">
                <MdEmail className="h-12 w-12 text-primary" />
              </div>
            </div>
            <h2 className="text-2xl font-semibold mb-4">
              Verifying Your Email
            </h2>
            <div className="space-y-2">
              <p className="text-gray-600">
                We're confirming your email address:
              </p>
              <p className="text-primary font-medium">{email}</p>
              <p className="text-sm text-gray-500">This won't take long...</p>
            </div>
          </div>
        );
      case "success":
        return (
          <div className="text-center">
            <div className="relative mx-auto w-24 h-24 mb-8">
              <div className="absolute inset-0 bg-green-100 rounded-full" />
              <div className="relative flex items-center justify-center w-full h-full">
                <CheckCircle className="h-16 w-16 text-green-500" />
              </div>
            </div>
            <h2 className="text-2xl font-semibold mb-4">Welcome Aboard</h2>
            <div className="space-y-4">
              <p className="text-gray-600">
                Your email has been verified successfully.
              </p>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-green-700">
                  Redirecting you to the Dashboard in a moment...
                </p>
              </div>
            </div>
          </div>
        );
      case "error":
        return (
          <div className="text-center">
            <div className="relative mx-auto w-24 h-24 mb-8">
              <div className="absolute inset-0 bg-red-100 rounded-full" />
              <div className="relative flex items-center justify-center w-full h-full">
                <XCircle className="h-16 w-16 text-red-500" />
              </div>
            </div>
            <h2 className="text-2xl font-semibold mb-4">Verification Failed</h2>
            <div className="space-y-4">
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-sm text-red-700">{error}</p>
              </div>
              <Link
                to="/signup"
                className="inline-flex items-center justify-center px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors w-full md:w-auto"
              >
                Back to Signup
              </Link>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Nav />
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-lg">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}
