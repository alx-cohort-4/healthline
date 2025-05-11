import React, { useState } from "react";
import { ChevronDownIcon } from "../../globals/Icons";

const faqs = [
  {
    question: "What is Clyna and who is it for?",
    answer:
      "Clyna is an AI-powered platform designed for clinics and healthcare providers to automate patient communication, appointment reminders, and support.",
  },
  {
    question: "Does Clyna make actual calls to patients?",
    answer:
      "Yes, Clyna can make automated calls and send messages to patients for appointment reminders and follow-ups.",
  },
  {
    question: "Can I import patient data from my hospital's EMR?",
    answer:
      "You can import patient data via spreadsheet or connect compatible EMR systems for seamless data sync.",
  },
  {
    question: "What happens if a patient misses a call?",
    answer:
      "If a patient misses a call, the system will attempt to reach them again or send a follow-up message.",
  },
  {
    question: "Is patient data secure on this platform?",
    answer:
      "Yes, all patient data is encrypted and handled according to healthcare data security standards.",
  },
  {
    question: "Can I try it before subscribing?",
    answer:
      "You can request a demo or access a trial to experience the platform before subscribing.",
  },
];

export default function FAQSection() {
  const [openIndex, setOpenIndex] = useState(null);

  const toggle = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="w-full  max-w-2xl mx-auto py-10 px-2 sm:py-16 sm:px-0">
      <h2 className="text-2xl sm:text-3xl font-bold text-center mb-2 text-gray-800">
        Frequently Asked Questions
      </h2>
      <p className="text-center text-gray-500 mb-6 sm:mb-8 max-w-xl mx-auto text-base sm:text-lg">
        Find quick answers to common questions about getting started, using AI
        HealthLine, and support.
      </p>
      <div className="space-y-3 sm:space-y-4">
        {faqs.map((faq, index) => (
          <div
            key={faq.question}
            className="border border-gray-200 rounded-lg bg-white overflow-hidden shadow-sm"
          >
            <button
              className="w-full flex justify-between items-center px-4 sm:px-6 py-4 sm:py-5 text-left font-semibold text-base sm:text-lg text-gray-900 focus:outline-none focus:bg-gray-50 transition"
              aria-expanded={openIndex === index}
              aria-controls={`faq-panel-${index}`}
              onClick={() => toggle(index)}
            >
              <span className="flex-1 text-left">{faq.question}</span>
              <span
                className="ml-2 sm:ml-4 transition-transform"
                style={{
                  transform:
                    openIndex === index ? "rotate(180deg)" : "rotate(0deg)",
                }}
              >
                <ChevronDownIcon className="w-4 h-4" />
              </span>
            </button>
            {openIndex === index && (
              <div
                id={`faq-panel-${index}`}
                className="px-4 sm:px-6 pb-4 sm:pb-5 text-gray-700 animate-fadeIn text-sm sm:text-base"
                role="region"
                aria-labelledby={`faq-header-${index}`}
              >
                {faq.answer}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}


