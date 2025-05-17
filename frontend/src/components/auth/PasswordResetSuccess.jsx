import React from "react";
import Button from "../ui/Button";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";
const PasswordResetSuccess = () => {
return (
    <div className="w-full mt-40 text-center">
        <h2 className="text-2xl sm:text-3xl font-bold text-center mb-2 text-gray-800">Password reset successfully</h2>
        <p className="text-center max-w-xl mx-auto text-base sm:text-lg">Your password has being successfully <br />reset.</p>
        <p className="text-center mb-6 sm:mb-8 max-w-xl mx-auto text-base sm:text-lg">Click below to continue.</p>
        <Button className="w-full py-2 mb-8 mt-2 text-lg">Continue</Button>
        <a href="/login" className="inline-flex items-center  text-blue-600 hover:underline">
        <ArrowLeftIcon className="w-5 mr-1.5" />
        Back to Login
        </a>
    </div>
);
};

export default PasswordResetSuccess;