import React, { useState, useRef } from "react";
import { UploadCloud, X, Image as ImageIcon } from "lucide-react";
import { cn } from "../../lib/cn";

export interface ImageUploadProps {
  label?: string;
  error?: string;
  onFileSelect: (file: File | null) => void;
  previewUrl?: string | null;
  accept?: string;
  maxSizeMb?: number;
  className?: string;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  label,
  error,
  onFileSelect,
  previewUrl = null,
  accept = "image/png, image/jpeg, image/webp",
  maxSizeMb = 10,
  className,
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [internalPreview, setInternalPreview] = useState<string | null>(previewUrl);
  const [sizeError, setSizeError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    setSizeError(null);
    if (file.size > maxSizeMb * 1024 * 1024) {
      setSizeError(`File size exceeds maximum limit of ${maxSizeMb}MB.`);
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      setInternalPreview(reader.result as string);
    };
    reader.readAsDataURL(file);
    onFileSelect(file);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const clearImage = (e: React.MouseEvent) => {
    e.stopPropagation();
    setInternalPreview(null);
    setSizeError(null);
    if (inputRef.current) inputRef.current.value = "";
    onFileSelect(null);
  };

  const displayError = error || sizeError;

  return (
    <div className={cn("w-full flex flex-col gap-1.5 select-none", className)}>
      {label && (
        <label className="text-sm font-medium text-slate-700 dark:text-slate-300 block">
          {label}
        </label>
      )}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "relative border-2 border-dashed rounded-2xl p-6 flex flex-col items-center justify-center cursor-pointer transition-all min-h-[180px] overflow-hidden",
          dragActive
            ? "border-primary-500 bg-primary-50/50 dark:bg-primary-950/30"
            : "border-slate-300 dark:border-forest-light bg-slate-50/40 dark:bg-forest-medium/30 hover:bg-slate-100/50 dark:hover:bg-forest-medium/50",
          displayError && "border-danger-500 bg-danger-50/20"
        )}
      >
        <input
          ref={inputRef}
          type="file"
          accept={accept}
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              handleFile(e.target.files[0]);
            }
          }}
          className="hidden"
        />

        {internalPreview ? (
          <div className="relative w-full h-full flex flex-col items-center">
            <img
              src={internalPreview}
              alt="Preview"
              className="max-h-48 rounded-xl object-contain shadow-sm"
            />
            <button
              type="button"
              onClick={clearImage}
              className="absolute top-2 right-2 p-1.5 rounded-full bg-slate-900/70 text-white hover:bg-danger-600 transition-colors shadow-md"
              title="Remove image"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center text-center gap-2">
            <div className="p-3 rounded-full bg-slate-200/70 dark:bg-forest-dark text-primary-600 dark:text-primary-400">
              {dragActive ? <UploadCloud className="w-6 h-6 animate-bounce" /> : <ImageIcon className="w-6 h-6" />}
            </div>
            <p className="text-sm font-medium text-slate-700 dark:text-slate-200">
              Click to browse or drag & drop leaf or crop image
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Supports PNG, JPG, WEBP up to {maxSizeMb}MB
            </p>
          </div>
        )}
      </div>
      {displayError && (
        <span className="text-xs text-danger-600 dark:text-danger-400 font-medium animate-fade-in">
          {displayError}
        </span>
      )}
    </div>
  );
};
