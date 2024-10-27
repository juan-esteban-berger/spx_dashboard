import * as React from "react";
import { useState, useEffect, useRef } from 'react';
import { Price, Financial, FilterOptions } from '@/types/interfaces';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { format, parseISO } from 'date-fns';
import { SearchableSelect } from "@/components/custom/searchable-select";
import { Line, LineChart, CartesianGrid, XAxis, Bar, BarChart, Tooltip, YAxis } from "recharts";
import { ChartContainer } from "@/components/ui/chart";

// Smart unit formatter function
const formatValue = (value: number) => {
  const abs = Math.abs(value);
  if (abs >= 1e12) {
    return `$${(value / 1e12).toFixed(1)}T`;
  } else if (abs >= 1e9) {
    return `$${(value / 1e9).toFixed(1)}B`;
  } else if (abs >= 1e6) {
    return `$${(value / 1e6).toFixed(1)}M`;
  } else if (abs >= 1e3) {
    return `$${(value / 1e3).toFixed(1)}K`;
  }
  return `$${value.toFixed(2)}`;
};

interface CombinedDataSectionProps {
  filterOptions: FilterOptions;
  selectedTicker: string;
  setSelectedTicker: (ticker: string) => void;
  pricesData: Price[];
  financialsData: Financial[];
  loading?: boolean;
}

