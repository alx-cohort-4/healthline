import axios from "axios"


export const registerUser = async (userData) => {
    console.log("Sending signup payload:", userData);
    console.log("🚀 ~ registerUser ~ VITE_API_URL:", import.meta.env.VITE_API_URL)


  const API_URL = import.meta.env.VITE_API_URL;

  if (!API_URL) {
    throw new Error("API base URL is not defined! Check your .env file.");
  }
  const response = await fetch(`${API_URL}/signup/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    let errorMessage = "Failed to register user";
    let responseText;
    
    try {
      responseText = await response.text();  
      const errorData = JSON.parse(responseText);
      errorMessage = errorData.message || errorMessage;
    } catch (err) {
        const errMsg = err instanceof Error ? err.message : "Failed to parse error response";
        console.error("Error parsing response:", errMsg);
      console.error("Non-JSON error response:", responseText); 
    }
  
    throw new Error(errorMessage);
  }
  const data = await response.json();
  return data
}

export const verifyUser = (token) => {
    console.log("Sending verify payload:", token);  
    const response = axios.get(
        `${import.meta.env.VITE_API_URL}/verify-email/?token=${token}/`,
    ).then((response) => {
        console.log("🚀 ~ verifyUser ~ response:", response);
        return response
    }).catch((error) => {
        console.error("Error verifying user:", error);
        throw new Error(error.response.data.message || "Failed to verify user");
    });
    return response
}

