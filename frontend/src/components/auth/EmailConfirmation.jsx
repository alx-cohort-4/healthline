import { MdEmail } from "react-icons/md";
import { Link } from "react-router-dom";
import Nav from "../shared/Nav";
import { useLocation } from "react-router-dom";

export default function EmailConfirmation() {
  const location = useLocation();
  const { email } = location.state || {};
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4">
      <Nav />
      <div className="bg-white rounded-2xl shadow-md p-8 max-w-md w-full text-center">
        <div className="flex justify-center mb-4">
          <MdEmail
            className="text-[#175CD3]"
            style={{ width: "100px", height: "80px" }}
          />
        </div>

        <h1 className="text-2xl font-semibold text-gray-800 mb-4">
          Check Your Email For Confirmation
        </h1>

        <p className="text-gray-600 mb-2">Thank you for signing up!</p>

        <p className="text-sm text-gray-600 mb-6">
          A confirmation link has been sent to{" "}
          <span className="text-primary">{email}</span>. Please check your inbox
          and click the link to activate your account.
        </p>

        <a
          href="https://mail.google.com"
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:underline"
        >
          Go to your mailbox
        </a>

        <p className="text-sm text-gray-500 mt-6">
          Didn’t receive the email?{" "}
          <Link to="/support" className="text-blue-600 hover:underline">
            Resend confirmation email again
          </Link>
        </p>

        {/* Shorter Divider at the Bottom */}
        <div
          className="my-6 mx-auto border-t-2"
          style={{ width: "80%", borderColor: "#BCBDC3" }}
        ></div>

        <p className="text-[10px] text-gray-600">
          Didn’t receive the email? Check your spam folder or resend the
          confirmation link.
        </p>
      </div>
    </div>
  );
}
