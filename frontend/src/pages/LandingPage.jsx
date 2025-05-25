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
import { FaUsers } from "react-icons/fa6";
import { DashboardHeading } from "../components/ui/DashboardHeading";

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
    <section className="mb-5">
      <DashboardHeading title="Clyna Overview" description="Monitor your facility’s AI automation activity, patient engagement, and real-time insights."/>
      <div className="flex gap-6">
        <Card className="w-1/4 px-[16px] py-[8px] bg-dashboard-card-color rounded-sm" label="Total Patients" value="0">
        <FaUsers className="text-primary text-[32px] mb-3 mt-1"></FaUsers>
      </Card>
      <Card className="w-1/4 px-[16px] py-[8px] bg-dashboard-card-color rounded-sm" label="Reminders Sent" value="0">
        <FaUsers className="text-primary text-[32px] mb-3 mt-1"></FaUsers>
      </Card>
      <Card className="w-1/4 px-[16px] py-[8px] bg-dashboard-card-color rounded-sm" label="Confirmed Response" value="0">
        <FaUsers className="text-primary text-[32px] mb-3 mt-1"></FaUsers>
      </Card>
      <Card className="w-1/4 px-[16px] py-[8px] bg-dashboard-card-color rounded-sm" label="No Response" value="0">
        <FaUsers className="text-primary text-[32px] mb-3 mt-1"></FaUsers>
      </Card>
      </div>
    </section>
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
