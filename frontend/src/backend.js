import React, { useEffect, useState } from "react";
import axios from "axios";

function Backend() {
    const [message, setMessage] = useState("");

    useEffect(() => {
        // Making GET request to Flask API
        axios
            .get("http://127.0.0.1:5000/api/data")
            .then((response) => {
                setMessage(response.data.message); // Update state with the message from Flask
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
            });
    }, []);

    return (
        <div>
            <h1>Message from Flask: {message}</h1>
        </div>
    );
}

export default Backend;
