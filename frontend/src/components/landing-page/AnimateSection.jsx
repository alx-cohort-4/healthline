import { useInView, motion } from "framer-motion";
import { useRef } from "react";

const variants = {
  hidden: { opacity: 0, y: 50 },
  visible: { opacity: 1, y: 0 },
};
const AnimateSection = ({ children }) => {
  const ref = useRef(null);
  const isInView = useInView(ref, {
    once: true,
    margin: "-80px",
  });

  return (
    <motion.div
      ref={ref}
      animate={isInView ? "visible" : "hidden"}
      variants={variants}
      transition={{ duration: 0.8, delay: 0.25, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
};

export default AnimateSection;
