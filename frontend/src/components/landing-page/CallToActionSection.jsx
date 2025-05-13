import Button from '../ui/Button';

const CallToActionSection = () => {
  return (
    <section className="w-full px-4 md:px-12 lg:px-20  max-w-[1280px] mx-auto  py-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-center mb-2 text-gray-800">
        Take Control of Your Patient Engagement Today
      </h2>
      <p className="text-center text-gray-500 mb-6 sm:mb-8 max-w-xl mx-auto text-base sm:text-lg">
        Streamline your operations, reduce no-shows, and deliver faster, smarter care — all from one intelligent dashboard.
      </p>
      <div>
        <Button type="submit" className="mb-2 h-[48px] py-4 mt-2 text-base/[24px] font-semibold">
        Get Started
        </Button>
      </div>
        
    </section>
  )
}

export default CallToActionSection