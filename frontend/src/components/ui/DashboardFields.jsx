import React from "react";

export const TextField = ({
  id,
  name,
  type,
  placeholder,
  children,
  className,
}) => {
  return (
    <div className={className}>
      <input
        id={id}
        name={name}
        type={type}
        placeholder={placeholder}
        className="w-full border-0 outline-0"
      />
      <div className="pt-1">{children}</div>
    </div>
  );
};

export const SelectionField = ({ name, id, className, children, options }) => {
  return (
    <div className={className}>
      <select
        name={name}
        id={id}
        className="w-full border-0 outline-0 appearance-none"
      >
        {options.map((eachOption) => {
          return (
            <option
              className="w-full px-2 block"
              key={eachOption.id}
              value={eachOption.value}
            >
              {eachOption.label}
            </option>
          );
        })}
      </select>
      <div className="pt-1">{children}</div>
    </div>
  );
};
