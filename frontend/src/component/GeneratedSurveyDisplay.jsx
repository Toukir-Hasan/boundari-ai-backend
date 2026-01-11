import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * GeneratedSurveyDisplay - A professional component to display AI-generated survey
 * Shows the survey in a beautiful, user-friendly card format
 */
const GeneratedSurveyDisplay = ({ survey, onClose, onUseSurvey }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!survey) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      >
        <motion.div
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold mb-2">✨ AI Generated Survey</h2>
                <p className="text-indigo-100 text-sm">
                  Your survey has been created successfully!
                </p>
              </div>
              <button
                onClick={onClose}
                className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition-all"
                title="Close"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="overflow-y-auto max-h-[calc(90vh-200px)] p-6">
            {/* Survey Title */}
            <div className="mb-6 p-4 bg-indigo-50 rounded-lg border-l-4 border-indigo-600">
              <h3 className="text-lg font-semibold text-gray-800 mb-1">
                Survey Title
              </h3>
              <p className="text-gray-700 text-xl font-medium">{survey.title}</p>
            </div>

            {/* Questions Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <span className="bg-indigo-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-2">
                  {survey.questions?.length || 0}
                </span>
                Questions Generated
              </h3>

              {survey.questions?.map((question, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow"
                >
                  {/* Question Header */}
                  <div className="flex items-start mb-3">
                    <span className="bg-purple-100 text-purple-700 font-semibold rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">
                      {index + 1}
                    </span>
                    <div className="flex-1">
                      <p className="text-gray-800 font-medium text-base">
                        {question.text}
                      </p>
                      <span className="inline-block mt-2 px-3 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700">
                        {question.type === "multiple_choice" && "Multiple Choice"}
                        {question.type === "rating" && "Rating Scale"}
                        {question.type === "open_text" && "Open Text"}
                      </span>
                    </div>
                  </div>

                  {/* Question Details */}
                  {question.type === "multiple_choice" && question.options && (
                    <div className="ml-11 mt-3 space-y-2">
                      <p className="text-sm font-medium text-gray-600 mb-2">
                        Options:
                      </p>
                      {question.options.map((option, optIndex) => (
                        <div
                          key={optIndex}
                          className="flex items-center p-2 bg-gray-50 rounded-lg"
                        >
                          <div className="w-4 h-4 rounded-full border-2 border-gray-400 mr-3"></div>
                          <span className="text-gray-700">{option}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {question.type === "rating" && question.scale && (
                    <div className="ml-11 mt-3">
                      <p className="text-sm font-medium text-gray-600 mb-2">
                        Rating Scale: 1 to {question.scale}
                      </p>
                      <div className="flex gap-2">
                        {[...Array(question.scale)].map((_, i) => (
                          <div
                            key={i}
                            className="w-10 h-10 flex items-center justify-center bg-indigo-100 text-indigo-700 font-semibold rounded-lg"
                          >
                            {i + 1}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {question.type === "open_text" && (
                    <div className="ml-11 mt-3">
                      <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <p className="text-sm text-gray-500 italic">
                          Open-ended text response
                        </p>
                      </div>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>

            {/* Raw JSON Toggle (for developers) */}
            <div className="mt-6">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="text-sm text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-2"
              >
                {isExpanded ? "Hide" : "Show"} Raw JSON
                <svg
                  className={`w-4 h-4 transition-transform ${
                    isExpanded ? "rotate-180" : ""
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>
              {isExpanded && (
                <motion.pre
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  className="mt-3 p-4 bg-gray-900 text-green-400 rounded-lg overflow-x-auto text-xs"
                >
                  {JSON.stringify(survey, null, 2)}
                </motion.pre>
              )}
            </div>
          </div>

          {/* Footer Actions */}
          <div className="bg-gray-50 px-6 py-4 flex justify-end gap-3 border-t">
            <button
              onClick={onClose}
              className="px-5 py-2.5 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 font-medium transition-colors"
            >
              Close
            </button>
            <button
              onClick={() => {
                // Copy JSON to clipboard
                navigator.clipboard.writeText(JSON.stringify(survey, null, 2));
                alert("Survey JSON copied to clipboard!");
              }}
              className="px-5 py-2.5 rounded-lg bg-purple-600 text-white hover:bg-purple-700 font-medium transition-colors"
            >
              Copy JSON
            </button>
            {onUseSurvey && (
              <button
                onClick={() => onUseSurvey(survey)}
                className="px-5 py-2.5 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 font-medium transition-colors shadow-md"
              >
                Use This Survey
              </button>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default GeneratedSurveyDisplay;
