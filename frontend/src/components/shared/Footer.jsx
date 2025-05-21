import { SecLogoIconFlip } from "../../globals/Icons";
import { FaFacebook, FaLinkedin, FaX } from "react-icons/fa6";

const socialLinks = [
  {
    icon: <FaFacebook />,
    href: "https://www.facebook.com",
  },
  {
    icon: <FaLinkedin />,
    href: "https://www.linkedin.com",
  },
  {
    icon: <FaX />,
    href: "https://www.x.com",
  },
];

const quickLinks = [
  {
    label: "Home",
    href: "",
  },
  {
    label: "Features",
    href: "features",
  },
  {
    label: "Pricing",
    href: "pricing",
  },
  {
    label: "How It Works",
    href: "how-it-works",
  },
  {
    label: "Contact Us",
    href: "contact",
  },
  {
    label: "Terms & Privacy",
    href: "terms",
  },
];

const Footer = () => {
  return (
    <footer className="bg-primary text-white pt-10 pb-4 px-4 md:px-12 lg:px-20">
      <div className="w-auto mx-auto flex flex-col md:flex-row md:justify-between gap-10 md:gap-0">
        <div className="flex-1 ">
          <div className="flex items-center gap-2 mb-4">
            {/* Logo Icon */}
            <SecLogoIconFlip className="max-md:w-20 max-md:h-8 " />
          </div>
          <p className="italic text-white/80 mb-2 text-sm">
            Smarter care. Simpler systems.
          </p>
          <p className="text-white/80 md:w-2/3 text-sm">
            Empowering clinics with AI to streamline appointments, automate
            interactions, and improve patient experiences.
          </p>
        </div>

        <div className="flex-1">
          <div className="font-semibold mb-3">Quick Links</div>
          <ul className="space-y-2 text-white/80 text-sm">
            {quickLinks.map((link, index) => (
              <li key={index}>
                <a href={`#${link.href}`} className="hover:text-white">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div className="flex-1 ">
          <div className="font-semibold mb-3">Contact</div>
          <div className="text-white/80 text-sm mb-1">
            <span className="font-medium">Email:</span> support@aihealthline.com
          </div>
          <div className="text-white/80 text-sm mb-1">
            <span className="font-medium">Phone:</span> +2349000000000
          </div>
          <div className="text-white/80 text-sm mb-3">
            <span className="font-medium">Address:</span> 300 Health st, Lagos
            State, Nigeria
          </div>
          <div className="flex gap-4 mt-2">
            {socialLinks.map((link, index) => (
              <a
                key={index}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-white"
              >
                {link.icon}
              </a>
            ))}
          </div>
        </div>
      </div>
      <hr className="my-6 border-white/30" />
      <div className="text-center text-xs text-white/70">
        © {new Date().getFullYear()} Clyna. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;
