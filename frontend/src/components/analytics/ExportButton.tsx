import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowDownTrayIcon,
  DocumentArrowDownIcon,
  PhotoIcon,
  DocumentIcon,
  TableCellsIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline';
import { exportAnalytics, prepareChartDataForCSV, formatAnalyticsForExport } from '../../utils/exportUtils';

interface ExportButtonProps {
  data?: any;
  chartData?: any[];
  chartType?: string;
  elementId?: string;
  fileName?: string;
  title?: string;
  className?: string;
  variant?: 'full' | 'minimal';
}

const ExportButton: React.FC<ExportButtonProps> = ({
  data,
  chartData,
  chartType,
  elementId,
  fileName = 'kairocal-analytics',
  title = 'Analytics Data',
  className = '',
  variant = 'full'
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportStatus, setExportStatus] = useState<string | null>(null);

  const exportOptions = [
    {
      type: 'csv' as const,
      label: 'CSV Spreadsheet',
      icon: TableCellsIcon,
      description: 'Export data as CSV file',
      available: Boolean(chartData && chartType)
    },
    {
      type: 'json' as const,
      label: 'JSON Data',
      icon: DocumentIcon,
      description: 'Export complete analytics data',
      available: Boolean(data)
    },
    {
      type: 'png' as const,
      label: 'PNG Image',
      icon: PhotoIcon,
      description: 'Save chart as image',
      available: Boolean(elementId)
    },
    {
      type: 'pdf' as const,
      label: 'PDF Report',
      icon: DocumentArrowDownIcon,
      description: 'Generate PDF report',
      available: Boolean(elementId)
    }
  ];

  const handleExport = async (type: 'csv' | 'json' | 'png' | 'pdf') => {
    setIsExporting(true);
    setExportStatus(null);

    try {
      let exportData;
      
      switch (type) {
        case 'csv':
          if (chartData && chartType) {
            exportData = prepareChartDataForCSV(chartData, chartType);
          } else {
            throw new Error('No chart data available for CSV export');
          }
          break;
        
        case 'json':
          if (data) {
            exportData = formatAnalyticsForExport(data);
          } else {
            throw new Error('No data available for JSON export');
          }
          break;
        
        default:
          exportData = data;
      }

      const success = await exportAnalytics({
        fileName,
        data: exportData,
        type,
        elementId,
        chartTitle: title
      });

      if (success) {
        setExportStatus(`Successfully exported as ${type.toUpperCase()}`);
        setTimeout(() => setExportStatus(null), 3000);
      } else {
        setExportStatus('Export failed. Please try again.');
      }
    } catch (error) {
      console.error('Export error:', error);
      setExportStatus('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
      setIsOpen(false);
    }
  };

  const availableOptions = exportOptions.filter(option => option.available);

  if (availableOptions.length === 0) {
    return null;
  }

  if (variant === 'minimal') {
    return (
      <div className={`relative ${className}`}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          disabled={isExporting}
          className="flex items-center space-x-2 px-2 py-1 text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded transition-colors"
        >
          <ArrowDownTrayIcon className="h-3 w-3" />
          <span>Export</span>
        </button>

        <AnimatePresence>
          {isOpen && (
            <>
              {/* Backdrop */}
              <div 
                className="fixed inset-0 z-40" 
                onClick={() => setIsOpen(false)}
              />
              
              {/* Menu */}
              <motion.div
                initial={{ opacity: 0, scale: 0.95, y: -10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: -10 }}
                className="absolute right-0 top-8 z-50 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-1"
              >
                {availableOptions.map((option) => {
                  const Icon = option.icon;
                  return (
                    <button
                      key={option.type}
                      onClick={() => handleExport(option.type)}
                      disabled={isExporting}
                      className="w-full flex items-center px-3 py-2 text-xs text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
                    >
                      <Icon className="h-3 w-3 mr-2 text-gray-400" />
                      <span>{option.label}</span>
                    </button>
                  );
                })}
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isExporting}
        className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <ArrowDownTrayIcon className={`h-4 w-4 ${isExporting ? 'animate-pulse' : ''}`} />
        <span>{isExporting ? 'Exporting...' : 'Export'}</span>
        <ChevronDownIcon className="h-4 w-4" />
      </button>

      {/* Export Status */}
      {exportStatus && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute top-12 right-0 bg-green-50 border border-green-200 text-green-700 px-3 py-2 rounded-lg text-sm whitespace-nowrap z-50"
        >
          {exportStatus}
        </motion.div>
      )}

      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <div 
              className="fixed inset-0 z-40" 
              onClick={() => setIsOpen(false)}
            />
            
            {/* Export Menu */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -10 }}
              className="absolute right-0 top-12 z-50 w-64 bg-white border border-gray-200 rounded-lg shadow-lg py-2"
            >
              <div className="px-4 py-2 border-b border-gray-100">
                <h4 className="text-sm font-medium text-gray-900">Export Options</h4>
                <p className="text-xs text-gray-500">Choose your preferred format</p>
              </div>

              <div className="py-1">
                {availableOptions.map((option) => {
                  const Icon = option.icon;
                  return (
                    <button
                      key={option.type}
                      onClick={() => handleExport(option.type)}
                      disabled={isExporting}
                      className="w-full flex items-center px-4 py-3 text-left hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <div className="flex-shrink-0">
                        <Icon className="h-5 w-5 text-gray-400" />
                      </div>
                      <div className="ml-3">
                        <div className="text-sm font-medium text-gray-900">
                          {option.label}
                        </div>
                        <div className="text-xs text-gray-500">
                          {option.description}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>

              {availableOptions.length === 0 && (
                <div className="px-4 py-3 text-center text-sm text-gray-500">
                  No export options available
                </div>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ExportButton;
