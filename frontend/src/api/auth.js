
export const registerUser = async (userData) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    console.log("Error response:", response)
    throw new Error("Failed to register user",response.status);
  }
  const data = await response.json();
  return data
}

