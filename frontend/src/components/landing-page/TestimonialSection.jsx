import { useState } from "react";
import { ArrowLeft, ArrowRight } from "lucide-react";

const testimonials = [
  {
    title: `"40% Drop in No-Shows"`,
    name: "Dr. Sarki Bello",
    role: "Chief Medical Officer, Lifeline Clinic",
    comment:
      "HealthLine AI has transformed how we schedule appointments. Our no-shows have dropped by 40% in just two months!",
    image: "https://i.pravatar.cc/150?img=3",
  },
  {
    title: `"Workflow Made Smoother"`,
    name: "Nurse Tunde Akande",
    role: "Lead Nurse, Healing Hands Hospital",
    comment:
      "Patient satisfaction is up, and the workflow feels so much smoother. We love it!",
    image: "https://i.pravatar.cc/150?img=4",
  },
  {
    title: `"Always-On Assistant"`,
    name: "Mrs. Ruth Eze",
    role: "Admin Manager, City Health Center",
    comment:
      "It’s like having an assistant that never sleeps. Efficient, fast, and reliable.",
    image: "https://i.pravatar.cc/150?img=5",
  },
  {
    title: `"Boosted Patient Happiness"`,
    name: "Dr. Chinedu Nwachukwu",
    role: "Medical Director, Unity Hospital",
    comment:
      "Incredible innovation. We’ve seen a real difference in efficiency and patient happiness.",
    image: "https://i.pravatar.cc/150?img=6",
  },
  {
    title: `"Quick Staff Adoption"`,
    name: "Mrs. Bisi Aluko",
    role: "Clinic Administrator, Grace Medical",
    comment:
      "User-friendly and super reliable. Our staff picked it up in no time!",
    image: "https://i.pravatar.cc/150?img=7",
  },
];

export default function Testimonials() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const { title, name, role, comment, image } = testimonials[currentIndex];

  const isFirst = currentIndex === 0;
  const isLast = currentIndex === testimonials.length - 1;

  const prevSlide = () => {
    if (!isFirst) setCurrentIndex(currentIndex - 1);
  };

  const nextSlide = () => {
    if (!isLast) setCurrentIndex(currentIndex + 1);
  };

  return (
    <section className="bg-white py-8 px-4 flex justify-center">
      <div className="w-full max-w-[1280px] flex flex-col items-center text-center relative">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-2">
          Trusted by Clinics That Care Deeply
        </h2>
        <p className="text-gray-600 text-sm sm:text-base max-w-xl mx-auto mb-6">
          Real results from healthcare teams using HealthLine AI to streamline
          operations, boost patient satisfaction, and cut down no-shows.
        </p>

        <div className="relative w-full max-w-[672px] mx-auto">
          {/* Desktop Arrow Buttons */}
          <div className="hidden md:flex justify-between absolute top-1/2 left-[-50px] right-[-50px] -translate-y-1/2">
            <button
              onClick={prevSlide}
              disabled={isFirst}
              className={`w-10 h-10 rounded-full shadow flex items-center justify-center ${
                isFirst
                  ? "bg-gray-300 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              <ArrowLeft color={isFirst ? "black" : "white"} size={20} />
            </button>
            <button
              onClick={nextSlide}
              disabled={isLast}
              className={`w-10 h-10 rounded-full shadow flex items-center justify-center ${
                isLast
                  ? "bg-gray-300 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              <ArrowRight color={isLast ? "black" : "white"} size={20} />
            </button>
          </div>

          {/* Testimonial Card */}
          <div className="w-full md:w-[672px] h-auto md:h-[230px] bg-white p-6 rounded-xl shadow-md flex flex-col md:flex-row text-left">
            {/* Left (Title) */}
            <div className="md:w-1/2 mb-4 md:mb-0 md:pr-4 flex justify-start md:justify-center items-start md:items-center">
              <p className="text-blue-600 text-lg sm:text-xl font-semibold text-left">
                {title}
              </p>
            </div>

            {/* Right (Content) */}
            <div className="md:w-1/2 md:pl-4 flex flex-col justify-between">
              <p className="text-gray-700 text-sm sm:text-base mb-4">
                {comment}
              </p>
              <div className="flex items-center gap-4">
                <img
                  src={image}
                  alt={name}
                  className="w-12 h-12 rounded-full object-cover"
                />
                <div className="mt-1">
                  <h4 className="font-semibold text-gray-800 text-sm sm:text-base">
                    {name}
                  </h4>
                  <p className="text-xs text-gray-500">{role}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Mobile Arrow Buttons */}
          <div className="flex md:hidden justify-center gap-[15px] mt-4">
            <button
              onClick={prevSlide}
              disabled={isFirst}
              className={`w-10 h-10 rounded-full border flex items-center justify-center ${
                isFirst
                  ? "border-gray-300 bg-white"
                  : "border-blue-600 bg-white"
              }`}
            >
              {!isFirst && (
                <ArrowLeft color="#2563EB" strokeWidth={2} size={20} />
              )}
            </button>
            <button
              onClick={nextSlide}
              disabled={isLast}
              className={`w-10 h-10 rounded-full border flex items-center justify-center ${
                isLast ? "border-gray-300 bg-white" : "border-blue-600 bg-white"
              }`}
            >
              {!isLast && (
                <ArrowRight color="#2563EB" strokeWidth={2} size={20} />
              )}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}