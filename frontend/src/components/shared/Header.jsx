import { Link } from "react-router-dom";

const navItems = [
  { name: "Features", path: "/features" },
  { name: "How It Works", path: "/how-it-works" },
  { name: "Contact Us", path: "/contact-us" },
  { name: "Login", path: "./login"}
];

const Header = () => {
  return (
    <header className="flex justify-between items-center py-6   ">
      <span className="text-primary text-3xl font-semibold ">
        Clyna
      </span>
      <nav>
        <ul className="flex space-x-8">
          {navItems.map((item) => (
            <li key={item.name} className="text-primary ">
              <Link to={item.path} className="">
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
