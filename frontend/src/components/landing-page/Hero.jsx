import React from "react";

const Hero = () => {
  return (
    <section className="w-full bg-white px-6 py-20">
      <div className="max-w-[1280px] h-[432px] mx-auto flex flex-col lg:flex-row items-center gap-10">
        
        {/* Left: Text and CTA */}
        <div className="flex-1 max-w-[600px]">
          <h1 className="text-[40px] leading-tight font-bold text-[#000E43] font-['Inter'] mb-4">
            Automated Appointment Calls <br /> & Chat for Your Clinic
          </h1>
          <p className="text-lg text-[#3B485E] mb-6">
            Streamline patient communication with Clyna-powered reminders, chat, and booking.
          </p>
          <div className="flex flex-wrap gap-4">
            <button className="bg-[#175CD3] text-white text-base font-semibold px-6 py-3 rounded-lg">
              Get Started
            </button>
            <button className="text-[#175CD3] border border-[#175CD3] bg-white text-base font-semibold px-6 py-3 rounded-lg">
              Request a Demo
           </button>
          </div>
        </div>

        <div className="flex-1">
          <img
          src="/images/hero-bot.png"
         alt="AI assistant illustration"
         className="w-[624px] h-[432px] object-contain"
       />
       </div>
      </div>
    </section>
  );
};

export default Hero;
