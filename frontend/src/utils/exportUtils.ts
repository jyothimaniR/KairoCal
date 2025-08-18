import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import Papa from 'papaparse';
import { saveAs } from 'file-saver';

export interface ExportData {
  fileName: string;
  data: any;
  type: 'csv' | 'json' | 'png' | 'pdf';
  elementId?: string;
  chartTitle?: string;
}

// Export data as CSV
export const exportToCSV = (data: any[], fileName: string) => {
  try {
    const csv = Papa.unparse(data);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `${fileName}.csv`);
    return true;
  } catch (error) {
    console.error('Error exporting CSV:', error);
    return false;
  }
};

// Export data as JSON
export const exportToJSON = (data: any, fileName: string) => {
  try {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json;charset=utf-8;' });
    saveAs(blob, `${fileName}.json`);
    return true;
  } catch (error) {
    console.error('Error exporting JSON:', error);
    return false;
  }
};

// Export chart/element as PNG
export const exportToPNG = async (elementId: string, fileName: string, options?: {
  backgroundColor?: string;
  scale?: number;
  quality?: number;
}) => {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      throw new Error(`Element with id "${elementId}" not found`);
    }

    const canvas = await html2canvas(element, {
      backgroundColor: options?.backgroundColor || '#ffffff',
      scale: options?.scale || 2,
      logging: false,
      useCORS: true,
      allowTaint: false
    });

    canvas.toBlob((blob) => {
      if (blob) {
        saveAs(blob, `${fileName}.png`);
      }
    }, 'image/png', options?.quality || 0.95);

    return true;
  } catch (error) {
    console.error('Error exporting PNG:', error);
    return false;
  }
};

// Export as PDF with chart embedded
export const exportToPDF = async (elementId: string, fileName: string, options?: {
  title?: string;
  orientation?: 'portrait' | 'landscape';
  format?: string;
}) => {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      throw new Error(`Element with id "${elementId}" not found`);
    }

    const canvas = await html2canvas(element, {
      backgroundColor: '#ffffff',
      scale: 2,
      logging: false,
      useCORS: true,
      allowTaint: false
    });

    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF({
      orientation: options?.orientation || 'landscape',
      unit: 'mm',
      format: options?.format || 'a4'
    });

    // Add title if provided
    if (options?.title) {
      pdf.setFontSize(16);
      pdf.text(options.title, 20, 20);
    }

    // Calculate image dimensions to fit PDF
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();
    const imgWidth = canvas.width;
    const imgHeight = canvas.height;
    
    const ratio = Math.min(
      (pdfWidth - 40) / imgWidth, 
      (pdfHeight - (options?.title ? 50 : 30)) / imgHeight
    );
    
    const scaledWidth = imgWidth * ratio;
    const scaledHeight = imgHeight * ratio;
    
    const x = (pdfWidth - scaledWidth) / 2;
    const y = options?.title ? 30 : 20;

    pdf.addImage(imgData, 'PNG', x, y, scaledWidth, scaledHeight);
    pdf.save(`${fileName}.pdf`);

    return true;
  } catch (error) {
    console.error('Error exporting PDF:', error);
    return false;
  }
};

// Comprehensive export function that handles multiple formats
export const exportAnalytics = async ({
  fileName,
  data,
  type,
  elementId,
  chartTitle
}: ExportData): Promise<boolean> => {
  const timestamp = new Date().toISOString().split('T')[0];
  const fullFileName = `${fileName}_${timestamp}`;

  switch (type) {
    case 'csv':
      return exportToCSV(data, fullFileName);
    
    case 'json':
      return exportToJSON(data, fullFileName);
    
    case 'png':
      if (!elementId) {
        console.error('Element ID required for PNG export');
        return false;
      }
      return await exportToPNG(elementId, fullFileName);
    
    case 'pdf':
      if (!elementId) {
        console.error('Element ID required for PDF export');
        return false;
      }
      return await exportToPDF(elementId, fullFileName, {
        title: chartTitle || 'KairoCal Analytics Report',
        orientation: 'landscape'
      });
    
    default:
      console.error(`Unsupported export type: ${type}`);
      return false;
  }
};

// Format analytics data for export
export const formatAnalyticsForExport = (analyticsData: any) => {
  const exportData: any = {};

  // Priority Trends
  if (analyticsData.priorityTrends?.trends) {
    exportData.priorityTrends = analyticsData.priorityTrends.trends.map((trend: any) => ({
      period: trend.period,
      totalEvents: trend.total_events,
      highPriorityPercentage: trend.high_priority_percentage,
      criticalEvents: trend.critical_events,
      priorityDistribution: trend.priority_distribution
    }));
  }

  // BERT Performance
  if (analyticsData.bertPerformance) {
    exportData.bertPerformance = {
      classificationOverview: analyticsData.bertPerformance.classification_overview,
      recommendations: analyticsData.bertPerformance.recommendations,
      methodDistribution: analyticsData.bertPerformance.classification_overview?.method_distribution
    };
  }

  // Productivity Metrics
  if (analyticsData.productivityMetrics?.metrics) {
    exportData.productivityMetrics = {
      overallScore: analyticsData.productivityMetrics.metrics.overall_score,
      components: analyticsData.productivityMetrics.metrics.components,
      patterns: analyticsData.productivityMetrics.metrics.patterns,
      insights: analyticsData.productivityMetrics.metrics.insights
    };
  }

  // Summary
  exportData.summary = {
    exportDate: new Date().toISOString(),
    totalEvents: analyticsData.priorityTrends?.insights?.total_events_analyzed || 0,
    highPriorityRate: analyticsData.priorityTrends?.insights?.high_priority_rate || 0,
    bertAdoptionRate: analyticsData.bertPerformance?.classification_overview?.bert_adoption_rate || 0,
    productivityScore: analyticsData.productivityMetrics?.metrics?.overall_score || 0
  };

  return exportData;
};

// Convert chart data to CSV-friendly format
export const prepareChartDataForCSV = (chartData: any[], chartType: string) => {
  switch (chartType) {
    case 'priority':
      return chartData.map(item => ({
        Priority: item.label,
        Count: item.count,
        Percentage: item.percentage,
        Level: item.priority
      }));

    case 'productivity':
      return chartData.map(item => ({
        Component: item.name,
        Score: item.value,
        Description: `${item.name} component score`
      }));

    case 'timeSeries':
      return chartData.map(item => ({
        Period: item.period,
        'Total Events': item.totalEvents,
        'High Priority %': item.highPriority,
        'Critical Events': item.critical
      }));

    case 'hourlyProductivity':
      return chartData.map(item => ({
        Hour: item.hour,
        'Productivity Score': item.score,
        'Time Period': `${item.hour} - ${parseInt(item.hour.split(':')[0]) + 1}:00`
      }));

    default:
      return chartData;
  }
};
