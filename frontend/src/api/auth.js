import axios from "axios"


export const registerUser = async (userData) => {
    console.log("Sending signup payload:", userData)
  const API_URL = import.meta.env.VITE_API_URL;

  if (!API_URL) {
    throw new Error("API base URL is not defined! Check your .env file.");
  }
  try{
    const response = await fetch(`${API_URL}/signup/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });
    if (!response.ok) {
     console.log("🚀 ~ registerUser ~ response:", response)
      throw new Error("Failed to register user");
    }
  
    const data = await response.json();
    return data
  }catch(err){
    console.error("Error registering user:", err);
    throw new Error(err.response.data.details || "Failed to register user");
  }

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

