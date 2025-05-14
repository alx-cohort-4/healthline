import { useEffect, useState } from "react";
import { fetchCountries } from "../api/countries";
import  useCountriesStore  from "../store/useCountries";

export const useCountries = () => {
	const {countries, setCountries} = useCountriesStore();
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		const loadCountries = async () => {
			try {
				const data = await fetchCountries();
				console.log("🔍 ~ loadCountries ~ data:", data)
				
				const preferredLayout = data.map((country) => {
					return {
						label: country.name.common,
						value: country.cca2,
					};
				});
				setCountries(preferredLayout);
			} catch (err) {
				setError(
					err instanceof Error ? err.message : "Failed to fetch countries"
				);
			} finally {
				setLoading(false);
			}
		};

		loadCountries();
	}, [countries, setCountries]);

	return { countries, loading, error };
};