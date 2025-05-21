 import Button from "../ui/Button";

const CallToActionSection = () => {
  return (
    <section className="w-full px-4 md:px-12 lg:px-20  max-w-[1280px] mx-auto  py-12">
      <h2 className="text-2xl sm:text-3xl font-bold text-center mb-2 text-gray-800">
        Take Control of Your Patient Engagement Today
      </h2>
      <p className="text-center text-gray-500 mb-6 sm:mb-8 max-w-xl mx-auto text-base sm:text-lg">
        Streamline your operations, reduce no-shows, and deliver faster, smarter
        care — all from one intelligent dashboard.
      </p>
      <div className="text-center">
        <Button
          type="button"
          className="mb-2 h-[48px] py-4 mt-2 text-base/[24px] font-semibold mr-5"
        >
          Get Started
        </Button>
        <Button
          type="button"
          className="mb-2 h-[48px] py-4 mt-2 text-base/[24px] font-semibold bg-white text-primary border-2 border-primary hover:text-white hover:border-secondary"
        >
          Book a Demo
        </Button>
      </div>
    </section>
  );
};

export default CallToActionSection;
