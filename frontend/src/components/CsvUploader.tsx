
"use client";

import { useState, useRef } from "react";
import { UploadCloud, CheckCircle, AlertCircle } from "lucide-react";

export default function CsvUploader() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const inputRef = useRef<HTMLInputElement>(null);

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile: File) => {
    if (selectedFile.type !== "text/csv" && !selectedFile.name.endsWith(".csv")) {
      setStatus("error");
      return;
    }
    setFile(selectedFile);
    setStatus("idle");
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");

    // In a real app, you would send this to the backend
    // const formData = new FormData();
    // formData.append("file", file);
    // await fetch('/api/v1/contacts/campaigns/1/upload', { method: 'POST', body: formData });

    setTimeout(() => {
      setStatus("success");
    }, 1500);
  };

  return (
    <div className="w-full">
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center text-center transition-colors
          ${dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:bg-gray-50 bg-white"}
          ${status === "success" ? "border-green-500 bg-green-50" : ""}
          ${status === "error" ? "border-red-500 bg-red-50" : ""}
        `}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          className="hidden"
          onChange={handleChange}
        />

        {status === "success" ? (
          <div className="flex flex-col items-center text-green-700">
            <CheckCircle className="h-10 w-10 mb-2" />
            <p className="font-medium">Upload successful!</p>
            <p className="text-sm mt-1">{file?.name}</p>
            <button onClick={() => { setFile(null); setStatus("idle"); }} className="mt-4 text-sm underline hover:text-green-800">
              Upload another file
            </button>
          </div>
        ) : (
          <>
            <UploadCloud className={`h-10 w-10 mb-3 ${dragActive ? "text-blue-500" : "text-gray-400"}`} />

            {file ? (
              <div className="flex flex-col items-center w-full">
                <p className="text-sm font-medium text-gray-900 truncate max-w-[200px] mb-4">{file.name}</p>
                <button
                  onClick={handleUpload}
                  disabled={status === "uploading"}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {status === "uploading" ? "Uploading..." : "Upload Contacts"}
                </button>
              </div>
            ) : (
              <>
                <p className="text-sm text-gray-700 mb-1">
                  <button onClick={() => inputRef.current?.click()} className="font-semibold text-blue-600 hover:text-blue-500 focus:outline-none underline mr-1">
                    Click to upload
                  </button>
                  or drag and drop
                </p>
                <p className="text-xs text-gray-500">CSV files only (max 10MB)</p>

                {status === "error" && (
                  <p className="mt-2 text-sm text-red-600 flex items-center">
                    <AlertCircle className="h-4 w-4 mr-1" />
                    Please select a valid CSV file.
                  </p>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
}
