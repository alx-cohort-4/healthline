import {tv} from "tailwind-variants"

export const buttonVariants = tv({
  base: "text-sm  px-2 py-1 inline-flex items-center justify-center gap-3 rounded-md cursor-pointer w-auto transition-all duration-200 ease-in-out ",
  variants: {
    size: {
      md: "max-md:min-h-[1.2rem] text-sm min-h-[1.6rem] max-md:py-0.5 max-md:px-2  py-1 px-3",
      sm: "max-md:min-h-[1rem] text-xs min-h-[2.1rem] max-md:py-0.5 max-md:px-1.5  py-1 px-2",
      custom: "",
      lg: "max-md:min-h-[1.8rem]  min-h-[2.5rem] max-md:py-1 max-md:px-2  py-2 px-4",
    },
    variant: {
       primary: "bg-primary text-white hover:bg-secondary ",
      secondary:
        "text-[#2E323B] border border-[#2E323B]",
      outline:"text-gray-900 ",
      success: "text-green-500 ",
      danger: "text-red-500 dark:text-red-400",
    },
  },
  defaultVariants: {
    size: "md",
    variant: "primary",
  },
})

