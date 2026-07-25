import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { User, Shield, Phone, KeyRound, CheckCircle2 } from "lucide-react";
import { useAuth } from "@/modules/auth";
import {
  UpdateProfileFormData,
  updateProfileSchema,
  ChangePasswordFormData,
  changePasswordSchema,
} from "@/utils/validation";
import { Card, Button, Input, PasswordInput, Avatar, Badge, Alert } from "@/components/common";

export const Profile: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [profileSuccess, setProfileSuccess] = useState<string | null>(null);
  const [passwordSuccess, setPasswordSuccess] = useState<string | null>(null);

  const {
    register: registerProfile,
    handleSubmit: handleProfileSubmit,
    formState: { errors: profileErrors, isSubmitting: isProfileSubmitting },
  } = useForm<UpdateProfileFormData>({
    resolver: zodResolver(updateProfileSchema),
    defaultValues: {
      full_name: user?.full_name || "",
      phone_number: user?.phone_number || "",
    },
  });

  const {
    register: registerPassword,
    handleSubmit: handlePasswordSubmit,
    reset: resetPasswordForm,
    formState: { errors: passwordErrors, isSubmitting: isPasswordSubmitting },
  } = useForm<ChangePasswordFormData>({
    resolver: zodResolver(changePasswordSchema),
    defaultValues: {
      old_password: "",
      new_password: "",
      new_password_confirm: "",
    },
  });

  const onProfileSubmit = async (data: UpdateProfileFormData) => {
    setProfileSuccess(null);
    // Simulate API update for Phase 3 UI demonstration
    await new Promise((resolve) => setTimeout(resolve, 600));
    updateUser(data);
    setProfileSuccess("Profile details updated successfully.");
  };

  const onPasswordSubmit = async () => {
    setPasswordSuccess(null);
    // Simulate password rotation for Phase 3 UI demonstration
    await new Promise((resolve) => setTimeout(resolve, 800));
    resetPasswordForm();
    setPasswordSuccess("Security credentials rotated successfully.");
  };

  return (
    <div className="flex flex-col gap-6 animate-fade-in max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
          <User className="h-6 w-6 text-primary-600 dark:text-primary-400" />
          Account & Profile Settings
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Manage your personal agricultural profile identity, role badges, and account security.
        </p>
      </div>

      <Card className="p-6 flex flex-col sm:flex-row items-center sm:items-start gap-6 bg-gradient-to-r from-primary-500/10 via-transparent to-transparent">
        <Avatar name={user?.full_name || "User"} size="xl" />
        <div className="flex-1 text-center sm:text-left">
          <div className="flex flex-col sm:flex-row sm:items-center gap-2">
            <h2 className="text-xl font-bold text-slate-900 dark:text-slate-100">
              {user?.full_name || "Dhatree Farmer"}
            </h2>
            <Badge variant="primary" size="sm" className="w-fit mx-auto sm:mx-0 uppercase tracking-wider">
              {user?.role || "farmer"}
            </Badge>
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{user?.email}</p>
          <div className="flex flex-wrap gap-4 mt-3 text-xs text-slate-500 dark:text-slate-400 justify-center sm:justify-start">
            <span>Username: <strong className="text-slate-700 dark:text-slate-200">@{user?.username}</strong></span>
            <span>Account Status: <strong className="text-success-600 dark:text-success-400">Active</strong></span>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100 border-b border-slate-100 dark:border-forest-light pb-3 mb-4 flex items-center gap-2">
            <User className="h-4 w-4 text-primary-600" />
            Profile Information
          </h3>

          {profileSuccess && (
            <Alert
              variant="success"
              title="Profile Saved"
              onClose={() => setProfileSuccess(null)}
              className="mb-4"
            >
              {profileSuccess}
            </Alert>
          )}

          <form onSubmit={handleProfileSubmit(onProfileSubmit)} className="flex flex-col gap-4">
            <Input
              label="Full Name"
              error={profileErrors.full_name?.message}
              {...registerProfile("full_name")}
            />

            <Input
              label="Phone Number"
              placeholder="+919876543210"
              leftIcon={<Phone className="w-4 h-4" />}
              error={profileErrors.phone_number?.message}
              {...registerProfile("phone_number")}
            />

            <div className="pt-2">
              <Button
                type="submit"
                variant="primary"
                isLoading={isProfileSubmitting}
                leftIcon={<CheckCircle2 className="w-4 h-4" />}
                className="w-full"
              >
                Save Profile Changes
              </Button>
            </div>
          </form>
        </Card>

        <Card className="p-6">
          <h3 className="text-base font-semibold text-slate-800 dark:text-slate-100 border-b border-slate-100 dark:border-forest-light pb-3 mb-4 flex items-center gap-2">
            <Shield className="h-4 w-4 text-primary-600" />
            Security & Password Rotation
          </h3>

          {passwordSuccess && (
            <Alert
              variant="success"
              title="Security Updated"
              onClose={() => setPasswordSuccess(null)}
              className="mb-4"
            >
              {passwordSuccess}
            </Alert>
          )}

          <form onSubmit={handlePasswordSubmit(onPasswordSubmit)} className="flex flex-col gap-4">
            <PasswordInput
              label="Current Password"
              leftIcon={<KeyRound className="w-4 h-4" />}
              error={passwordErrors.old_password?.message}
              {...registerPassword("old_password")}
            />

            <PasswordInput
              label="New Password"
              placeholder="Min 10 chars"
              leftIcon={<KeyRound className="w-4 h-4" />}
              error={passwordErrors.new_password?.message}
              {...registerPassword("new_password")}
            />

            <PasswordInput
              label="Confirm New Password"
              placeholder="Re-type new password"
              leftIcon={<KeyRound className="w-4 h-4" />}
              error={passwordErrors.new_password_confirm?.message}
              {...registerPassword("new_password_confirm")}
            />

            <div className="pt-2">
              <Button
                type="submit"
                variant="secondary"
                isLoading={isPasswordSubmitting}
                leftIcon={<Shield className="w-4 h-4" />}
                className="w-full"
              >
                Rotate Password
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default Profile;
