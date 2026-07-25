import { z } from "zod";

/**
 * Reusable Zod validation schemas across Dhatree AI authentication and profile forms.
 */

export const loginSchema = z.object({
  identifier: z
    .string()
    .min(3, "Email or username must be at least 3 characters long.")
    .trim(),
  password: z
    .string()
    .min(1, "Password is required."),
});

export const registerSchema = z
  .object({
    email: z
      .string()
      .email("Please enter a valid email address.")
      .trim()
      .toLowerCase(),
    username: z
      .string()
      .min(3, "Username must be at least 3 characters.")
      .max(30, "Username cannot exceed 30 characters.")
      .regex(
        /^[a-zA-Z0-9_.-]+$/,
        "Username can only contain letters, numbers, underscores, dots, and hyphens."
      )
      .trim(),
    full_name: z
      .string()
      .min(2, "Full name must be at least 2 characters.")
      .trim(),
    phone_number: z
      .string()
      .optional()
      .or(z.literal(""))
      .refine(
        (val) => !val || /^\+?[1-9]\d{9,14}$/.test(val),
        "Invalid phone number format (e.g. +919876543210)."
      ),
    role: z.enum(["farmer", "agronomist", "researcher", "admin"] as const),
    password: z
      .string()
      .min(10, "Password must be at least 10 characters long.")
      .regex(/[A-Z]/, "Password must contain at least one uppercase letter.")
      .regex(/[a-z]/, "Password must contain at least one lowercase letter.")
      .regex(/[0-9]/, "Password must contain at least one number."),
    password_confirm: z.string().min(1, "Please confirm your password."),
  })
  .refine((data) => data.password === data.password_confirm, {
    message: "Passwords do not match.",
    path: ["password_confirm"],
  });

export const updateProfileSchema = z.object({
  full_name: z
    .string()
    .min(2, "Full name must be at least 2 characters.")
    .trim(),
  phone_number: z
    .string()
    .optional()
    .or(z.literal(""))
    .refine(
      (val) => !val || /^\+?[1-9]\d{9,14}$/.test(val),
      "Invalid phone number format."
    ),
});

export const changePasswordSchema = z
  .object({
    old_password: z.string().min(1, "Current password is required."),
    new_password: z
      .string()
      .min(10, "New password must be at least 10 characters long.")
      .regex(/[A-Z]/, "Must contain an uppercase letter.")
      .regex(/[a-z]/, "Must contain a lowercase letter.")
      .regex(/[0-9]/, "Must contain a number."),
    new_password_confirm: z.string().min(1, "Please confirm your new password."),
  })
  .refine((data) => data.new_password === data.new_password_confirm, {
    message: "New passwords do not match.",
    path: ["new_password_confirm"],
  })
  .refine((data) => data.old_password !== data.new_password, {
    message: "New password cannot be identical to your current password.",
    path: ["new_password"],
  });

export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type UpdateProfileFormData = z.infer<typeof updateProfileSchema>;
export type ChangePasswordFormData = z.infer<typeof changePasswordSchema>;
