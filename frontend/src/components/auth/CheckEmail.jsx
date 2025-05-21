import { Section } from 'lucide-react'
import React from 'react'
import Button from '../ui/Button'
import { Link } from "react-router-dom";
import { FaArrowLeft } from 'react-icons/fa';

const CheckEmail = () => {
  return (
    <section className='flex h-full'>
        <div className='lg:w-[656px] my-auto'>
            <h2 className="text-2xl sm:text-3xl font-bold text-center mb-2 text-gray-800">
        Check your email
      </h2>
      <p className="text-center text-grey-500 mb-6 sm:mb-6 max-w-xl mx-auto text-base sm:text-lg w-[350px]">
        We sent you a password reset link to name@gmail.com
      </p>
      <Button className="w-full mb-2 h-[48px] py-4 text-base/[24px] font-semibold">
        Open email App
        </Button>

        <p className="text-sm text-gray-500 mt-6 text-center">
          Didn’t receive the email? <Link to="/support" className="text-blue-600 hover:underline">
            Click to resend
          </Link>
        </p>
        <p className='text-center mt-6 text-blue-600 '>
        <FaArrowLeft className='inline-block mr-3' /><Link to="/login" className="hover:underline">
          Back to Login
          </Link>
        </p>
        </div>
    </section>
  )
}

export default CheckEmail