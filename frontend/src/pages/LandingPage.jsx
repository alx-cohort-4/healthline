import Nav from "../components/shared/Nav";
import HeroSection from "../components/landing-page/HeroSection";
import HardworkingSection from "../components/landing-page/HardworkingSection";
import Testimonials from "../components/landing-page/TestimonialSection";

const LandingPage = () => (
  <div className=" flex flex-col min-h-dvh    ">
    <Nav />
    <HeroSection />
    <Testimonials />
    <HardworkingSection />
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
