export default function CIFScoreCard({ score }) {
  const getBandColor = (band) => {
    switch (band?.toUpperCase()) {
      case 'A':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'B':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'C':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'D':
        return 'bg-red-50 text-red-700 border-red-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-10">
      <div className="flex items-end justify-between gap-8">
        <div>
          <h2 className="text-xs uppercase tracking-wide font-semibold text-slate-500 mb-3">
            Overall Capability Score
          </h2>
          <p className="text-6xl font-light text-slate-900 leading-none">
            {score?.value?.toFixed(1) || '0.0'}
          </p>
          <p className="text-sm text-slate-500 mt-2">out of 5.0</p>
        </div>
        <div className="text-right">
          <p className="text-xs uppercase tracking-wide font-semibold text-slate-500 mb-3">
            Performance Band
          </p>
          <span
            className={`inline-block px-6 py-3 rounded-lg text-base font-semibold border ${getBandColor(
              score?.band
            )}`}
          >
            Band {score?.band || 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
}