export const CombinedDataSection = ({
  filterOptions = { symbols: [], sectors: [], subIndustries: [], locations: [], foundedRange: { min: 0, max: 0 } },
  selectedTicker = '',
  setSelectedTicker,
  pricesData = [],
  financialsData = [],
  loading = false
}: CombinedDataSectionProps) => {
  // Default values
  const DEFAULT_METRIC = 'Close';
  const DEFAULT_VARIABLE = 'Total Revenue';

  // State initialization
  const [selectedMetric, setSelectedMetric] = useState({ label: DEFAULT_METRIC, value: DEFAULT_METRIC });
  const [selectedVariable, setSelectedVariable] = useState({ label: DEFAULT_VARIABLE, value: DEFAULT_VARIABLE });
  const [chartRendering, setChartRendering] = useState(false);
  const [dataTransitioning, setDataTransitioning] = useState(false);
  
  // Refs for tracking previous data
  const prevPricesDataRef = useRef(pricesData);
  const prevFinancialsDataRef = useRef(financialsData);
  const transitionTimerRef = useRef<NodeJS.Timeout>();
  const renderTimerRef = useRef<NodeJS.Timeout>();

  // Cleanup function for timers
  useEffect(() => {
    return () => {
      if (transitionTimerRef.current) clearTimeout(transitionTimerRef.current);
      if (renderTimerRef.current) clearTimeout(renderTimerRef.current);
    };
  }, []);

  // Track data changes and manage transition states
  useEffect(() => {
    const pricesChanged = pricesData !== prevPricesDataRef.current;
    const financialsChanged = financialsData !== prevFinancialsDataRef.current;

    if (pricesChanged || financialsChanged) {
      setDataTransitioning(true);
      setChartRendering(true);

      // Update refs
      prevPricesDataRef.current = pricesData;
      prevFinancialsDataRef.current = financialsData;

      // Handle transition timing
      if (transitionTimerRef.current) clearTimeout(transitionTimerRef.current);
      if (renderTimerRef.current) clearTimeout(renderTimerRef.current);

      transitionTimerRef.current = setTimeout(() => {
        setDataTransitioning(false);
        
        renderTimerRef.current = setTimeout(() => {
          setChartRendering(false);
        }, 500);
      }, 750);
    }
  }, [pricesData, financialsData]);

  // Handle loading state changes
  useEffect(() => {
    if (loading) {
      setDataTransitioning(true);
      setChartRendering(true);
    }
  }, [loading]);

  // Initialize default values
  useEffect(() => {
    const metricExists = pricesData.some(p => p.metric === DEFAULT_METRIC);
    if (!metricExists && pricesData.length > 0) {
      const firstMetric = pricesData[0].metric;
      setSelectedMetric({ label: firstMetric, value: firstMetric });
    }

    const variableExists = financialsData.some(f => f.variable === DEFAULT_VARIABLE);
    if (!variableExists && financialsData.length > 0) {
      const firstVariable = financialsData[0].variable;
      setSelectedVariable({ label: firstVariable, value: firstVariable });
    }
  }, [pricesData, financialsData]);

  // Get unique metrics and variables with null checks
  const uniqueMetrics = Array.from(new Set(pricesData?.map(p => p.metric) || []))
    .map(metric => ({ label: metric, value: metric }));
  
  const uniqueVariables = Array.from(new Set(financialsData
    ?.filter(f => f.value !== null)
    .map(f => f.variable) || []))
    .map(variable => ({ label: variable, value: variable }));

  // Chart data preparation
  const pricesChartData = pricesData
    .filter(price => price.metric === selectedMetric.value)
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map(price => ({
      date: price.date,
      displayDate: format(parseISO(price.date), 'MMM yyyy'),
      value: price.value
    }));

  const financialsChartData = financialsData
    .filter(financial => 
      financial.variable === selectedVariable.value && 
      financial.value !== null && 
      !isNaN(financial.value)
    )
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    .map(financial => ({
      date: financial.date,
      displayDate: format(parseISO(financial.date), 'MMM yyyy'),
      value: financial.value
    }));

  const chartConfig = {
    value: {
      label: "Value",
      color: "hsl(var(--chart-1))",
    },
  };

  // Loading state component
  const LoadingSpinner = () => (
    <div className="absolute inset-0 flex items-center justify-center bg-background/50 backdrop-blur-sm">
      <div className="flex flex-col items-center gap-2">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="text-sm text-muted-foreground">
          {loading ? "Loading data..." : 
           dataTransitioning ? "Preparing chart data..." : 
           chartRendering ? "Rendering chart..." : 
           "Updating view..."}
        </span>
      </div>
    </div>
  );

  // Custom tooltip content
  const CustomTooltipContent = ({ active, payload, label }: any) => {
    if (!active || !payload || !payload.length) return null;
    
    return (
      <div className="rounded-lg border bg-background p-2 shadow-sm">
        <div className="text-sm text-muted-foreground">{label}</div>
        <div className="text-sm font-medium">
          {formatValue(payload[0].value)}
        </div>
      </div>
    );
  };

  const isLoading = loading || dataTransitioning || chartRendering;

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          Market Data
          {isLoading && (
            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4 mb-6">
          {/* Symbol Selection */}
          <div>
            <label className="text-sm font-medium mb-1 block">Symbol</label>
            <SearchableSelect
              options={(filterOptions?.symbols || []).map(symbol => ({
                label: symbol,
                value: symbol
              }))}
              value={{ label: selectedTicker, value: selectedTicker }}
              onChange={(option) => setSelectedTicker(option.value)}
              placeholder="Select symbol..."
              className="w-full"
            />
          </div>

          {/* Metric Filter */}
          <div>
            <label className="text-sm font-medium mb-1 block">Price Metric</label>
            <SearchableSelect
              options={uniqueMetrics}
              value={selectedMetric}
              onChange={setSelectedMetric}
              placeholder="Select metric..."
              className="w-full"
            />
          </div>

          {/* Financial Variable Filter */}
          <div>
            <label className="text-sm font-medium mb-1 block">Financial Metric</label>
            <SearchableSelect
              options={uniqueVariables}
              value={selectedVariable}
              onChange={setSelectedVariable}
              placeholder="Select financial metric..."
              className="w-full"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Prices Chart */}
          <Card className="relative">
            <CardHeader>
              <CardTitle>Price History</CardTitle>
              <CardDescription>{selectedMetric.value} Prices</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading && <LoadingSpinner />}
              <ChartContainer config={chartConfig}>
                <LineChart
                  data={pricesChartData}
                  margin={{ top: 10, right: 10, bottom: 20, left: 60 }}
                >
                  <CartesianGrid vertical={false} strokeDasharray="3 3" />
                  <XAxis
                    dataKey="displayDate"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    angle={-45}
                    textAnchor="end"
                    height={60}
                  />
                  <YAxis
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tickFormatter={formatValue}
                  />
                  <Tooltip content={CustomTooltipContent} />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="var(--color-value)"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ChartContainer>
            </CardContent>
          </Card>

          {/* Financials Chart */}
          <Card className="relative">
            <CardHeader>
              <CardTitle>Financial History</CardTitle>
              <CardDescription>
                {selectedVariable.value}
                {financialsChartData.length === 0 && " (No data available)"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isLoading && <LoadingSpinner />}
              <ChartContainer config={chartConfig}>
                {financialsChartData.length > 0 ? (
                  <BarChart
                    data={financialsChartData}
                    margin={{ top: 10, right: 10, bottom: 20, left: 60 }}
                  >
                    <CartesianGrid vertical={false} strokeDasharray="3 3" />
                    <XAxis
                      dataKey="displayDate"
                      tickLine={false}
                      axisLine={false}
                      tickMargin={8}
                      angle={-45}
                      textAnchor="end"
                      height={60}
                    />
                    <YAxis
                      tickLine={false}
                      axisLine={false}
                      tickMargin={8}
                      tickFormatter={formatValue}
                    />
                    <Tooltip content={CustomTooltipContent} />
                    <Bar
                      dataKey="value"
                      fill="var(--color-value)"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                ) : (
                  <div className="flex h-full items-center justify-center text-muted-foreground">
                    No data available for selected metric
                  </div>
                )}
              </ChartContainer>
            </CardContent>
          </Card>
        </div>
      </CardContent>
    </Card>
  );
};

export default CombinedDataSection;
