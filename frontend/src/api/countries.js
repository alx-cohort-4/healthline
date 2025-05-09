

export const fetchCountries = async ()=> {
	try {
		const response = await fetch(
			"https://restcountries.com/v3.1/all?fields=name,flags,cca2,cca3"
		);
		if (!response.ok) {
			throw new Error("Failed to fetch countries");
		}
		const data = await response.json();
		return data.sort((a, b) => a.name.common.localeCompare(b.name.common));
	} catch (error) {
		console.error("Error fetching countries:", error);
		throw error;
	}
}