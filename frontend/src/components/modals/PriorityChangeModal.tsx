import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface PriorityLevel {
  level: number;
  label: string;
  description: string;
  color: string;
  bgColor: string;
  emoji: string;
}

interface PriorityChangeModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentPriority: number;
  eventTitle: string;
  onSave: (newPriority: number) => Promise<boolean>;
}

const PRIORITY_LEVELS: PriorityLevel[] = [
  {
    level: 5,
    label: 'CRITICAL',
    description: 'Urgent, high-impact tasks that require immediate attention',
    color: 'text-red-700',
    bgColor: 'bg-red-100 border-red-200',
    emoji: '🚨'
  },
  {
    level: 4,
    label: 'HIGH',
    description: 'Important, time-sensitive tasks with significant impact',
    color: 'text-orange-700',
    bgColor: 'bg-orange-100 border-orange-200',
    emoji: '⚡'
  },
  {
    level: 3,
    label: 'MEDIUM',
    description: 'Regular work items with moderate importance',
    color: 'text-blue-700',
    bgColor: 'bg-blue-100 border-blue-200',
    emoji: '📝'
  },
  {
    level: 2,
    label: 'LOW',
    description: 'Flexible tasks that can be delayed if needed',
    color: 'text-green-700',
    bgColor: 'bg-green-100 border-green-200',
    emoji: '🟢'
  },
  {
    level: 1,
    label: 'VERY LOW',
    description: 'Social, optional activities with minimal business impact',
    color: 'text-gray-700',
    bgColor: 'bg-gray-100 border-gray-200',
    emoji: '⭕'
  }
];

export const PriorityChangeModal: React.FC<PriorityChangeModalProps> = ({
  isOpen,
  onClose,
  currentPriority,
  eventTitle,
  onSave
}) => {
  const [selectedPriority, setSelectedPriority] = useState(currentPriority);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    if (selectedPriority === currentPriority) {
      onClose();
      return;
    }

    setIsSaving(true);
    setError(null);

    try {
      const success = await onSave(selectedPriority);
      if (success) {
        onClose();
      } else {
        setError('Failed to update priority. Please try again.');
      }
    } catch (err) {
      setError('An error occurred while updating priority.');
    } finally {
      setIsSaving(false);
    }
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="bg-white rounded-xl shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto"
        >
          {/* Header */}
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                Change Event Priority
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 transition-colors"
                title="Close modal"
              >
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
            <p className="text-sm text-gray-600 mt-1 truncate">
              {eventTitle}
            </p>
          </div>

          {/* Content */}
          <div className="px-6 py-4">
            <div className="space-y-3">
              {PRIORITY_LEVELS.map((priority) => (
                <motion.div
                  key={priority.level}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`
                    border-2 rounded-lg p-4 cursor-pointer transition-all
                    ${selectedPriority === priority.level
                      ? `${priority.bgColor} border-current shadow-sm`
                      : 'bg-white border-gray-200 hover:border-gray-300'
                    }
                  `}
                  onClick={() => setSelectedPriority(priority.level)}
                >
                  <div className="flex items-start space-x-3">
                    <span className="text-2xl" role="img" aria-label={priority.label}>
                      {priority.emoji}
                    </span>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-gray-900">
                          Priority {priority.level} - {priority.label}
                        </span>
                        {currentPriority === priority.level && (
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                            Current
                          </span>
                        )}
                        {selectedPriority === priority.level && selectedPriority !== currentPriority && (
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                            Selected
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {priority.description}
                      </p>
                    </div>
                    <div className="flex-shrink-0">
                      <div className={`w-4 h-4 rounded-full border-2 transition-all ${
                        selectedPriority === priority.level
                          ? 'bg-blue-600 border-blue-600'
                          : 'border-gray-300'
                      }`}>
                        {selectedPriority === priority.level && (
                          <div className="w-full h-full rounded-full bg-white scale-50"></div>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg"
              >
                <p className="text-sm text-red-700">{error}</p>
              </motion.div>
            )}
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-200">
            <div className="flex items-center justify-end space-x-3">
              <button
                onClick={onClose}
                disabled={isSaving}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
              >
                {isSaving && (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                )}
                <span>{isSaving ? 'Saving...' : 'Update Priority'}</span>
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
