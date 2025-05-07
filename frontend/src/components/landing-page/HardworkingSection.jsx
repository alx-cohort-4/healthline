import React from "react";

const steps = [
  {
    number: "01",
    title: "Add or Import Patient Data",
    description: "Easily upload patient records using a simple form, import a spreadsheet, or connect your existing EMR system to sync patient details securely.",
  },
  {
    number: "02",
    title: "AI Handles All Communication",
    description: "Once added, our AI assistance automatically reaches out to patients with appointments, reminders and responds to common questions in voice or chat.",
  },
  {
    number: "03",
    title: "Monitor and Manage Appointments",
    description: "Your staff can track confirmations, reschedules, and missed appointments from a centralized dashboard with filters, transcripts and notifications.",
  },
  {
    number: "04",
    title: "Improve Workflow and Experiences",
    description: "Get clear insights into appointment trends, patient responses, and staff workloads to reduce missed visits and improve overall clinic efficiency.",
  },
];

export default function HardworkingSection() {
  return (
    <section className="w-full max-w-[1280px] h-[654px] mx-auto px-4 py-12">
     <h2 className="w-[680px] h-[44px] mx-auto font-bold text-[36px] leading-[44px] tracking-[0px] text-center text-[#000E43] font-['Bricolage_Grotesque']">
     How AI Healthline Works
     </h2>
     <p className="text-center text-[22px] leading-[28px] tracking-[0px] font-normal font-['Bricolage_Grotesque'] text-[#3B485E] mb-10 max-w-2xl mx-auto">
       Simple steps to automate your patient communications and appointment flow.
      </p>


      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 place-items-center">
        {steps.map((step, index) => (
          <div
            key={index}
            className="w-[544px] h-[205px] bg-white border border-gray-200 rounded-xl shadow-sm p-6 relative"
          >
           <div className="absolute top-4 left-4 w-[29px] h-[29px] flex items-center justify-center rounded-full bg-[#EBEBEB] text-[#175CD3] font-extrabold text-[24px] leading-[100%] font-['Inter']">
           {step.number}
           </div>
            <div className="relative z-10 mt-8">
              <h3 className="text-[18px] font-semibold leading-[28px] text-[#2C2D33] font-['Inter'] mb-2">
                {step.title}
               </h3>
               <p className="text-[16px] font-normal leading-[100%] text-[#646362] font-['Inter']">
                 {step.description}
                </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
