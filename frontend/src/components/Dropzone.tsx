import React, { useCallback, useState } from "react";

type Props = {
  onUploadComplete?: () => void;
  uploadUrl?: string;
};

type UploadState = {
  name: string;
  progress: number;
  status: "idle" | "uploading" | "done" | "error";
};

export default function Dropzone({ onUploadComplete, uploadUrl = "/api/upload" }: Props) {
  const [dragActive, setDragActive] = useState(false);
  const [uploads, setUploads] = useState<UploadState[]>([]);

  const uploadFile = (file: File) =>
    new Promise<void>((resolve, reject) => {
      const form = new FormData();
      form.append("files", file);

      const xhr = new XMLHttpRequest();
      xhr.open("POST", uploadUrl, true);

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          setUploads((prev) =>
            prev.map((u) => (u.name === file.name ? { ...u, progress: Math.round((e.loaded / e.total) * 100) } : u))
          );
        }
      };

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          setUploads((prev) => prev.map((u) => (u.name === file.name ? { ...u, status: "done", progress: 100 } : u)));
          resolve();
        } else {
          const errMsg = `Upload failed: ${xhr.status} ${xhr.statusText}`;
          console.error(errMsg, xhr.responseText);
          setUploads((prev) => prev.map((u) => (u.name === file.name ? { ...u, status: "error" } : u)));
          reject(new Error(errMsg));
        }
      };

      xhr.onerror = () => {
        console.error("Network error during upload", xhr.responseText);
        setUploads((prev) => prev.map((u) => (u.name === file.name ? { ...u, status: "error" } : u)));
        reject(new Error("Network error"));
      };

      xhr.onabort = () => {
        console.warn("Upload aborted");
        reject(new Error("Upload aborted"));
      };

      xhr.send(form);
    });

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const fileArray = Array.from(files);
    setUploads((prev) => [...prev, ...fileArray.map((f) => ({ name: f.name, progress: 0, status: "uploading" as const }))]);

    for (const f of fileArray) {
      try {
        await uploadFile(f);
      } catch {
        // ignore individual errors, state already updated
      }
    }

    onUploadComplete?.();
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    handleFiles(e.dataTransfer.files);
  };

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
    e.currentTarget.value = "";
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const onDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  return (
    <div className={`dropzone ${dragActive ? "active" : ""}`} onDrop={onDrop} onDragOver={onDragOver} onDragLeave={onDragLeave}>
      <input id="file-input" className="file-input" type="file" multiple onChange={onInputChange} />
      <label htmlFor="file-input" className="dropzone-label">
        <strong>Drag & drop files here</strong>
        <span>or click to select files</span>
      </label>

      <div className="uploads">
        {uploads.map((u) => (
          <div className="upload-row" key={u.name}>
            <div className="upload-meta">
              <div className="upload-name">{u.name}</div>
              <div className={`upload-status ${u.status}`}>{u.status}</div>
            </div>
            <div className="progress">
              <div className="progress-bar" style={{ width: `${u.progress}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
