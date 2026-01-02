export default function ProgressBar({ current, total }) {
  // Ensure percentage never exceeds 100
  const percentage = total ? Math.min((current / total) * 100, 100) : 0;

  return (
    <div className="w-full mb-6">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-slate-600">
          Question {current} of {total}
        </span>
        <span className="text-sm font-medium text-slate-500">
          {Math.round(percentage)}%
        </span>
      </div>

      <div className="w-full h-2.5 bg-slate-300 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 transition-all duration-500 ease-out rounded-full"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
