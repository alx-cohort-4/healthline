import { Link } from "react-router-dom";
import { WarningIcon } from "../globals/Icons";
const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-white w-screen   items-center justify-center px-4">
      <Link to="/">
        <img src="/Logo.svg" alt="Clyna Logo" className="h-12 mt-4  mb-8" />
      </Link>

      <div className="max-w-2xl mx-auto text-center">
        <div className="mb-8">
          <h1 className="text-7xl font-bold text-blue-600 mb-2">404</h1>
          <div className="h-1 w-24 bg-blue-600 mx-auto mb-8"></div>
        </div>

        <div className="space-y-6">
          <div className="flex justify-center">
            <div className="p-4 bg-blue-100 rounded-full">
              <WarningIcon className={"w-24 h-24 text-blue-600"} />
            </div>
          </div>

          <div className="space-y-4">
            <h2 className="text-3xl font-semibold text-gray-800">
              Page Not Found
            </h2>
            <p className="text-gray-600 text-lg max-w-md mx-auto">
              We apologize, but the page you're looking for seems to have moved
              or doesn't exist. Let us help you find your way back.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
            <Link
              to="/"
              className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition duration-150 ease-in-out"
            >
              Return to Homepage
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
