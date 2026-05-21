import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search } from 'lucide-react';

const SearchBar = ({ initialHandle = '' }) => {
  const [handle, setHandle] = useState(initialHandle);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (handle.trim()) {
      navigate(`/dashboard/codeforces/${handle.trim()}`);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="relative group w-full max-w-md mx-auto fade-in"
    >
      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        <Search className="h-5 w-5 text-muted group-focus-within:text-primary transition-colors" />
      </div>
      <input
        type="text"
        value={handle}
        onChange={(e) => setHandle(e.target.value)}
        placeholder="Enter Codeforces handle..."
        className="block w-full pl-12 pr-4 py-4 bg-white/20 backdrop-blur-md border-2 border-white/20 rounded-2xl text-text placeholder-muted focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/40 transition-all shadow-xl hover:shadow-2xl"
        required
        autoFocus
      />
      <button
        type="submit"
        className="absolute right-2 top-2 bottom-2 bg-gradient-to-r from-primary to-secondary hover:from-primary/90 hover:to-secondary/90 text-white font-bold px-7 rounded-xl shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/50"
      >
        Analyze
      </button>
    </form>
  );
};

export default SearchBar;
