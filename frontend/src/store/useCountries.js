import {create } from "zustand"

const useCountriesStore = create((set) => ({
    countries: [],
    setCountries : (countries) => set({ countries }), 
}));
export default useCountriesStore;