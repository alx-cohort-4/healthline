import {tv} from "tailwind-variants"

export const buttonVariants = tv({
  base: "text-sm  px-2 py-1 inline-flex items-center justify-center gap-3 rounded-md !cursor-pointer w-auto transition-all duration-200 ease-in-out ",
  variants: {
    size: {
      md: " text-sm min-h-[1.6rem]  max-md:px-2  py-1 px-3",
      sm: " text-xs min-h-[2.1rem]  max-md:px-1.5  py-1 px-2",
      custom: "",
      lg: "  min-h-[2.5rem] max-md:py-1 max-md:px-2  py-2 px-4",
    },
    variant: {
       primary: "bg-primary text-white hover:bg-secondary ",
      secondary:
        "text-[#2E323B] border border-[#2E323B]",
      outline:"text-primary border border-primary hover:bg-secondary hover:text-white",
      success: "text-green-500 ",
      danger: "text-red-500 dark:text-red-400",
    },
  },
  defaultVariants: {
    size: "md",
    variant: "primary",
  },
})

