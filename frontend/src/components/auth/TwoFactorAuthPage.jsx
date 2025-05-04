import React, { useRef, useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import Button from '../ui/Button';

const otpSchema = z.object({
  otp: z
    .array(z.string().regex(/^\d$/, 'Each field must be a digit'))
    .length(6, 'OTP must be 6 digits'),
});

const TwoFactorAuthPage = ({ onVerify, onBackToLogin, onResendOtp }) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
    setValue,
    getValues,
  } = useForm({
    resolver: zodResolver(otpSchema),
    defaultValues: {
      otp: Array(6).fill(''),
    },
  });

  const inputRefs = useRef([]);
  const [resendCooldown, setResendCooldown] = useState(0);

  const handleChange = (value, index) => {
    if (/^\d$/.test(value)) {
      setValue(`otp.${index}`, value);
      if (index < 5) {
        inputRefs.current[index + 1]?.focus();
      }
    } else if (value === '') {
      setValue(`otp.${index}`, '');
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === 'Backspace' && getValues(`otp.${index}`) === '' && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const onSubmit = ({ otp }) => {
    const joinedOtp = otp.join('');
    if (joinedOtp === '123456') {
      onVerify();
    } else {
      alert('Invalid OTP');
    }
  };

  const handleResend = () => {
    if (resendCooldown > 0) return;
    setResendCooldown(30);
    onResendOtp?.();
    const interval = setInterval(() => {
      setResendCooldown((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  return (
    <div className='flex min-h-[85vh] h-auto w-full ml-0  bg-white'>
    <div className=" mx-auto pt-40 pb-40 text-center ">
      <h2 className="text-4xl font-semibold mb-2">Two-Factor Authentication</h2>
      <p className="mb-6">Enter the 6-digit code sent to you to confirm your login</p>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="flex justify-center gap-2 mb-4">
          {Array(6).fill(0).map((_, index) => (
            <Controller
              key={index}
              name={`otp.${index}`}
              control={control}
              render={({ field }) => (
                <input
                  {...field}
                  ref={(el) => (inputRefs.current[index] = el)}
                  type="text"
                  inputMode="numeric"
                  maxLength={1}
                  className={`w-10 h-12 text-xl text-center border rounded focus:outline-none ${
                    errors.otp?.[index] ? 'border-red-500' : 'border-gray-300'
                  }`}
                  onChange={(e) => handleChange(e.target.value, index)}
                  onKeyDown={(e) => handleKeyDown(e, index)}
                />
              )}
            />
          ))}
        </div>
        {errors.otp && <p className="text-red-500 text-sm mb-2">{errors.otp.message}</p>}
        <Button className="w-full py-3 mt-2 mb-4">Confirm</Button>
      </form>

      <p className="mt-6">
        <button
          onClick={handleResend}
          disabled={resendCooldown > 0}
          className="text-blue-600 hover:underline disabled:text-gray-400 disabled:cursor-not-allowed"
        >
          Resend confirmation code {resendCooldown > 0 ? `(${resendCooldown}s)` : ''}
        </button>
      </p>

      <p className="mt-4 text-sm text-gray-600">
        Remembered password?{' '}
        <button
          onClick={onBackToLogin}
          className="text-blue-600 hover:underline"
        >
          Login
        </button>
      </p>
    </div>
    </div>
  );
};

export default TwoFactorAuthPage;
