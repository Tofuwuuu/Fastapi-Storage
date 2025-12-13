import React, { useEffect, useState, useCallback } from "react";
import Dropzone from "./components/Dropzone";
import "./App.css";

type FileRecord = {
  id: number;
  name: string;
  size: number;
  uploaded_at: string;
  type?: string;
};

export default function App() {
  const [files, setFiles] = useState<FileRecord[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchFiles = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/files");
      const data = await res.json();
      setFiles(data.files || []);
    } catch (err) {
      console.error("Failed to fetch files", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  const handleUploadComplete = () => {
    fetchFiles();
  };

  const handleDownload = (id: number, name: string) => {
    const url = `/api/download/${id}`;
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this file?")) return;
    try {
      await fetch(`/api/files/${id}`, { method: "DELETE" });
      fetchFiles();
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>File Storage</h1>
      </header>

      <main className="container">
        <section className="upload-section">
          <Dropzone onUploadComplete={handleUploadComplete} />
        </section>

        <section className="files-section">
          <h2>Files</h2>
          {loading ? (
            <div>Loading...</div>
          ) : files.length === 0 ? (
            <div className="empty">No files uploaded yet.</div>
          ) : (
            <table className="files-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Size</th>
                  <th>Uploaded</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {files.map((f) => (
                  <tr key={f.id}>
                    <td>{f.name}</td>
                    <td>{(f.size / 1024).toFixed(2)} KB</td>
                    <td>{new Date(f.uploaded_at).toLocaleString()}</td>
                    <td>
                      <button onClick={() => handleDownload(f.id, f.name)}>Download</button>
                      <button onClick={() => handleDelete(f.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  );
}
