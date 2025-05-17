import {create} from "zustand";
import {persist,createJSONStorage} from "zustand/middleware";


const useMe = create(
  persist(
    (set) => ({
        //state
      me: null,

      //actions
      setMe: (me) => set({me}),
      clearMe: () => set({me: null}),
    }),
    {
      name: "me-storage",
      storage: createJSONStorage(() => localStorage), 
    }
  )
);

export default useMe;