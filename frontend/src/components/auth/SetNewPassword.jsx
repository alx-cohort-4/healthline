import React, { useState } from "react";
import { RiEyeLine, RiEyeOffLine, RiArrowLeftLine } from "react-icons/ri";

// Reusable Password Input Component
const PasswordInput = ({
  id,
  label,
  value,
  onChange,
  placeholder = "*****************",
  helperText = "Must be at least 8 characters",
}) => {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="flex flex-col gap-1 w-full min-h-[92px]">
      {/* Label */}
      <label
        htmlFor={id}
        className="text-[#1A1A1A] font-bricolage font-medium text-base sm:text-lg md:text-xl"
      >
        {label} <span className="text-red-500">*</span>
      </label>

      {/* Input Wrapper */}
      <div className="relative">
        <input
          id={id}
          type={showPassword ? "text" : "password"}
          required
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className="w-full min-h-[48px] px-4 pr-10 font-bricolage text-base sm:text-lg text-[#1A1A1A] border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-[#1A1A1A]"
        />

        {/* Toggle Visibility Icon */}
        <span
          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 cursor-pointer"
          onClick={() => setShowPassword((prev) => !prev)}
          aria-label={showPassword ? "Hide password" : "Show password"}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") setShowPassword((prev) => !prev);
          }}
        >
          {showPassword ? <RiEyeOffLine size={20} /> : <RiEyeLine size={20} />}
        </span>
      </div>

      {/* Helper Text */}
      <p className="text-[#333333] font-bricolage font-normal text-sm sm:text-base">
        {helperText}
      </p>
    </div>
  );
};

// Main Component
const SetNewPassword = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    console.log("Password successfully reset:", newPassword);
    // Add API call or further logic here
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4 py-6">
      <div className="container max-w-lg mx-auto">
        {/* Heading */}
        <h1 className="font-bricolage font-semibold text-xl sm:text-2xl md:text-3xl text-center text-[#1A1A1A]">
          Set new password
        </h1>

        {/* Instruction */}
        <p className="mt-3 font-bricolage font-medium text-sm sm:text-base md:text-lg text-center text-[#333333] tracking-wide leading-relaxed">
          Your new password must be different from your previous password.
        </p>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-col gap-6 mt-6 w-full px-4 sm:px-6"
        >
          <PasswordInput
            id="newPassword"
            label="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />

          <PasswordInput
            id="confirmPassword"
            label="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            helperText="Password must match"
          />

          <button
            type="submit"
            className="h-12 w-full font-bricolage font-semibold text-white text-base bg-[#175CD3] rounded hover:bg-blue-700 transition"
          >
            Reset your Password
          </button>

          {/* Back to Login Link */}
          <div className="mt-2 flex justify-center items-center">
            <a
              href="/login" // or use React Router's <Link> component
              className="flex items-center gap-2 text-[#175CD3] font-bricolage font-medium text-base leading-6 tracking-wide hover:underline"
            >
              <RiArrowLeftLine size={16} className="mt-[4px]" />
              Back to Login
            </a>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SetNewPassword;

