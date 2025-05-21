const EmailTemplate = ({ clinicName, confirmLink }) => {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gray-50 p-4 font-sans">
      <div className="w-full max-w-[552px] bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
        
        {/* Main Content */}
        <main className="w-full p-6 text-gray-900">
          <p className="mb-4 text-xl font-bold">Hi {clinicName},</p>

          <p className="mb-4 text-base leading-relaxed">
            Thank you for signing up with <strong>Clyna</strong>! You’re just one click away from getting started. Please confirm your email address by clicking the button below:
          </p>

          <div className="mb-6">
            <a
              href={confirmLink}
              className="inline-block bg-blue-600 text-white font-semibold py-3 px-8 rounded-lg shadow-md hover:bg-blue-700 transition"
            >
              Confirm My Email
            </a>
          </div>

          <p className="mb-2 text-sm text-gray-600 leading-relaxed">
            If you didn't sign up for <strong>Clyna</strong>, you can safely ignore this email.
          </p>

          <p className="font-semibold py-2 text-base">The Clyna Team</p>

          <p className="mb-2 text-sm text-gray-600 leading-relaxed">
            If the button above doesn’t work, copy and paste this link into your browser:
          </p>

          {/* Full link display */}
          <div className="mt-2 p-3 border border-blue-600 rounded-lg break-words text-blue-700 font-mono text-sm shadow-sm select-all">
            <a href={confirmLink} className="hover:underline">
              {confirmLink}
            </a>
          </div>
        </main>

        {/* Footer Notice*/}
        <div className="w-full bg-blue-600 text-white px-4 py-4 text-sm text-left">
          <p>
            If you didn’t request this, please ignore this email...
          </p>
        </div>
      </div>
    </div>
  );
};

export default EmailTemplate;
