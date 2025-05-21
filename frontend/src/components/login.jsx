import React from "react";
import Button from "./ui/Button";
import Input from "./ui/Input";
import {
  //  useNavigate,
  Link,
} from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

const Login = () => {
  // const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
    mode: "onBlur",
  });

  const onSubmit = (data) => {
    console.log("Logging in with:", data);
  };

  return (
    <div className="flex w-full h-fit max-md:w-full bg-white ">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="bg-white rounded-lg w-full"
      >
        <h2 className="text-3xl font-bold text-center mb-2 text-gray-800">
          Login
        </h2>
        <p className="text-sm text-center text-gray-600 mb-6">
          Enter your email and password to login
        </p>

        <Input
          label="Email"
          type="email"
          placeholder="Enter your email address"
          required
          error={errors.email?.message}
          {...register("email")}
        />

        <Input
          label="Password"
          type="password"
          placeholder="Enter your password"
          required
          showPasswordToggle
          error={errors.password?.message}
          {...register("password")}
        />

        <div className="flex justify-end mb-2">
          <Link
            to="/forgot-password"
            className="text-xs cursor-pointer text-primary hover:underline"
          >
            Forgot password?
          </Link>
        </div>

        <Button type="submit" className="w-full mb-2 h-[48px] py-4 mt-2">
          Login
        </Button>

        <div className="text-center mt-1">
          <span className="text-xs text-gray-600">Don't have an account?</span>
          <Link
            to="/signup"
            className="text-xs ml-1 cursor-pointer text-primary font-semibold hover:underline"
          >
            Sign Up
          </Link>
        </div>
      </form>
    </div>
  );
};

export default Login;
