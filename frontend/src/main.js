import React, { useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "./main.css"; // Ensure the correct path to your CSS file
import { FaPaperclip, FaTrash } from "react-icons/fa"; // Import paperclip and trash icons

function Main() {
    const [field1, setField1] = useState("");
    const [field2, setField2] = useState("");
    const [suggestion, setSuggestion] = useState(""); // New state for suggestion input
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [file1, setFile1] = useState(null);
    const [file2, setFile2] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!field1 && !file1) {
            setError("Please provide text or upload a file for Field 1!");
            return;
        }

        if (!field2 && !file2) {
            setError("Please provide text or upload a file for Instruction!");
            return;
        }

        const fileFormatValid1 = file1
            ? /\.(txt|pdf|doc|docx|html|json)$/i.test(file1.name)
            : true;
        const fileFormatValid2 = file2
            ? /\.(txt|pdf|doc|docx|html|json)$/i.test(file2.name)
            : true;

        if (!fileFormatValid1) {
            setError(
                "Wrong file format for Field 1. Allowed files: .txt, .pdf, .doc, .docx"
            );
            return;
        }

        if (!fileFormatValid2) {
            setError(
                "Wrong file format for Instruction. Allowed files: .txt, .pdf, .doc, .docx"
            );
            return;
        }

        setLoading(true);
        setError("");

        const formData = new FormData();
        if (file1) {
            formData.append("file1", file1);
        }
        if (file2) {
            formData.append("file2", file2);
        }
        formData.append("text", field1);
        formData.append("standard", field2);

        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/api/data",
                formData
            );
            console.log("Response:", response.data);

            setResult(response.data);
            setField1("");
            setField2("");
            setFile1(null);
            setFile2(null);
        } catch (error) {
            console.error(
                "Error:",
                error.response ? error.response.data : error.message
            );
            setError("An error occurred while submitting the data.");
        } finally {
            setLoading(false);
        }
    };

    const adjustTextareaHeight = (e) => {
        e.target.style.height = "auto";
        e.target.style.height = `${e.target.scrollHeight}px`;
    };

    const handleFileChange1 = (e) => {
        const selectedFile = e.target.files[0]; // This function remains unchanged
        if (selectedFile) {
            setFile1(selectedFile);
            setField1(selectedFile.name);
        }
    };

    const handleFileChange2 = (e) => {
        const selectedFile = e.target.files[0]; // This function remains unchanged
        if (selectedFile) {
            setFile2(selectedFile);
            setField2(selectedFile.name);
        }
    };

    const handleNewRequest = () => {
        // Reset all relevant states
        setField1("");
        setField2("");
        setSuggestion(""); // Reset suggestion input
        setFile1(null);
        setFile2(null);
        setResult(null);
        setError("");
    };

    const resetFileInput1 = () => {
        setFile1(null);
        setField1("");
    };

    const resetFileInput2 = () => {
        setFile2(null);
        setField2("");
    };

    const refreshIframe = () => {
        const iframe = document.getElementById("myIframe");
        iframe.src = iframe.src;
    };

    const handleSuggestionSubmit = async () => {
        if (!suggestion) {
            setError("Please provide a suggestion!");
            return;
        }

        setLoading(true);
        setError("");

        const formData = new FormData();
        formData.append("suggestion", suggestion); // Add suggestion to form data

        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/api/new",
                formData
            );
            console.log("Suggestion Response:", response.data);
            setSuggestion(""); // Reset suggestion input
            refreshIframe();
        } catch (error) {
            console.error(
                "Error:",
                error.response ? error.response.data : error.message
            );
            setError("An error occurred while submitting the suggestion.");
        } finally {
            setLoading(false);
        }
    };

    if (result) {
        return (
            <div className="container mt-5">
                <iframe
                    id="myIframe"
                    src="http://127.0.0.1:5000/html"
                    width="100%"
                    height="900px"
                ></iframe>
                <h1>Content Overview</h1>
                <div>
                    <h2>The provided document is</h2>
                    <p>{result["The provided document is"]}</p>
                </div>
                <div>
                    <h2>Overall score</h2>
                    <p>{result["Overall score"]}</p>
                </div>

                <div>
                    <h2>Recommendations for Autofill Suggestions</h2>
                    <pre>
                        {result["Recommendations for Autofill Suggestions"]}
                    </pre>
                </div>
                <div>
                    <h2>Conclusion</h2>
                    <p>{result.Conclusion}</p>
                </div>
                {/* Suggestion Field */}
                <div className="form-group mb-4">
                    <label htmlFor="suggestion">Suggestion:</label>
                    <textarea
                        id="suggestion"
                        value={suggestion}
                        onChange={(e) => {
                            setSuggestion(e.target.value);
                            adjustTextareaHeight(e);
                        }}
                        className="form-control rounded-input"
                        rows="1"
                        placeholder="Type your suggestion here..."
                        style={{ resize: "none" }}
                    />
                </div>
                {/* Submit Suggestion Button */}
                <button
                    className="btn btn-primary button-spacing"
                    onClick={handleSuggestionSubmit}
                    disabled={loading}
                >
                    {loading ? "Submitting..." : "Submit Suggestion"}
                </button>
                {/* New Request Button */}
                <button
                    className="btn btn-secondary button-spacing"
                    onClick={handleNewRequest}
                >
                    New Request
                </button>
            </div>
        );
    }

    return (
        <div className="container mt-5">
            <form onSubmit={handleSubmit}>
                {/* Field 1 for File or Text input */}
                <div className="form-group mb-4">
                    <label htmlFor="field1">Upload File or Enter Text:</label>
                    <div className="input-group position-relative">
                        {file1 ? (
                            <>
                                <span className="form-control rounded-file-display">
                                    {file1.name}
                                </span>
                                <div className="input-group-append">
                                    <button
                                        type="button"
                                        className="btn btn-danger rounded-button"
                                        onClick={resetFileInput1}
                                    >
                                        <FaTrash />
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                <textarea
                                    id="field1"
                                    value={field1}
                                    onChange={(e) => {
                                        setField1(e.target.value);
                                        adjustTextareaHeight(e);
                                    }}
                                    className="form-control rounded-input"
                                    rows="1"
                                    placeholder="Type your text or select a file..."
                                    style={{ resize: "none" }}
                                />
                                <label
                                    className="input-group-text rounded-icon-label"
                                    htmlFor="fileInput1"
                                    style={{
                                        cursor: "pointer",
                                        position: "absolute",
                                        right: "0px",
                                        bottom: "-2px",
                                    }}
                                >
                                    <FaPaperclip />
                                </label>
                                <input
                                    type="file"
                                    id="fileInput1"
                                    onChange={handleFileChange1}
                                    className="d-none"
                                    accept=".txt,.pdf,.doc,.docx,.html"
                                />
                            </>
                        )}
                    </div>
                </div>

                {/* Field 2 for Instructions */}
                <div className="form-group mb-4">
                    <label htmlFor="field2">Instructions:</label>
                    <div className="input-group position-relative">
                        {file2 ? (
                            <>
                                <span className="form-control rounded-file-display">
                                    {file2.name}
                                </span>
                                <div className="input-group-append">
                                    <button
                                        type="button"
                                        className="btn btn-danger rounded-button"
                                        onClick={resetFileInput2}
                                    >
                                        <FaTrash />
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                <textarea
                                    id="field2"
                                    value={field2}
                                    onChange={(e) => {
                                        setField2(e.target.value);
                                        adjustTextareaHeight(e);
                                    }}
                                    className="form-control rounded-input"
                                    rows="1"
                                    placeholder="Type your instructions or select a file..."
                                    style={{ resize: "none" }}
                                />
                                <label
                                    className="input-group-text rounded-icon-label"
                                    htmlFor="fileInput2"
                                    style={{
                                        cursor: "pointer",
                                        position: "absolute",
                                        right: "0px",
                                        bottom: "-2px",
                                    }}
                                >
                                    <FaPaperclip />
                                </label>
                                <input
                                    type="file"
                                    id="fileInput2"
                                    onChange={handleFileChange2}
                                    className="d-none"
                                    accept=".txt,.pdf,.doc,.docx,.html"
                                />
                            </>
                        )}
                    </div>
                </div>

                <button
                    type="submit"
                    className="btn btn-primary btn-block rounded-button"
                    disabled={loading}
                >
                    {loading ? "Submitting..." : "Submit"}
                </button>
            </form>
            {error && <div className="alert alert-danger mt-3">{error}</div>}
        </div>
    );
}

export default Main;
