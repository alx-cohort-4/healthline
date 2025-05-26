import Nav from "../components/shared/Nav";
import HardworkingSection from "../components/landing-page/HardworkingSection";
import FAQSection from "../components/landing-page/FAQSection";
import Footer from "../components/shared/Footer";
import AnimateSection from "../components/landing-page/AnimateSection";
import HealthlineFeatures from "../components/landing-page/HealthlineFeatures";
import Testimonials from "../components/landing-page/TestimonialSection";
import Hero from "../components/landing-page/Hero";
import PlansSection from "../components/landing-page/PlansSection";
import CallToActionSection from "../components/landing-page/CallToActionSection";
import Card from "../components/ui/DashboardCard";
import { FaAngleDown, FaCalendar, FaMagnifyingGlass, FaUsers } from "react-icons/fa6";
import { DashboardHeading } from "../components/ui/DashboardHeading";
import { SelectionField, TextField } from "../components/ui/DashboardFields";
import { FaCalendarAlt } from "react-icons/fa";

const LandingPage = () => (
  <div className=" flex flex-col min-h-dvh    ">
    <Nav />
    <AnimateSection>
      <Hero />
    </AnimateSection>
    <AnimateSection>
      <HealthlineFeatures />
    </AnimateSection>
    <AnimateSection>
      <HardworkingSection />
    </AnimateSection>
    <AnimateSection>
      <PlansSection />
    </AnimateSection>
    <AnimateSection>
      <Testimonials />
    </AnimateSection>
    <AnimateSection>
      <FAQSection />
    </AnimateSection>
    <AnimateSection>
      <CallToActionSection />
    </AnimateSection>
    <Footer />
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
