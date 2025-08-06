import React from 'react';
import { motion } from 'framer-motion';
import { 
  SparklesIcon
} from '@heroicons/react/24/outline';
import VoiceCommandCenter from '../../components/voice/VoiceCommandCenter';

// Mock data - replace with real API calls
const mockProductivityData = {
  currentScore: 87,
  weeklyChange: 5,
  peakHours: ['9:00-11:00 AM'],
  conflictsResolved: 3,
  voiceEvents: 12,
  meetingEfficiency: 85,
  focusScore: 90
};

const DashboardPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      {/* AI Priority Alert */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-6 text-white"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <SparklesIcon className="h-8 w-8" />
            <div>
              <h3 className="text-lg font-semibold">🤖 AI Priority Alert</h3>
              <p className="text-purple-100">"Meeting with CEO" detected as high priority</p>
              <div className="mt-2 text-sm text-purple-200">
                Priority: 3 → 1⭐Confidence: 94%
              </div>
              <div className="text-xs text-purple-300 mt-1">
                Keywords detected: CEO, quarterly review, strategic planning
              </div>
            </div>
          </div>
          <div className="flex space-x-2">
            <button className="bg-white/20 px-4 py-2 rounded-lg text-sm hover:bg-white/30 transition-colors">
              📋 Review
            </button>
            <button className="bg-white/20 px-4 py-2 rounded-lg text-sm hover:bg-white/30 transition-colors">
              ✅ Accept
            </button>
            <button className="bg-white/20 px-2 py-2 rounded-lg text-sm hover:bg-white/30 transition-colors">
              ✖️
            </button>
          </div>
        </div>
      </motion.div>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Productivity Overview */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                📊 Productivity Overview
              </h2>
              <span className="text-sm text-gray-500">Updated 5 min ago</span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">
                  {mockProductivityData.currentScore}%
                </div>
                <div className="text-sm text-green-600 flex items-center justify-center mt-1">
                  ✅ +{mockProductivityData.weeklyChange}% this week
                </div>
                <div className="text-xs text-gray-500 mt-1">Productivity Score</div>
              </div>

              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {mockProductivityData.peakHours[0]}
                </div>
                <div className="text-xs text-gray-500 mt-1">Peak Hours</div>
              </div>

              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">
                  {mockProductivityData.conflictsResolved}
                </div>
                <div className="text-xs text-gray-500 mt-1">Conflicts Resolved Today</div>
              </div>

              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {mockProductivityData.voiceEvents}
                </div>
                <div className="text-xs text-gray-500 mt-1">Voice Events Today</div>
              </div>
            </div>
          </motion.div>

          {/* Voice Command Center */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <VoiceCommandCenter />
          </motion.div>
        </div>

        {/* Right Column - Sidebar */}
        <div className="space-y-6">
          {/* Mini Calendar */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center justify-between">
              August 2025
              <div className="flex space-x-1">
                <button className="p-1 hover:bg-gray-100 rounded">◀️</button>
                <button className="p-1 hover:bg-gray-100 rounded">▶️</button>
              </div>
            </h3>
            
            <div className="grid grid-cols-7 gap-1 text-center text-xs">
              {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, index) => (
                <div key={`day-${index}`} className="p-2 text-gray-500 font-medium">{day}</div>
              ))}
              {Array.from({length: 31}, (_, i) => (
                <div key={`date-${i}`} className={`p-2 text-sm ${i + 1 === 5 ? 'bg-purple-500 text-white rounded-full' : 'hover:bg-gray-100 rounded'}`}>
                  {i + 1}
                </div>
              ))}
            </div>
          </motion.div>

          {/* Today's Schedule */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              📅 Today's Schedule
            </h3>
            
            <div className="space-y-3">
              <div className="border-l-4 border-yellow-400 pl-3 py-2">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-sm">Team Standup</div>
                    <div className="text-xs text-gray-500">9:00 AM</div>
                    <div className="text-xs text-gray-400">Conference Room A</div>
                  </div>
                  <div className="text-xs">
                    <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded">MEDIUM</span>
                    <div className="text-xs text-purple-600 mt-1">🤖 92%</div>
                  </div>
                </div>
              </div>

              <div className="border-l-4 border-red-400 pl-3 py-2">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-sm">Client Presentation</div>
                    <div className="text-xs text-gray-500">2:00 PM</div>
                    <div className="text-xs text-gray-400">Zoom Meeting</div>
                  </div>
                  <div className="text-xs">
                    <span className="bg-red-100 text-red-800 px-2 py-1 rounded">CRITICAL</span>
                    <div className="text-xs text-purple-600 mt-1">🤖 94%</div>
                  </div>
                </div>
              </div>

              <div className="border-l-4 border-green-400 pl-3 py-2">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-sm">Yoga Class</div>
                    <div className="text-xs text-gray-500">6:00 PM</div>
                  </div>
                  <div className="text-xs">
                    <span className="bg-green-100 text-green-800 px-2 py-1 rounded">VERY LOW</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Smart Scheduling Suggestions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          🧠 AI Scheduling Suggestions
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="border border-blue-200 rounded-lg p-4 bg-blue-50">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-900">Optimal Focus Time</span>
              <span className="text-xs text-blue-600">⭐ 95% match</span>
            </div>
            <p className="text-sm text-blue-800">Block 10:00-12:00 AM for deep work based on your productivity patterns</p>
          </div>
          
          <div className="border border-green-200 rounded-lg p-4 bg-green-50">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-green-900">Meeting Buffer</span>
              <span className="text-xs text-green-600">⭐ 88% recommended</span>
            </div>
            <p className="text-sm text-green-800">Add 15-min buffer between meetings to reduce stress</p>
          </div>
          
          <div className="border border-purple-200 rounded-lg p-4 bg-purple-50">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-purple-900">Priority Reshuffling</span>
              <span className="text-xs text-purple-600">⭐ 92% beneficial</span>
            </div>
            <p className="text-sm text-purple-800">Move "Code Review" to 2:00 PM when you're most analytical</p>
          </div>
        </div>
      </motion.div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
      >
        <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          ⚡ Recent Activity
        </h2>
        
        <div className="space-y-4">
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                Event priority updated by AI
              </p>
              <p className="text-xs text-gray-500">18 min ago</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">
                Voice command processed: "Team meeting tomorrow"
              </p>
              <p className="text-xs text-gray-500">34 min ago</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <div className="flex-1">
              <p className="text-sm text-gray-900">
                Analytics data refreshed
              </p>
              <p className="text-xs text-gray-500">23 min ago</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default DashboardPage;
