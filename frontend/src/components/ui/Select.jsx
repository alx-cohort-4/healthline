import React, { useState, useEffect } from "react";
import * as SelectPrimitive from "@radix-ui/react-select";
import { Check, ChevronDown, Search } from "lucide-react";
import cn from "../../libs/cn";

const Select = React.forwardRef(
  ({ options = [], placeholder, error, label, required, ...props }, ref) => {
    const [filteredOptions, setFilteredOptions] = useState(options);

    useEffect(() => {
      setFilteredOptions(options);
    }, [options]);

    return (
      <div className="w-full">
        {label && (
          <p className="text-sm text-gray-600 mb-1">
            {label}
            {required && <span className="text-red-500">*</span>}
          </p>
        )}
        <SelectPrimitive.Root {...props}>
          <SelectPrimitive.Trigger
            ref={ref}
            aria-label={label || "Select"}
            className={cn(
              "text-sm w-full p-3 border flex justify-between items-center rounded focus:outline-none focus:ring-2 focus:ring-blue-400",
              error ? "border-red-500" : "border-gray-300"
            )}
          >
            <SelectPrimitive.Value placeholder={placeholder} />
            <SelectPrimitive.Icon>
              <ChevronDown className="h-4 w-4" />
            </SelectPrimitive.Icon>
          </SelectPrimitive.Trigger>

          <SelectPrimitive.Portal>
            <SelectPrimitive.Content
              position="popper"
              side="bottom"
              align="start"
              sideOffset={4}
              className="w-[var(--radix-select-trigger-width)] max-h-[300px] bg-white rounded-md shadow-lg border border-gray-200 z-50"
            >
              <div className="p-2 flex items-center border-b border-gray-100 bg-white sticky top-0">
                <Search className="h-4 w-4 text-gray-400 ml-2" />
                <input
                  className="w-full p-1 text-sm border-none focus:outline-none placeholder-gray-400"
                  placeholder="Search..."
                  onChange={(e) => {
                    const searchValue = e.target.value.toLowerCase();
                    setFilteredOptions(
                      options.filter(
                        (option) =>
                          option.label.toLowerCase().includes(searchValue) ||
                          option.value.toLowerCase().includes(searchValue)
                      )
                    );
                  }}
                />
              </div>
              <SelectPrimitive.Viewport className="p-1 max-h-[300px] overflow-y-auto">
                <SelectPrimitive.ScrollUpButton className="flex items-center justify-center h-6 bg-white text-gray-700 cursor-default select-none sticky top-0 z-10">
                  <ChevronDown className="h-4 w-4" />
                </SelectPrimitive.ScrollUpButton>
                <SelectPrimitive.Group>
                  {filteredOptions.map((option) => (
                    <SelectPrimitive.Item
                      key={option.value}
                      value={option.value}
                      className="text-sm relative flex items-center h-8 px-6 rounded hover:bg-gray-100 cursor-pointer outline-none data-[highlighted]:bg-gray-100"
                    >
                      {option?.icon && (
                        <img
                          src={option.icon}
                          alt={option.label}
                          className="w-4 h-4 mr-2"
                        />
                      )}
                      <SelectPrimitive.ItemText>
                        {option.label}
                      </SelectPrimitive.ItemText>
                      <SelectPrimitive.ItemIndicator className="absolute left-1">
                        <Check className="h-4 w-4" />
                      </SelectPrimitive.ItemIndicator>
                    </SelectPrimitive.Item>
                  ))}
                </SelectPrimitive.Group>
              </SelectPrimitive.Viewport>
            </SelectPrimitive.Content>
          </SelectPrimitive.Portal>
        </SelectPrimitive.Root>
        {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
      </div>
    );
  }
);

Select.displayName = "Select";

export default Select;
