import { create } from 'zustand';
import localforage from 'localforage';

interface DraftProduct {
  id: string;
  name: string;
  price: number;
  mrp: number;
  stock: number;
  description?: string;
  category?: string;
  createdAt: string;
}

interface OfflineState {
  draftProducts: DraftProduct[];
  isOnline: boolean;
  addDraft: (product: Omit<DraftProduct, 'id' | 'createdAt'>) => void;
  removeDraft: (id: string) => void;
  getDrafts: () => Promise<void>;
  setOnline: (online: boolean) => void;
}

export const useOfflineStore = create<OfflineState>((set, get) => ({
  draftProducts: [],
  isOnline: navigator.onLine,
  
  addDraft: async (product) => {
    const draft: DraftProduct = {
      ...product,
      id: Date.now().toString(),
      createdAt: new Date().toISOString(),
    };
    
    const drafts = [...get().draftProducts, draft];
    set({ draftProducts: drafts });
    await localforage.setItem('draftProducts', drafts);
  },
  
  removeDraft: async (id) => {
    const drafts = get().draftProducts.filter(d => d.id !== id);
    set({ draftProducts: drafts });
    await localforage.setItem('draftProducts', drafts);
  },
  
  getDrafts: async () => {
    const drafts = await localforage.getItem<DraftProduct[]>('draftProducts');
    if (drafts) {
      set({ draftProducts: drafts });
    }
  },
  
  setOnline: (online) => set({ isOnline: online }),
}));

window.addEventListener('online', () => useOfflineStore.getState().setOnline(true));
window.addEventListener('offline', () => useOfflineStore.getState().setOnline(false));
