import React, { useState } from 'react';
import {
  ArrowRightIcon,
  Squares2X2Icon,
  CalendarDaysIcon,
  ChatBubbleLeftRightIcon,
  CloudArrowUpIcon,
} from '@heroicons/react/24/outline';
import { HiAdjustmentsHorizontal } from 'react-icons/hi2';
import { Wand2 } from 'lucide-react';

const colorClasses = {
  green: {
    base: 'text-green-800',
    hover: 'bg-green-800 text-white',
  },
  blue: {
    base: 'text-blue-600',
    hover: 'bg-blue-600 text-white',
  },
  teal: {
    base: 'text-teal-600',
    hover: 'bg-teal-600 text-white',
  },
  amber: {
    base: 'text-gray-600',
    hover: 'bg-gray-600 text-white',
  },
  yellow: {
    base: 'text-yellow-700',
    hover: 'bg-yellow-700 text-white',
  },
  purple: {
    base: 'text-purple-500',
    hover: 'bg-purple-500 text-white',
  },
};

const features = [
  {
    title: "Unified Admin Dashboard",
    icon: Squares2X2Icon,
    color: "blue",
    description:
      "A command center for all patient communications, (passing of information and getting feedback). Monitor appointments, access patient interactions, manage notifications, and oversee automation—all from a single, intuitive interface.",
  },
  {
    title: "AI-Powered Appointment Scheduling",
    icon: CalendarDaysIcon,
    color: "green",
    description:
      "Optimize your calendar and reduce no-shows. Send intelligent reminders, manage confirmations, and allow seamless rescheduling—all logged in real time. Staff can manually override or update appointment statuses as needed.",
  },
  {
    title: "Automated Patient Interaction Logs",
    icon: ChatBubbleLeftRightIcon,
    color: "yellow",
    description:
      "Track every conversation without lifting a finger. All AI-led voice and chat interactions are logged and transcribed, giving staff easy access to past conversations for follow-ups, audits, or performance reviews.",
  },
  {
    title: "Configurable Settings",
    icon: HiAdjustmentsHorizontal,
    color: "amber",
    description:
      "Tailor the assistant to match clinic operations. Set working hours, choose a preferred AI voice, define response templates, and fine-tune automation behavior—all within a structured, easy-to-manage settings page.",
  },
  {
    title: "Flexible Patient Data Intake",
    icon: CloudArrowUpIcon,
    color: "teal",
    description:
      "Add clients manually, import via spreadsheet, or connect with your EMR. Choose how to onboard patients based on your workflow—ideal for clinics of all sizes, whether you're just starting out or scaling up.",
  },
  {
    title: "Smart Action Management",
    icon: Wand2,
    color: "purple",
    description:
      "Confirm, reschedule, or cancel appointments with one click. Use action-based controls linked to appointment statuses for quick administrative decisions—no complicated workflows, just fast execution.",
  },
];

const HealthlineFeatures = () => {
  const [hoveredIndex, setHoveredIndex] = useState(null);

  return (
    <section className="py-16 bg-gray-50 text-gray-800">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl text-center font-bold mb-4">AI HealthLine Features</h2>
        <p className="text-lg text-center text-gray-600 mb-12">
          AI HealthLine automates repetitive tasks, enhances appointment <br /> 
          management, and simplifies patient engagement—allowing your staff to <br />
          focus on quality care delivery.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            const color = colorClasses[feature.color];
            const isHovered = hoveredIndex === index;
            const iconClass = isHovered ? color.hover : color.base;

            return (
              <div
                key={index}
                className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow"
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                <div
                  className={`w-10 h-10 rounded-md flex items-center justify-center mb-3 transition-colors duration-200 ${iconClass}`}
                >
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-700">{feature.description}</p>
                <a href="#" className="flex items-center text-blue-500 mt-4 hover:underline">
                  Read More
                  <ArrowRightIcon className="w-5 h-5 ml-4" />
                </a>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HealthlineFeatures;
