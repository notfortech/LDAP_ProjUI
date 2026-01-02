import { useState } from "react";
import QuestionCard from "./components/QuestionCard";
import ProgressBar from "./components/ProgressBar";
import LoadingScreen from "./components/LoadingScreen";
import CIFScoreCard from "./components/CIFScoreCard";
import SignalCard from "./components/SignalCard";

const API = "http://localhost:8000";

export default function App() {
  const [state, setState] = useState("initial"); // initial | questions | results | error
  const [questionsData, setQuestionsData] = useState(null);
  const [results, setResults] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [currentAnswer, setCurrentAnswer] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const totalQuestions = questionsData?.questions?.length || 0;
  const currentQuestion = questionsData?.questions?.[currentIndex];

  // -----------------------------
  // Fetch questions
  // -----------------------------
  const fetchQuestions = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/questions?context=education&limit=12`);
      if (!res.ok) throw new Error("Failed to fetch questions");

      const data = await res.json();
      console.log("API response:", data);

      // Flatten questions
      const allQuestions = data.questions.map((q) => ({
        ...q,
        options: Object.entries(q.options).map(([key, label]) => ({
          key,
          label,
        })),
      }));

      setQuestionsData({ questions: allQuestions });
      setState("questions");
      console.log("Normalized questions:", allQuestions);
    } catch (err) {
      console.error("Fetch questions error:", err);
      setState("error");
    } finally {
      setIsLoading(false);
    }
  };

  // -----------------------------
  // Submit evaluation
  // -----------------------------
  const submitEvaluation = async (finalAnswers) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          context: "education",
          responses: finalAnswers,
        }),
      });

      if (!res.ok) throw new Error("Evaluation failed");

      const data = await res.json();
      setResults(data);
      setState("results");
    } catch (err) {
      console.error(err);
      setState("error");
    } finally {
      setIsLoading(false);
    }
  };

  // -----------------------------
  // Navigation handlers
  // -----------------------------
  const handleNext = () => {
    const updatedAnswers = {
      ...answers,
      [currentQuestion.question_id]: currentAnswer,
    };

    setAnswers(updatedAnswers);

    if (currentIndex === totalQuestions - 1) {
      submitEvaluation(updatedAnswers);
    } else {
      const nextIndex = currentIndex + 1;
      setCurrentIndex(nextIndex);
      setCurrentAnswer(
        updatedAnswers[questionsData.questions[nextIndex]?.question_id] || null
      );
    }
  };

  const handleBack = () => {
    if (currentIndex === 0) return;

    const prevIndex = currentIndex - 1;
    const prevQuestionId = questionsData.questions[prevIndex].question_id;

    setCurrentIndex(prevIndex);
    setCurrentAnswer(answers[prevQuestionId] || null);
  };

  const handleRestart = () => {
    setState("initial");
    setCurrentIndex(0);
    setAnswers({});
    setCurrentAnswer(null);
    setQuestionsData(null);
    setResults(null);
  };

  // -----------------------------
  // Loading
  // -----------------------------
  if (isLoading) return <LoadingScreen />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl">

        {/* ---------- INITIAL ---------- */}
        {state === "initial" && (
          <div className="bg-white rounded-3xl shadow-xl p-10 text-center">
            <h1 className="text-4xl font-bold text-slate-900 mb-4">
              Capability Assessment
            </h1>
            <p className="text-slate-700 mb-8">
              A short evaluation to understand readiness and capability signals.
            </p>
            <button
              onClick={fetchQuestions}
              className="bg-slate-900 text-white px-8 py-3 rounded-lg hover:bg-slate-800 shadow-md transition"
            >
              Start Assessment
            </button>
          </div>
        )}

        {/* ---------- QUESTIONS ---------- */}
        {state === "questions" && currentQuestion && (
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <ProgressBar current={currentIndex + 1} total={totalQuestions} />
            <QuestionCard
              question={currentQuestion}
              selectedOption={currentAnswer}
              onSelectOption={setCurrentAnswer}
              onNext={handleNext}
              onBack={handleBack}
              isFirst={currentIndex === 0}
              isLast={currentIndex === totalQuestions - 1}
            />
          </div>
        )}

        {/* ---------- RESULTS ---------- */}
        {state === "results" && results && (
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <CIFScoreCard score={results.cif_score} />

            <div className="mt-6">
              <h2 className="text-2xl font-semibold text-slate-900 mb-4">
                Capability Signals
              </h2>
              <div className="space-y-3">
                {results.signals.map((signal, idx) => (
                  <SignalCard key={idx} signal={signal} />
                ))}
              </div>
            </div>

            <div className="mt-8 text-center">
              <button
                onClick={handleRestart}
                className="bg-slate-900 text-white px-8 py-3 rounded-lg hover:bg-slate-800 shadow-md transition"
              >
                Run Another Assessment
              </button>
            </div>
          </div>
        )}

        {/* ---------- ERROR ---------- */}
        {state === "error" && (
          <div className="bg-white rounded-3xl shadow-xl p-8 text-center">
            <h2 className="text-xl font-semibold mb-3">
              Something went wrong
            </h2>
            <p className="text-slate-600 mb-6">
              Unable to load the assessment.
            </p>
            <button
              onClick={handleRestart}
              className="bg-slate-900 text-white px-6 py-2.5 rounded-lg hover:bg-slate-800 shadow-md transition"
            >
              Retry
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
