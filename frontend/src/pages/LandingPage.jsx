import Nav from "../components/shared/Nav";
import HeroSection from "../components/landing-page/HeroSection";
import HardworkingSection from "../components/landing-page/HardworkingSection";
import Testimonials from "../components/landing-page/TestimonialSection";

const LandingPage = () => (
  <div className=" flex px-4 md:px-12 lg:px-25 flex-col min-h-dvh pb-20   ">
    <Nav />
    <HeroSection />
    <HardworkingSection />
    <Testimonials/>
  </div>
);

export default LandingPage;
// This is a placeholder for the landing page content.
// You can add your own components and styles here.
// For example, you might want to include a header, a hero section, and other features.
// You can also import and use other components from your project.
// For example:
// import Header from "../components/Header";
// import HeroSection from "../components/HeroSection";
// import FeaturesSection from "../components/FeaturesSection";
