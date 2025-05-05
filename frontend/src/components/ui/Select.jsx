import React from "react";
import * as SelectPrimitive from "@radix-ui/react-select";
import { Check, ChevronDown } from "lucide-react";
import cn from "../../libs/utils/cn";

const Select = React.forwardRef(
  ({ options, placeholder, error, label, required, ...props }, ref) => {
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
            <SelectPrimitive.Content className="overflow-hidden bg-white rounded-md shadow-lg border border-gray-200 z-50">
              <SelectPrimitive.Viewport className="p-1">
                <SelectPrimitive.Group>
                  {options.map((option) => (
                    <SelectPrimitive.Item
                      key={option.value}
                      value={option.value}
                      className="text-sm relative flex items-center h-8 px-6 rounded hover:bg-gray-100 cursor-pointer outline-none data-[highlighted]:bg-gray-100"
                    >
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
