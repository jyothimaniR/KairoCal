import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadialBarChart,
  RadialBar,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine
} from 'recharts';

// Color palettes
const COLORS = {
  primary: ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
  pastel: ['#ddd6fe', '#bfdbfe', '#bbf7d0', '#fef3c7', '#fecaca'],
  professional: ['#1f2937', '#374151', '#6b7280', '#9ca3af', '#d1d5db'],
  gradient: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
};

interface BaseChartProps {
  data: any[];
  height?: number;
  className?: string;
  title?: string;
  showLegend?: boolean;
  colorScheme?: keyof typeof COLORS;
}

// Enhanced Line Chart with multiple lines and trend analysis
interface EnhancedLineChartProps extends BaseChartProps {
  lines: Array<{
    dataKey: string;
    name: string;
    color?: string;
    strokeDasharray?: string;
  }>;
  showTrend?: boolean;
  showArea?: boolean;
}

export const EnhancedLineChart: React.FC<EnhancedLineChartProps> = ({
  data,
  lines,
  height = 300,
  className = '',
  showLegend = true,
  showTrend = false,
  showArea = false,
  colorScheme = 'primary'
}) => {
  const colors = COLORS[colorScheme];

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={height}>
        {showArea ? (
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={lines[0]?.dataKey || 'name'} />
            <YAxis />
            <Tooltip />
            {showLegend && <Legend />}
            {lines.map((line, index) => (
              <Area
                key={line.dataKey}
                type="monotone"
                dataKey={line.dataKey}
                stackId={showArea ? "1" : undefined}
                stroke={line.color || colors[index % colors.length]}
                fill={line.color || colors[index % colors.length]}
                fillOpacity={0.6}
                name={line.name}
              />
            ))}
          </AreaChart>
        ) : (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={lines[0]?.dataKey || 'name'} />
            <YAxis />
            <Tooltip />
            {showLegend && <Legend />}
            {lines.map((line, index) => (
              <Line
                key={line.dataKey}
                type="monotone"
                dataKey={line.dataKey}
                stroke={line.color || colors[index % colors.length]}
                strokeWidth={2}
                dot={{ fill: line.color || colors[index % colors.length], strokeWidth: 2, r: 4 }}
                strokeDasharray={line.strokeDasharray}
                name={line.name}
              />
            ))}
            {showTrend && data.length > 1 && (
              <ReferenceLine 
                segment={[
                  { x: data[0]?.name, y: data[0]?.[lines[0]?.dataKey] },
                  { x: data[data.length - 1]?.name, y: data[data.length - 1]?.[lines[0]?.dataKey] }
                ]}
                stroke="#ef4444"
                strokeDasharray="5 5"
              />
            )}
          </LineChart>
        )}
      </ResponsiveContainer>
    </div>
  );
};

// Donut Chart for better proportion visualization
interface DonutChartProps extends BaseChartProps {
  dataKey: string;
  showPercentage?: boolean;
  innerRadius?: number;
  outerRadius?: number;
}

