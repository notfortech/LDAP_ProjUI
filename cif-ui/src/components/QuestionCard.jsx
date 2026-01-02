export default function QuestionCard({
  question,
  selectedOption,
  onSelectOption,
  onNext,
  onBack,
  isFirst,
  isLast,
}) {
  return (
    <div className="w-full">
      <div className="mb-8">
        {question.situation_title && (
          <h2 className="text-2xl font-semibold text-slate-900 mb-2">
            {question.situation_title}
          </h2>
        )}

        {question.background && (
          <p className="text-slate-600 text-base mb-4">
            {question.background}
          </p>
        )}

        <p className="text-slate-700 text-lg mb-4 font-light">{question.text}</p>
      </div>

    <div className="space-y-3 mb-6">
        {question.options.map((option) => (
        <button
            key={option.key}
            onClick={() => {
                console.log("Selected:", option.key);
                onSelectOption(option.key)}
            } 
            className={`w-full text-left p-4 rounded-xl border transition-all duration-200 ${
            selectedOption === option.key
                ? "border-slate-700 bg-slate-50 shadow-sm"
                : "border-slate-200 hover:border-slate-400 bg-white hover:shadow-sm"
            }`}
        >
            <span className="text-slate-800 text-base font-medium">
            {option.label}
            </span>
        </button>
    ))}
    </div>

      <div className="flex justify-between items-center">
        <button
          onClick={onBack}
          disabled={isFirst}
          className={`px-6 py-2.5 rounded-lg font-medium transition-all duration-150 ${
            isFirst
              ? "text-slate-300 cursor-not-allowed"
              : "text-slate-600 hover:bg-slate-100 hover:text-slate-700"
          }`}
        >
          Back
        </button>

        <button
          onClick={onNext}
          disabled={!selectedOption}
          className={`px-8 py-2.5 rounded-lg font-medium transition-all duration-150 ${
            selectedOption
              ? "bg-slate-900 text-white hover:bg-slate-800 shadow-md hover:shadow-lg"
              : "bg-slate-200 text-slate-400 cursor-not-allowed"
          }`}
        >
          {isLast ? "Submit Assessment" : "Next Question"}
        </button>
      </div>
    </div>
  );
}
