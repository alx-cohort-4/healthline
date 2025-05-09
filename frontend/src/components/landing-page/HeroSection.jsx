import React from "react";

const HeroSection = () => {
  return (
    <div className="relative px-4 md:px-12 lg:px-20  bg-white min-h-[600px] flex items-center justify-center p-8 overflow-hidden">
      <div className="absolute top-[-50%] left-[-50%] w-[200%] h-[200%] bg-[#175cd3] opacity-10 blur-[100px] -z-10"></div>

      <div className="relative z-10 max-w-3xl text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900 leading-tight">
          Automated Appointment Calls & Chat for your Clinic
        </h1>
        <p className="text-xl text-gray-600 mb-10 leading-relaxed">
          Streamline patient communication with AI-powered
          <br />
          reminders, chat, and booking.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="bg-[#175cd3] text-white px-8 py-3 rounded-lg font-semibold hover:bg-[#124ba8] transition-colors">
            Get Started
          </button>

          <button className="border-2 border-[#175cd3] text-[#175cd3] px-8 py-3 rounded-lg font-semibold hover:bg-[#175cd3] hover:text-white transition-colors">
            Request a Demo
          </button>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
