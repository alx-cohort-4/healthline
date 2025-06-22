import React, { useState } from 'react';
import { DashboardHeading } from '../../components/ui/DashboardHeading';
import DashboardCard from '../../components/ui/DashboardCard';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const PatientDirectory = () => {
  const [selectedDate, setSelectedDate] = useState(null);

  return (
    <div className="max-w-full md:w-[1092px] mx-auto space-y-6 p-4 md:p-6 font-inter">
      {/* Heading */}
      <DashboardHeading
        title="Patient Directory"
        description="Manage patient records, Clyna reminder statuses, and personalize automated communications."
      />

      {/* Filters */}
      <div className="flex flex-col md:flex-row md:flex-nowrap gap-4 md:gap-[46px] w-full">
        {/* Date Filter */}
        <div className="relative w-full md:w-[253.5px] h-[48px] px-4 border border-[#999] rounded-md bg-white flex items-center">
          <DatePicker
            selected={selectedDate}
            onChange={(date) => setSelectedDate(date)}
            placeholderText="By Date"
            className="w-full bg-transparent outline-none text-[#333] placeholder-[#999]"
            dateFormat="yyyy-MM-dd"
          />
          <span className="material-symbols-outlined text-[#999] text-xl absolute right-3 pointer-events-none">
            calendar_month
          </span>
        </div>

        {/* Status Filter */}
        <div className="relative w-full md:w-[253.5px] h-[48px]">
          <select
            id="filter-status"
            name="status"
            defaultValue=""
            className="appearance-none w-full h-full px-4 pr-10 border border-[#999] rounded-md bg-white text-[#333] focus:outline-none"
          >
            <option value="" disabled hidden>By Status</option>
            <option value="not_set">Not Set</option>
            <option value="confirmed">Confirmed</option>
            <option value="missed">Missed</option>
            <option value="pending">Pending</option>
          </select>
          <span className="material-symbols-outlined text-[#999] absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
            expand_more
          </span>
        </div>

        {/* Search Filter */}
        <div className="relative w-full md:w-[500px] h-[48px] px-4 border border-[#999] rounded-md bg-white flex items-center">
          <input
            type="text"
            id="filter-search"
            name="search"
            placeholder="Search by name, email or phone…"
            className="w-full pr-8 bg-transparent outline-none text-[#333] placeholder:text-[#999]"
          />
          <span className="material-symbols-outlined text-[#999] text-xl absolute right-4">
            search
          </span>
        </div>
      </div>

      {/* Buttons */}
      <div className="flex justify-center lg:justify-end">
        <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 flex-wrap">
          <button className="btn w-full sm:w-[182px] h-[48px] bg-[#175CD3] text-white flex items-center justify-center gap-2 rounded-md">
            Add manually
            <span className="material-symbols-outlined text-white text-lg">add</span>
          </button>
          <button className="btn w-full sm:w-[235px] h-[48px] bg-[#175CD3] text-white flex items-center justify-center gap-2 rounded-md">
            Upload spreadsheet
            <span className="material-symbols-outlined text-white text-lg">upload</span>
          </button>
          <button className="btn w-full sm:w-[202px] h-[48px] bg-[#175CD3] text-white flex items-center justify-center gap-2 rounded-md">
            Connect to EMR
            <span className="material-symbols-outlined text-white text-xl">share</span>
          </button>
        </div>
      </div>

      {/* Pagination */}
      <div className="flex flex-col sm:flex-row items-center justify-between border-t pt-3 px-4 gap-3">
        <button className="font-inter text-sm font-normal leading-5 tracking-[0.25px] text-[#175CD3] bg-transparent border-none">
          Back
        </button>
        <p className="text-sm font-normal leading-5 tracking-[0.25px] text-[#333] text-center">
          Page 1 of 10
        </p>
        <button className="btn btn-sm bg-[#175CD3] text-white text-sm font-normal leading-5 tracking-[0.25px] rounded-md">
         Next
        </button>
      </div>
    </div>
  );
};


export default PatientDirectory;
