import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { CROP_NAMES } from '../utils/constants';

interface ProfileFormData {
  name: string;
  email: string;
  farmName: string;
  location: string;
  farmSize: number;
  preferredCrops: string[];
}

interface NotificationSettings {
  emailAlerts: boolean;
  smsAlerts: boolean;
  priceAlerts: boolean;
  weatherAlerts: boolean;
  weeklyReport: boolean;
}

const MOCK_USER = {
  name: 'John Farmer',
  email: 'john@myfarm.com',
  farmName: 'Green Valley Farm',
  location: 'Kansas, USA',
  farmSize: 250,
  preferredCrops: ['Wheat', 'Corn', 'Soybean'],
};

const Profile: React.FC = () => {
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [selectedCrops, setSelectedCrops] = useState<string[]>(MOCK_USER.preferredCrops);
  const [notifications, setNotifications] = useState<NotificationSettings>({
    emailAlerts: true,
    smsAlerts: false,
    priceAlerts: true,
    weatherAlerts: true,
    weeklyReport: true,
  });

  const {
    register,
    handleSubmit,
    formState: { errors, isDirty },
  } = useForm<ProfileFormData>({
    defaultValues: MOCK_USER,
  });

  const toggleCrop = (crop: string) => {
    setSelectedCrops(prev =>
      prev.includes(crop) ? prev.filter(c => c !== crop) : [...prev, crop]
    );
  };

  const toggleNotification = (key: keyof NotificationSettings) => {
    setNotifications(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const onSubmit = (data: ProfileFormData) => {
    console.log('Saving profile:', { ...data, preferredCrops: selectedCrops });
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
        <p className="text-sm text-gray-500 mt-1">Manage your account and farm settings</p>
      </div>

      <div className="bg-white rounded-xl shadow-card p-6">
        <div className="flex items-center gap-5 mb-6 pb-6 border-b border-gray-100">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-primary-400 to-primary-700 flex items-center justify-center text-white text-3xl font-bold shadow-md">
            {MOCK_USER.name.charAt(0)}
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">{MOCK_USER.name}</h2>
            <p className="text-sm text-gray-500">{MOCK_USER.email}</p>
            <span className="badge-success mt-1.5 inline-block">🌾 {MOCK_USER.farmName}</span>
          </div>
        </div>

        {saveSuccess && (
          <div className="mb-5 flex items-center gap-3 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-xl p-4 text-sm font-medium">
            <svg className="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Profile saved successfully!
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Full Name</label>
              <input
                {...register('name', { required: 'Name is required' })}
                className="input-field"
                placeholder="Your name"
              />
              {errors.name && <p className="text-xs text-red-500 mt-1">{errors.name.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Email Address</label>
              <input
                {...register('email', {
                  required: 'Email is required',
                  pattern: { value: /^\S+@\S+$/i, message: 'Invalid email' },
                })}
                type="email"
                className="input-field"
                placeholder="your@email.com"
              />
              {errors.email && <p className="text-xs text-red-500 mt-1">{errors.email.message}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Farm Name</label>
              <input
                {...register('farmName')}
                className="input-field"
                placeholder="e.g. Green Valley Farm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Location</label>
              <input
                {...register('location')}
                className="input-field"
                placeholder="City, State/Country"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Farm Size (hectares)</label>
              <input
                {...register('farmSize', { valueAsNumber: true, min: { value: 0, message: 'Must be positive' } })}
                type="number"
                className="input-field max-w-xs"
                placeholder="e.g. 250"
              />
              {errors.farmSize && <p className="text-xs text-red-500 mt-1">{errors.farmSize.message}</p>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Crops</label>
            <div className="flex flex-wrap gap-2">
              {CROP_NAMES.map(crop => (
                <button
                  key={crop}
                  type="button"
                  onClick={() => toggleCrop(crop)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    selectedCrops.includes(crop)
                      ? 'bg-primary-500 text-white shadow-sm'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {crop}
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={
                !isDirty &&
                selectedCrops.slice().sort().join(',') === [...MOCK_USER.preferredCrops].sort().join(',')
              }
              className="btn-primary px-8"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>

      <div className="bg-white rounded-xl shadow-card p-6">
        <h3 className="text-base font-bold text-gray-900 mb-4">Notification Preferences</h3>
        <div className="space-y-4">
          {([
            { key: 'emailAlerts', label: 'Email Alerts', desc: 'Receive alerts via email' },
            { key: 'smsAlerts', label: 'SMS Alerts', desc: 'Receive critical alerts via SMS' },
            { key: 'priceAlerts', label: 'Price Change Alerts', desc: 'Notify when crop prices change significantly' },
            { key: 'weatherAlerts', label: 'Weather Warnings', desc: 'Frost, drought, and severe weather alerts' },
            { key: 'weeklyReport', label: 'Weekly Report', desc: 'Receive weekly farm performance summary' },
          ] as { key: keyof NotificationSettings; label: string; desc: string }[]).map(({ key, label, desc }) => (
            <div key={key} className="flex items-center justify-between py-2">
              <div>
                <p className="text-sm font-medium text-gray-800">{label}</p>
                <p className="text-xs text-gray-500">{desc}</p>
              </div>
              <button
                type="button"
                onClick={() => toggleNotification(key)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 focus:outline-none ${
                  notifications[key] ? 'bg-primary-500' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform duration-200 ${
                    notifications[key] ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Profile;
