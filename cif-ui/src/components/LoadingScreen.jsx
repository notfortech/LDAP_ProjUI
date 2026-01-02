export default function LoadingScreen() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="text-center">
        <div className="w-14 h-14 border-3 border-slate-200 border-t-slate-900 rounded-full animate-spin mx-auto mb-6" />
        <p className="text-slate-500 text-base font-light">Preparing assessment...</p>
      </div>
    </div>
  );
}
