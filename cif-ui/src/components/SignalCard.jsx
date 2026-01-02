export default function SignalCard({ signal }) {
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
    <div className="border border-slate-200 rounded-xl p-6 bg-white hover:shadow-md transition-shadow duration-200">
      <div className="flex justify-between items-start mb-4 gap-4">
        <p className="text-slate-700 text-base leading-relaxed flex-1">
          {signal?.description}
        </p>

        <span
          className={`inline-block px-3 py-1.5 rounded-md text-xs font-semibold border whitespace-nowrap ${getBandColor(
            signal?.band
          )}`}
        >
          Band {signal?.band}
        </span>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex-1">
          <div className="h-1.5 bg-slate-150 rounded-full overflow-hidden">
            <div
              className="h-full bg-slate-900 transition-all duration-500 rounded-full"
              style={{ width: `${((signal?.score || 0) / 5) * 100}%` }}
            />
          </div>
        </div>

        <span className="text-sm font-semibold text-slate-700 w-14 text-right">
          {(signal?.score || 0).toFixed(1)}
        </span>
      </div>
    </div>
  );
}
