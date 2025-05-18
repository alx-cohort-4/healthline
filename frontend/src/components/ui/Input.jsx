import React, { forwardRef } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import cn from "../../libs/cn";

const Input = forwardRef(
  (
    {
      label,
      type = "text",
      error,
      required,
      showPasswordToggle = false,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = React.useState(false);

    const togglePasswordVisibility = () => {
      setShowPassword((prev) => !prev);
    };

    const inputType = type === "password" && showPassword ? "text" : type;

    return (
      <div className="mb-4 w-auto">
        {label && (
          <p className="text-sm text-gray-600 mb-1">
            {label}
            {required && <span className="text-red-500">*</span>}
          </p>
        )}
        <div className="relative">
          <input
            type={inputType}
            ref={ref}
            className={cn(
              "text-sm w-full p-3 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400",
              error
                ? "border-red-500 bg-red-500/5 focus:ring-1 focus:ring-red-400"
                : "border-gray-300",
              type === "password" && "pr-10"
            )}
            {...props}
          />
          {type === "password" && showPasswordToggle && (
            <span
              onClick={togglePasswordVisibility}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer text-gray-500"
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </span>
          )}
        </div>
        {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
      </div>
    );
  }
);

Input.displayName = "Input";

export default Input;
