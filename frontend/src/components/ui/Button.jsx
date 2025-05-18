import cn from "../../libs/cn";
import { buttonVariants } from "../../libs/variants";
import { Slot } from "@radix-ui/react-slot";

const Button = ({
  variant = "primary",
  size = "md",
  asChild = false,
  ...props
}) => {
  const Comp = asChild ? Slot : "button";

  return (
    <Comp
      {...props}
      className={cn(buttonVariants({ variant, size }), props?.className)}
    >
      {props.children}
    </Comp>
  );
};

Button.displayName = "Button";

export default Button;
