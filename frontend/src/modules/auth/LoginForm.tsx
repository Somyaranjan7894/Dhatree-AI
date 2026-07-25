import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate, Link } from "react-router-dom";
import { Mail, KeyRound, LogIn } from "lucide-react";
import { useAuth } from "./useAuth";
import { LoginFormData, loginSchema } from "@/utils/validation";
import { Input, PasswordInput, Button, Alert } from "@/components/common";

export const LoginForm: React.FC = () => {
  const { login, loading, error, clearError } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identifier: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    clearError();
    try {
      await login(data);
      navigate("/dashboard");
    } catch {
      // Error is caught and set inside AuthContext
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5 w-full">
      {error && (
        <Alert
          variant="danger"
          title="Authentication Error"
          onClose={clearError}
        >
          {error}
        </Alert>
      )}

      <Input
        label="Email or Username"
        placeholder="e.g. farmer.ramesh@dhatree.ai or farmer_ramesh"
        leftIcon={<Mail className="w-4 h-4" />}
        error={errors.identifier?.message}
        {...register("identifier")}
      />

      <PasswordInput
        label="Password"
        placeholder="Enter your account password"
        leftIcon={<KeyRound className="w-4 h-4" />}
        error={errors.password?.message}
        {...register("password")}
      />

      <div className="flex items-center justify-between text-xs mt-1">
        <label className="flex items-center gap-2 text-slate-600 dark:text-slate-400 cursor-pointer select-none">
          <input type="checkbox" className="rounded border-slate-300 text-primary-600 focus:ring-primary-500" />
          <span>Remember this session</span>
        </label>
        <a href="#forgot" className="text-primary-600 dark:text-primary-400 hover:underline font-medium">
          Forgot Password?
        </a>
      </div>

      <Button
        type="submit"
        variant="primary"
        size="lg"
        isLoading={loading}
        leftIcon={<LogIn className="w-4 h-4" />}
        className="w-full mt-2"
      >
        Sign In to Platform
      </Button>

      <div className="text-center text-xs text-slate-600 dark:text-slate-400 mt-2">
        Don&apos;t have an agricultural account?{" "}
        <Link to="/register" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
          Register New Account
        </Link>
      </div>
    </form>
  );
};
