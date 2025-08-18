// Simple user store using localStorage for demo purposes
interface UserData {
  full_name: string;
  email: string;
  account_status: 'active' | 'inactive';
}

const USER_STORAGE_KEY = 'kairocal-user-data';

const defaultUser: UserData = {
  full_name: 'John Doe',
  email: 'john.doe@example.com',
  account_status: 'active'
};

export const userService = {
  getUser(): UserData {
    try {
      const stored = localStorage.getItem(USER_STORAGE_KEY);
      if (stored) {
        return { ...defaultUser, ...JSON.parse(stored) };
      }
      return defaultUser;
    } catch {
      return defaultUser;
    }
  },

  updateUser(updates: Partial<UserData>): UserData {
    try {
      const current = this.getUser();
      const updated = { ...current, ...updates };
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(updated));
      
      // Dispatch custom event to notify components
      window.dispatchEvent(new CustomEvent('user-updated', { 
        detail: updated 
      }));
      
      return updated;
    } catch {
      return this.getUser();
    }
  },

  clearUser(): void {
    try {
      localStorage.removeItem(USER_STORAGE_KEY);
      window.dispatchEvent(new CustomEvent('user-updated', { 
        detail: defaultUser 
      }));
    } catch {
      // Ignore errors
    }
  }
};
