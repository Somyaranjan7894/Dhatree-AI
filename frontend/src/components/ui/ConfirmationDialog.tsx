import React from "react";
import { AlertTriangle, Info, CheckCircle2 } from "lucide-react";
import { Modal } from "./Modal";
import { Button } from "./Button";

export interface ConfirmationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void | Promise<void>;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  variant?: "danger" | "warning" | "info" | "success";
  isLoading?: boolean;
}

export const ConfirmationDialog: React.FC<ConfirmationDialogProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  variant = "danger",
  isLoading = false,
}) => {
  const icons = {
    danger: <AlertTriangle className="w-6 h-6 text-danger-600 dark:text-danger-400" />,
    warning: <AlertTriangle className="w-6 h-6 text-warning-600 dark:text-warning-400" />,
    info: <Info className="w-6 h-6 text-primary-600 dark:text-primary-400" />,
    success: <CheckCircle2 className="w-6 h-6 text-success-600 dark:text-success-400" />,
  };

  const bgColors = {
    danger: "bg-danger-50 dark:bg-danger-500/10",
    warning: "bg-warning-50 dark:bg-warning-500/10",
    info: "bg-primary-50 dark:bg-primary-500/10",
    success: "bg-success-50 dark:bg-success-500/10",
  };

  const buttonVariants = {
    danger: "danger" as const,
    warning: "primary" as const,
    info: "primary" as const,
    success: "primary" as const,
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm">
      <div className="flex flex-col items-center text-center py-2">
        <div className={`p-3 rounded-full mb-4 ${bgColors[variant]}`}>
          {icons[variant]}
        </div>
        <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">
          {title}
        </h4>
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
          {message}
        </p>
        <div className="flex items-center gap-3 w-full">
          <Button
            variant="outline"
            className="w-full"
            onClick={onClose}
            disabled={isLoading}
          >
            {cancelLabel}
          </Button>
          <Button
            variant={buttonVariants[variant]}
            className="w-full"
            onClick={onConfirm}
            isLoading={isLoading}
          >
            {confirmLabel}
          </Button>
        </div>
      </div>
    </Modal>
  );
};
