import * as React from "react";
import { useState, useEffect } from 'react';
import { Price, Financial, FilterOptions } from '@/types/interfaces';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";
import { currencyFormatter } from '@/utils/formatters';
import { format } from 'date-fns';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface CombinedDataSectionProps {
  filterOptions: FilterOptions;
  selectedTicker: string;
  setSelectedTicker: (ticker: string) => void;
  pricesData: Price[];
  financialsData: Financial[];
  loading?: boolean;
}

export const CombinedDataSection = ({
  filterOptions,
  selectedTicker,
  setSelectedTicker,
  pricesData,
  financialsData,
  loading = false
}: CombinedDataSectionProps) => {
  // Set initial default values
  const [selectedMetric, setSelectedMetric] = useState<string>('Close');
  const [selectedVariable, setSelectedVariable] = useState<string>('Total Revenue');

  // Set initial values when component mounts
  useEffect(() => {
    if (!selectedTicker) {
      setSelectedTicker('AAPL');
    }
  }, []);

  // Get unique metrics from prices data
  const uniqueMetrics = Array.from(new Set(pricesData.map(p => p.metric)));

  // Get unique variables from financials data
  const uniqueVariables = Array.from(new Set(financialsData.map(f => f.variable)));

  // Filter data based on selected filters
  const filteredPricesData = pricesData.filter(price => 
    price.metric === selectedMetric
  ).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  const filteredFinancialsData = financialsData.filter(financial => 
    financial.variable === selectedVariable
  ).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          Market Data
          {loading && (
            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Filters Section */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          {/* Symbol Selection */}
          <div>
            <label className="text-sm font-medium mb-1 block">Symbol</label>
            <Select
              value={selectedTicker || 'AAPL'}
              onValueChange={setSelectedTicker}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select symbol" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  {filterOptions.symbols.map((symbol) => (
                    <SelectItem key={symbol} value={symbol}>
                      {symbol}
                    </SelectItem>
                  ))}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          {/* Metric Filter */}
          <div>
            <label className="text-sm font-medium mb-1 block">Price Metric</label>
            <Select
              value={selectedMetric}
              onValueChange={setSelectedMetric}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select metric" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  {uniqueMetrics.map((metric) => (
                    <SelectItem key={metric} value={metric}>
                      {metric}
                    </SelectItem>
                  ))}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          {/* Financial Variable Filter */}
          <div>
            <label className="text-sm font-medium mb-1 block">Financial Metric</label>
            <Select
              value={selectedVariable}
              onValueChange={setSelectedVariable}
            >
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select financial metric" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  {uniqueVariables.map((variable) => (
                    <SelectItem key={variable} value={variable}>
                      {variable}
                    </SelectItem>
                  ))}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Data Display */}
        <div className="grid grid-cols-2 gap-6">
          {/* Prices Section */}
          <div className="space-y-4">
            <h3 className="font-semibold text-lg">Price Data</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-200">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 border">Date</th>
                    <th className="px-4 py-2 border">Metric</th>
                    <th className="px-4 py-2 border">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPricesData.slice(0, 10).map((price, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 border">{format(new Date(price.date), 'yyyy-MM-dd')}</td>
                      <td className="px-4 py-2 border">{price.metric}</td>
                      <td className="px-4 py-2 border">${price.value.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="text-sm text-gray-500">
              Showing {Math.min(10, filteredPricesData.length)} of {filteredPricesData.length} records
            </p>
          </div>

          {/* Financials Section */}
          <div className="space-y-4">
            <h3 className="font-semibold text-lg">Financial Data</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-200">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 border">Date</th>
                    <th className="px-4 py-2 border">Variable</th>
                    <th className="px-4 py-2 border">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFinancialsData.slice(0, 10).map((financial, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 border">{format(new Date(financial.date), 'yyyy-MM-dd')}</td>
                      <td className="px-4 py-2 border">{financial.variable}</td>
                      <td className="px-4 py-2 border">{currencyFormatter(financial.value)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="text-sm text-gray-500">
              Showing {Math.min(10, filteredFinancialsData.length)} of {filteredFinancialsData.length} records
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CombinedDataSection;
