import React from "react";
import Button from "./ui/Button";
import Input from "./ui/Input";
import Select from "./ui/Select";
import { useNavigate } from "react-router-dom";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const signupSchema = z
  .object({
    clinicName: z.string().min(1, "Clinic name is required"),
    email: z.string().email("Invalid email address"),
    phone: z.string().min(10, "Phone number must be at least 10 digits"),
    website: z.string().optional(),
    country: z.string().min(1, "Country is required"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirmPassword: z.string().min(8, "Confirm password is required"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

const countryOptions = [
  { value: "Ghana", label: "Ghana" },
  { value: "Nigeria", label: "Nigeria" },
  { value: "Kenya", label: "Kenya" },
  { value: "South Africa", label: "South Africa" },
  { value: "Uganda", label: "Uganda" },
  { value: "Tanzania", label: "Tanzania" },
  { value: "Zimbabwe", label: "Zimbabwe" },
  { value: "Rwanda", label: "Rwanda" },
  { value: "Cameroon", label: "Cameroon" },
  { value: "Senegal", label: "Senegal" },
  { value: "United States", label: "United States" },
  { value: "Canada", label: "Canada" },
  { value: "United Kingdom", label: "United Kingdom" },
  { value: "Australia", label: "Australia" },
  { value: "Germany", label: "Germany" },
  { value: "France", label: "France" },
  { value: "Japan", label: "Japan" },
  { value: "Brazil", label: "Brazil" },
  { value: "India", label: "India" },
];

const Signup = () => {
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      clinicName: "",
      email: "",
      phone: "",
      website: "",
      country: "",
      password: "",
      confirmPassword: "",
    },
    mode: "onBlur",
  });

  const onSubmit = (data) => {
    console.log("Signing up with:", data);
  };

  return (
    <div className="flex w-full bg-white">
      <form onSubmit={handleSubmit(onSubmit)} className="rounded-lg w-full">
        <h2 className="text-3xl font-bold text-center mb-2 text-gray-800">
          Sign Up
        </h2>
        <p className="text-sm text-center text-gray-600 mb-6">
          Fill the form to get registered
        </p>

        <Input
          label="Clinic Name"
          placeholder="Enter Clinic Name"
          required
          error={errors.clinicName?.message}
          {...register("clinicName")}
        />

        <Input
          label="Clinic Email Address"
          type="email"
          placeholder="Enter Clinic Email"
          required
          error={errors.email?.message}
          {...register("email")}
        />

        <Input
          label="Clinic Phone Number"
          type="tel"
          placeholder="Enter Clinic Phone Number"
          required
          error={errors.phone?.message}
          {...register("phone")}
        />

        <Input
          label="Clinic Website"
          type="url"
          placeholder="Enter Clinic Website"
          error={errors.website?.message}
          {...register("website")}
        />

        <Controller
          name="country"
          control={control}
          render={({ field }) => (
            <Select
              label="Country"
              required
              placeholder="Select Country"
              options={countryOptions}
              error={errors.country?.message}
              value={field.value}
              onValueChange={field.onChange}
            />
          )}
        />

        <Input
          label="Password"
          type="password"
          placeholder="Enter your email password"
          required
          showPasswordToggle
          error={errors.password?.message}
          {...register("password")}
        />

        <Input
          label="Confirm Password"
          type="password"
          placeholder="Re-enter your password"
          required
          showPasswordToggle
          error={errors.confirmPassword?.message}
          {...register("confirmPassword")}
        />

        <Button type="submit" className="w-full mb-2 min-h-10 py-4 mt-2">
          Create Account
        </Button>

        <div className="text-center mt-1">
          <span className="text-xs text-gray-600">
            Already have an account?
          </span>
          <button
            type="button"
            onClick={() => navigate("/login")}
            className="text-xs ml-1 text-primary py-4 font-semibold hover:underline"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  );
};

export default Signup;
