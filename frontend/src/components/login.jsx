import React, { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import Button from "../components/ui/Button";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Logging in with:", formData);
    // Add actual authentication logic here
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <div className="flex w-full bg-white px-4">
      <form onSubmit={handleSubmit} className="bg-white rounded-lg  w-full ">
        <h2 className="text-3xl font-bold text-center mb-2 text-gray-800">
          Login
        </h2>
        <p className="text-sm text-center text-gray-600 mb-6">
          Enter your email and password to login
        </p>

        <div className="mb-4">
          <p className="text-sm text-gray-600 mb-1">
            Email<span className="text-red-500">*</span>
          </p>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email address"
            className="text-sm w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
        </div>

        <div className="mb-2 relative">
          <p className="text-sm text-gray-600 mb-1">
            Password<span className="text-red-500">*</span>
          </p>
          <input
            type={showPassword ? "text" : "password"}
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            className="text-sm w-full p-3 pr-10 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
            required
          />
          <span
            onClick={togglePasswordVisibility}
            className="absolute right-3 top-10 transform -translate-y-1/2 cursor-pointer text-gray-500 mt-3"
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </span>
        </div>

        <div className="flex justify-end mb-2">
          <button
            type="button"
            onClick={() => navigate("/forgot-password")}
            className="text-xs text-blue-600 hover:underline"
          >
            Forgot password?
          </button>
        </div>

        <Button type="submit" className="w-full mb-2 py-4 mt-2">
          Login
        </Button>

        <div className="text-center mt-1">
          <span className="text-xs text-gray-600">Don't have an account?</span>
          <button
            type="button"
            onClick={() => navigate("/signup")}
            className="text-xs ml-1 text-blue-600 font-semibold hover:underline"
          >
            Sign Up
          </button>
        </div>
      </form>
    </div>
  );
};

export default Login;