export const DonutChart: React.FC<DonutChartProps> = ({
  data,
  dataKey,
  height = 300,
  className = '',
  showLegend = true,
  showPercentage = true,
  innerRadius = 60,
  outerRadius = 100,
  colorScheme = 'primary'
}) => {
  const colors = COLORS[colorScheme];
  const total = data.reduce((sum, entry) => sum + entry[dataKey], 0);

  const renderLabel = (entry: any) => {
    if (!showPercentage) return '';
    const percentage = ((entry[dataKey] / total) * 100).toFixed(1);
    return `${percentage}%`;
  };

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={innerRadius}
            outerRadius={outerRadius}
            paddingAngle={5}
            dataKey={dataKey}
            label={renderLabel}
            labelLine={false}
          >
            {data.map((_, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={colors[index % colors.length]} 
              />
            ))}
          </Pie>
          <Tooltip formatter={(value) => [value, 'Count']} />
          {showLegend && <Legend />}
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

// Stacked Bar Chart for comparative analysis
interface StackedBarChartProps extends BaseChartProps {
  bars: Array<{
    dataKey: string;
    name: string;
    color?: string;
  }>;
  orientation?: 'vertical' | 'horizontal';
}

export const StackedBarChart: React.FC<StackedBarChartProps> = ({
  data,
  bars,
  height = 300,
  className = '',
  showLegend = true,
  colorScheme = 'primary',
  orientation = 'vertical'
}) => {
  const colors = COLORS[colorScheme];

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} layout={orientation === 'horizontal' ? 'horizontal' : 'vertical'}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type={orientation === 'horizontal' ? 'number' : 'category'} dataKey="name" />
          <YAxis type={orientation === 'horizontal' ? 'category' : 'number'} />
          <Tooltip />
          {showLegend && <Legend />}
          {bars.map((bar, index) => (
            <Bar
              key={bar.dataKey}
              dataKey={bar.dataKey}
              stackId="stack"
              fill={bar.color || colors[index % colors.length]}
              name={bar.name}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// Radial Progress Chart for KPIs
interface RadialProgressProps {
  value: number;
  maxValue?: number;
  label?: string;
  unit?: string;
  size?: 'small' | 'medium' | 'large';
  className?: string;
  colorScheme?: keyof typeof COLORS;
}

export const RadialProgress: React.FC<RadialProgressProps> = ({
  value,
  maxValue = 100,
  label = '',
  unit = '%',
  className = '',
  size = 'medium',
  colorScheme = 'primary'
}) => {
  const colors = COLORS[colorScheme];
  const percentage = (value / maxValue) * 100;
  
  const dimensions = {
    small: { height: 120, innerRadius: 25, outerRadius: 40 },
    medium: { height: 160, innerRadius: 40, outerRadius: 60 },
    large: { height: 200, innerRadius: 60, outerRadius: 80 }
  };

  const { height, innerRadius, outerRadius } = dimensions[size];

  const data = [{ name: 'progress', value: percentage, fill: colors[0] }];

  return (
    <div className={`${className} relative`}>
      <ResponsiveContainer width="100%" height={height}>
        <RadialBarChart 
          cx="50%" 
          cy="50%" 
          innerRadius={innerRadius}
          outerRadius={outerRadius}
          barSize={10}
          data={data}
          startAngle={90}
          endAngle={-270}
        >
          <RadialBar
            dataKey="value"
            cornerRadius={5}
            fill={colors[0]}
          />
        </RadialBarChart>
      </ResponsiveContainer>
      
      {/* Center text */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center">
          <div className={`font-bold text-gray-800 ${
            size === 'small' ? 'text-lg' : size === 'medium' ? 'text-xl' : 'text-2xl'
          }`}>
            {value}{unit}
          </div>
          {label && (
            <div className={`text-gray-500 ${
              size === 'small' ? 'text-xs' : size === 'medium' ? 'text-sm' : 'text-base'
            }`}>
              {label}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Heatmap-style Calendar Chart
interface HeatmapCalendarProps {
  data: Array<{
    date: string;
    value: number;
  }>;
  height?: number;
  className?: string;
}

export const HeatmapCalendar: React.FC<HeatmapCalendarProps> = ({
  data,
  className = ''
}) => {
  const maxValue = Math.max(...data.map(d => d.value));
  
  const getIntensity = (value: number) => {
    const intensity = value / maxValue;
    if (intensity === 0) return 'bg-gray-100';
    if (intensity < 0.25) return 'bg-green-200';
    if (intensity < 0.5) return 'bg-green-300';
    if (intensity < 0.75) return 'bg-green-400';
    return 'bg-green-500';
  };

  // Group data by week (simplified for demo)
  const weeks = Array.from({ length: 12 }, (_, weekIndex) => {
    return Array.from({ length: 7 }, (_, dayIndex) => {
      const dataPoint = data[weekIndex * 7 + dayIndex];
      return dataPoint || { date: '', value: 0 };
    });
  });

  return (
    <div className={`${className} p-4`}>
      <div className="grid grid-cols-12 gap-1">
        {weeks.map((week, weekIndex) => (
          <div key={weekIndex} className="flex flex-col gap-1">
            {week.map((day, dayIndex) => (
              <div
                key={`${weekIndex}-${dayIndex}`}
                className={`w-3 h-3 rounded-sm ${getIntensity(day.value)}`}
                title={`${day.date}: ${day.value} events`}
              />
            ))}
          </div>
        ))}
      </div>
      
      <div className="flex items-center justify-between mt-4 text-xs text-gray-500">
        <span>Less</span>
        <div className="flex gap-1">
          <div className="w-3 h-3 bg-gray-100 rounded-sm" />
          <div className="w-3 h-3 bg-green-200 rounded-sm" />
          <div className="w-3 h-3 bg-green-300 rounded-sm" />
          <div className="w-3 h-3 bg-green-400 rounded-sm" />
          <div className="w-3 h-3 bg-green-500 rounded-sm" />
        </div>
        <span>More</span>
      </div>
    </div>
  );
};

// Scatter Plot for correlation analysis
interface ScatterPlotProps extends BaseChartProps {
  xKey: string;
  yKey: string;
  xLabel?: string;
  yLabel?: string;
  showTrend?: boolean;
}

export const ScatterPlot: React.FC<ScatterPlotProps> = ({
  data,
  xKey,
  yKey,
  height = 300,
  className = '',
  xLabel,
  yLabel,
  showTrend = false,
  colorScheme = 'primary'
}) => {
  const colors = COLORS[colorScheme];

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height={height}>
        <ScatterChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} name={xLabel || xKey} />
          <YAxis dataKey={yKey} name={yLabel || yKey} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter 
            dataKey={yKey} 
            fill={colors[0]}
            fillOpacity={0.7}
          />
          {showTrend && (
            <ReferenceLine 
              stroke="#ef4444"
              strokeDasharray="5 5"
            />
          )}
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default {
  EnhancedLineChart,
  DonutChart,
  StackedBarChart,
  RadialProgress,
  HeatmapCalendar,
  ScatterPlot
};
