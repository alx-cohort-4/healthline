import React from "react";
import Button from "../ui/Button";
// import useMe from "../../store/useMe";s

const Hero = () => {
  // const token = useMe(state=>state.token)

  // const onRequestDemoClick = () => {

  // }
  return (
    <section className="w-full bg-white  px-4 md:px-12 lg:px-20 py-20">
      <div className="max-w-[1280px] min-h-[432px] h-auto mx-auto flex flex-col lg:flex-row items-center gap-10">
        {/* Left: Text and CTA */}
        <div className="flex-1 max-w-[600px]">
          <h1 className="text-[40px] leading-tight font-bold text-[#000E43] font-['Inter'] mb-4">
            Automated Appointment Calls <br /> & Chat for Your Clinic
          </h1>
          <p className="text-lg text-[#3B485E] mb-6">
            Streamline patient communication with Clyna-powered reminders, chat,
            and booking.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button
              type="submit"
              className="min-w-fit px-8 mb-2 h-[48px] py-4 mt-2 text-base/[24px] font-semibold"
            >
              Get Started
            </Button>

            <Button
              type="submit"
              variant="outline"
              className="w-fit mb-2 px-8 h-[48px] py-4 mt-2 text-base/[24px] font-semibold"
            >
              Request a Demo
            </Button>
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
