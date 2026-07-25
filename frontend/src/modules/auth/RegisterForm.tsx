import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate, Link } from "react-router-dom";
import { Mail, User as UserIcon, Phone, KeyRound, UserCheck } from "lucide-react";
import { useAuth } from "./useAuth";
import { RegisterFormData, registerSchema } from "@/utils/validation";
import { Input, PasswordInput, Button, Alert } from "@/components/common";
import { Select } from "@/components/ui/Select";

const ROLE_SELECT_OPTIONS = [
  { label: "Farmer (Primary Agricultural User)", value: "farmer" },
  { label: "Agronomist (Advisory & Crop Specialist)", value: "agronomist" },
  { label: "Researcher (Analytics & Data Scientist)", value: "researcher" },
];

export const RegisterForm: React.FC = () => {
  const { register: registerUser, loading, error, clearError } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      username: "",
      full_name: "",
      phone_number: "",
      role: "farmer",
      password: "",
      password_confirm: "",
    },
  });

  const onSubmit = async (data: RegisterFormData) => {
    clearError();
    try {
      await registerUser(data);
      navigate("/dashboard");
    } catch {
      // Error is handled inside AuthContext
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 w-full">
      {error && (
        <Alert
          variant="danger"
          title="Registration Failed"
          onClose={clearError}
        >
          {error}
        </Alert>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Full Name"
          placeholder="e.g. Ramesh Kumar"
          leftIcon={<UserIcon className="w-4 h-4" />}
          error={errors.full_name?.message}
          {...register("full_name")}
        />

        <Input
          label="Username"
          placeholder="e.g. farmer_ramesh"
          leftIcon={<UserCheck className="w-4 h-4" />}
          error={errors.username?.message}
          {...register("username")}
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Email Address"
          type="email"
          placeholder="ramesh@example.com"
          leftIcon={<Mail className="w-4 h-4" />}
          error={errors.email?.message}
          {...register("email")}
        />

        <Input
          label="Phone Number (Optional)"
          placeholder="e.g. +919876543210"
          leftIcon={<Phone className="w-4 h-4" />}
          error={errors.phone_number?.message}
          {...register("phone_number")}
        />
      </div>

      <Select
        label="Account Role Profile"
        options={ROLE_SELECT_OPTIONS}
        error={errors.role?.message}
        {...register("role")}
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <PasswordInput
          label="Password"
          placeholder="Min 10 chars (A-Z, a-z, 0-9)"
          leftIcon={<KeyRound className="w-4 h-4" />}
          error={errors.password?.message}
          {...register("password")}
        />

        <PasswordInput
          label="Confirm Password"
          placeholder="Re-enter password"
          leftIcon={<KeyRound className="w-4 h-4" />}
          error={errors.password_confirm?.message}
          {...register("password_confirm")}
        />
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        isLoading={loading}
        className="w-full mt-2"
      >
        Create Platform Account
      </Button>

      <div className="text-center text-xs text-slate-600 dark:text-slate-400 mt-2">
        Already have an active profile?{" "}
        <Link to="/login" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
          Sign In Here
        </Link>
      </div>
    </form>
  );
};
