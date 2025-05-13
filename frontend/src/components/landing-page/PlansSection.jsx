
import { FaCheckCircle } from 'react-icons/fa';
import Button from '../ui/Button';


const plans = [
  {
    title: "Basic Plan",
    description: "For clinics with up to 50 patients/month",
    amount: "$49",
    duration: "/month",
    features: [
      "AI appointment reminders",
      "Basic voice + chat support",
      "Manual patient entry",
      "Email support",
      "Up to 3 team members",
    ],
    btnTitle: "Get Started",
  },
  {
    tag: "recommended",
    title: "Pro Plan",
    description: "For medium clinics, up to 250 patients/month",
    amount: "$129",
    duration: "/month",
    features: [
      "All features in Basic",
      "Spreadsheet import",
      "EMR integration",
      "Appointment dashboard",
      "Up to 10 team members",
    ],
    btnTitle: "Start with Pro",
  },
  {
    title: "Enterprise Plan",
    description: "For hospitals and large practices",
    amount: "Custom Pricing",
    duration: "",
    features: [
      "Everything in Pro",
      "Unlimited patients",
      "Dedicated account manager",
      "Premium support",
      "Custom AI voice logic",
    ],
    btnTitle: "Talk to Sales",
  },
];

const PlansSection = () => {
  return (
    <section className="w-full px-4 md:px-12 lg:px-20  max-w-[1280px] mx-auto  py-12">
      <h2 className="text-2xl sm:text-3xl font-bold text-center mb-2 text-gray-800">
        Choose the Right Plan for Your Clinic
      </h2>
      <p className="text-center text-gray-500 mb-6 sm:mb-8 max-w-xl mx-auto text-base sm:text-lg">
        Whether you're a small clinic or a large hospital, AI HealthLine scales
        to match your needs and automate your patient communication.
      </p>
      <div className="flex flex-col gap-y-6 md:flex-row lg:justify-between lg:gap-x-8">
        {plans.map((eachPlan, index) => (
          <div key={index} className="p-6 border-[#B2B2B2] border rounded-lg grow">
            <div className="mb-2">
              {eachPlan.tag && (
                <button className="capitalize text-[11px] font-bold block w-full bg-[#994D00] py-2 px-4 text-white rounded-lg mb-4">
                  {eachPlan.tag}
                </button>
              )}
              <h1 className="text-[22px]/[28px] font-semibold mb-2">
                {eachPlan.title}
              </h1>
              <p className="font-normal text-sm/[20px] text-[#666666] ">
                {eachPlan.description}
              </p>
            </div>
            <div>
              <h1 className="inline-block text-[32px]/[40px] text-[#175CD3] font-bold">
                {eachPlan.amount}
              </h1>
              <span className="text-base/[24px] font-normal text-[#666666]">
                {eachPlan.duration}
              </span>
            </div>
            <ul className="mt-4 flex flex-col gap-y-[8px] mb-6">
              {eachPlan.features &&
                eachPlan.features.map((feature, index) => (
                  <li className="text-[#1A1A1A] font-normal text-base" key={index}> <span className="inline-block text-[#009933] mr-4"><FaCheckCircle className="inline-block"/></span>
                    <span className="inline-block">{feature}</span>
                  </li>
                ))}
            </ul>
            <Button type="submit" className="w-full mb-2 h-[48px] py-4 mt-2 text-base/[24px] font-semibold">
                 {eachPlan.btnTitle}
            </Button>
          </div>
        ))}
      </div>
    </section>
  );
};

export default PlansSection;
