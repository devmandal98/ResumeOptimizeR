import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { UserPlus, Upload } from 'lucide-react';

interface RegisterFormValues {
  username: string;
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const Register: React.FC = () => {
  const [profileFile, setProfileFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterFormValues>();
  const password = watch('password');

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setProfileFile(file);
  };

  const onSubmit = async (data: RegisterFormValues) => {
    setError(null);
    setSuccess(null);
    if (data.password !== data.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    const form = new FormData();
    form.append('username', data.username);
    form.append('name', data.name);
    form.append('email', data.email);
    form.append('password', data.password);
    if (profileFile) {
      form.append('file', profileFile);
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        body: form
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Registration failed');
      }

      setSuccess('Registration successful! Redirecting to login…');
      setTimeout(() => window.location.href = '/login', 1500);
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="container mx-auto px-4 py-8 md:py-16"
    >
      <div className="max-w-lg mx-auto bg-gray-800 bg-opacity-80 backdrop-blur-lg rounded-xl shadow-xl border border-gray-700 overflow-hidden">
        <div className="p-8">
          <div className="flex justify-center mb-6">
            <div className="bg-purple-500 bg-opacity-20 p-4 rounded-full">
              <UserPlus className="h-8 w-8 text-purple-400" />
            </div>
          </div>
          <h2 className="text-2xl font-bold text-center mb-6">Create Your Account</h2>
          {error && <p className="text-red-400 text-center mb-4">{error}</p>}
          {success && <p className="text-green-400 text-center mb-4">{success}</p>}
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className="grid gap-6">
              <div className="flex justify-center mb-2">
                <div className="relative">
                  <div className="w-24 h-24 rounded-full overflow-hidden bg-gray-700 flex items-center justify-center border-2 border-gray-600">
                    {profileFile
                      ? <img src={URL.createObjectURL(profileFile)} alt="Profile" className="w-full h-full object-cover" />
                      : <span className="text-gray-400">Photo</span>
                    }
                  </div>
                  <label htmlFor="profilePhoto" className="absolute bottom-0 right-0 bg-blue-500 p-2 rounded-full cursor-pointer hover:bg-blue-600">
                    <Upload className="h-4 w-4 text-white" />
                    <input
                      id="profilePhoto"
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={handleImageChange}
                    />
                  </label>
                </div>
              </div>
              { /* Username, Name, Email, Password, Confirm fields */ }
              <div>
                <label className="block text-sm text-gray-300 mb-2">Username</label>
                <input
                  {...register('username', { required: 'Username is required' })}
                  className={`w-full px-4 py-3 bg-gray-700 border rounded-lg focus:ring-2 ${
                    errors.username ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
                  }`}
                  placeholder="Choose a username"
                />
                {errors.username && <p className="mt-2 text-sm text-red-400">{errors.username.message}</p>}
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-2">Full Name</label>
                <input
                  {...register('name', { required: 'Name is required' })}
                  className={`w-full px-4 py-3 bg-gray-700 border rounded-lg focus:ring-2 ${
                    errors.name ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
                  }`}
                  placeholder="Enter your full name"
                />
                {errors.name && <p className="mt-2 text-sm text-red-400">{errors.name.message}</p>}
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-2">Email</label>
                <input
                  {...register('email', {
                    required: 'Email is required',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Invalid email address'
                    }
                  })}
                  className={`w-full px-4 py-3 bg-gray-700 border rounded-lg focus:ring-2 ${
                    errors.email ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
                  }`}
                  placeholder="Enter your email"
                />
                {errors.email && <p className="mt-2 text-sm text-red-400">{errors.email.message}</p>}
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-2">Password</label>
                <input
                  type="password"
                  {...register('password', {
                    required: 'Password is required',
                    minLength: { value: 8, message: 'At least 8 characters' }
                  })}
                  className={`w-full px-4 py-3 bg-gray-700 border rounded-lg focus:ring-2 ${
                    errors.password ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
                  }`}
                  placeholder="Create a password"
                />
                {errors.password && <p className="mt-2 text-sm text-red-400">{errors.password.message}</p>}
              </div>
              <div>
                <label className="block text-sm text-gray-300 mb-2">Confirm Password</label>
                <input
                  type="password"
                  {...register('confirmPassword', {
                    required: 'Confirm your password',
                    validate: v => v === password || 'Passwords must match'
                  })}
                  className={`w-full px-4 py-3 bg-gray-700 border rounded-lg focus:ring-2 ${
                    errors.confirmPassword ? 'border-red-500 focus:ring-red-500' : 'border-gray-600 focus:ring-blue-500'
                  }`}
                  placeholder="Confirm your password"
                />
                {errors.confirmPassword && <p className="mt-2 text-sm text-red-400">{errors.confirmPassword.message}</p>}
              </div>

              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                className="w-full bg-gradient-to-r from-purple-500 to-pink-600 text-white py-3 px-4 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all duration-300"
              >
                Create Account
              </motion.button>
            </div>
          </form>
          <p className="mt-6 text-center text-gray-400">
            Already have an account?{' '}
            <Link to="/login" className="text-purple-400 hover:text-purple-300 font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default Register;
