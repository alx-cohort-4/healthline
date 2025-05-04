import React from 'react';
import Login from '../components/login';

const LoginPage = () => {
  return (
    <div className="flex min-h-screen w-full">
      <div className="flex items-center justify-center min-h-[85vh] h-auto">
        <Login />
      </div>
    </div>
  );
};

export default LoginPage;
