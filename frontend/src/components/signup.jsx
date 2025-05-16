import React from "react";
import Button from "./ui/Button";
import Input from "./ui/Input";
import Select from "./ui/Select";
import { useNavigate } from "react-router-dom";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import useCountriesStore from "../store/useCountries";
import "react-phone-number-input/style.css";
import PhoneInput, { isValidPhoneNumber } from "react-phone-number-input";
import { registerUser } from "../api/auth";

const signupSchema = z
  .object({
    clinic_name: z.string().min(1, "Clinic name is required"),
    clinic_email: z.string().email("Invalid clinic address"),
    phone: z.string().refine((value) => isValidPhoneNumber(value), {
      message: "Invalid phone number",
    }),
    address: z.string().optional(),
    website: z.string().optional(),
    country: z.string().min(1, "Country is required"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    re_enter_password: z.string().min(8, "Confirm password is required"),
  })
  .refine((data) => data.password === data.re_enter_password, {
    message: "Passwords do not match",
    path: ["re_enter_password"],
  });

const Signup = () => {
  const navigate = useNavigate();
  const countries = useCountriesStore((state) => state.countries);
  const {
    register,
    handleSubmit,
    isSubmitting,
    control,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      clinic_name: "",
      clinic_email: "",
      phone: "",
      website: "",
      address: "",
      country: "",
      password: "",
      re_enter_password: "",
    },
    mode: "onBlur",
  });

  const onSubmit = async (data) => {
    console.log("Signing up with:", data);
    try {
      const response = await registerUser(data);
      console.log("🚀 ~ onSubmit ~ response:", response);
    } catch (err) {
      console.error("Error signing up:", err);
    }
  };

  return (
    <div className="flex w-full ">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="rounded-lg space-y-4 w-full"
      >
        <h2 className="text-3xl font-bold text-center mb-2 text-gray-800">
          Sign Up
        </h2>
        <p className="text-sm text-center text-gray-600 mb-6">
          Enter the Details of your Healthcare Facility below to create an
          account
        </p>

        <Input
          label="Healthcare Faculty  Name"
          placeholder="Enter Healthcare Faculty  Name"
          required
          error={errors.clinic_name?.message}
          {...register("clinic_name")}
        />

        <Input
          label="Healthcare Faculty Email Address"
          type="clinic_email"
          placeholder="Enter Healthcare Faculty Email"
          required
          error={errors.clinic_email?.message}
          {...register("clinic_email")}
        />

        <Controller
          name="phone"
          control={control}
          render={({ field }) => (
            <div>
              <label className="text-sm text-gray-600 mb-1">
                Healthcare Faculty Phone Number
                <span className="text-red-500">*</span>
              </label>
              <PhoneInput
                {...field}
                international
                defaultCountry="GH"
                className="!w-full [&>.PhoneInputInput]:border-none [&>.PhoneInputInput]:outline-none [&>.PhoneInputInput]:bg-transparent [&>.PhoneInputInput]:focus:outline-none "
              />
              {errors.phone && (
                <p className="text-xs text-red-500 mt-1">
                  {errors.phone.message}
                </p>
              )}
            </div>
          )}
        />

        <Input
          label="Healthcare Faculty Website"
          // type="url"
          placeholder="Enter Healthcare Faculty Website"
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
              options={countries}
              error={errors.country?.message}
              value={field.value}
              onValueChange={field.onChange}
            />
          )}
        />

        <Input
          label="Enter Healthcare Faculty"
          type="address"
          // className="mt-4"
          placeholder="Enter your Address"
          required
          error={errors.address?.message}
          {...register("address")}
        />
        <Input
          label="Password"
          type="password"
          // className="mt-4"
          placeholder="Enter your clinic_email password"
          required
          showPasswordToggle
          error={errors.password?.message}
          {...register("password")}
        />

        <Input
          label="Confirm Password"
          type="password"
          placeholder="Confirm your password"
          required
          showPasswordToggle
          error={errors.re_enter_password?.message}
          {...register("re_enter_password")}
        />

        <Button
          disabled={isSubmitting}
          type="submit"
          className="w-full mb-2 min-h-10 py-4 mt-2"
        >
          {isSubmitting ? "Submitting..." : "Create Account"}
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
