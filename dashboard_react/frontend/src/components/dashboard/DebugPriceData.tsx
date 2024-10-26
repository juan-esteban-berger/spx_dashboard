import { Price, FilterOptions } from '@/types/interfaces';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Loader2 } from "lucide-react"; // Import the spinner icon

{/*****************************************************************************/}
{/* Interface Definitions */}

interface DebugPriceDataProps {
  filterOptions: FilterOptions;                  // Available filter options
  selectedTicker: string;                        // Currently selected stock ticker
  setSelectedTicker: (ticker: string) => void;   // Function to update selected ticker
  pricesData: Price[];                          // Price data for selected ticker
  loading?: boolean;                            // Loading state indicator
}

{/*****************************************************************************/}
{/* DebugPriceData Component */}
// Debug component to display and inspect price data for selected stocks
export const DebugPriceData = ({
  filterOptions,
  selectedTicker,
  setSelectedTicker,
  pricesData,
  loading = false // Default to false if not provided
}: DebugPriceDataProps) => {
  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          Debug: Price Data
          {loading && (
            <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Ticker Selection Dropdown */}
        <div className="w-[200px]">
          <Select value={selectedTicker} onValueChange={setSelectedTicker}>
            <SelectTrigger>
              <SelectValue placeholder="Select a symbol..." />
            </SelectTrigger>
            <SelectContent>
              {filterOptions.symbols.map((symbol) => (
                <SelectItem key={symbol} value={symbol}>
                  {symbol}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Price Data Display */}
        <div className="space-y-4 relative">
          {/* Loading Overlay */}
          {loading && (
            <div className="absolute inset-0 bg-background/50 flex items-center justify-center z-50">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          )}

          {/* First Record Preview */}
          <div>
            <h3 className="font-semibold mb-2">First Price Record:</h3>
            {pricesData.length > 0 ? (
              <pre className="bg-gray-100 p-4 rounded-lg overflow-auto">
                {JSON.stringify(pricesData[0], null, 2)}
              </pre>
            ) : (
              <p className="text-gray-500">No price data available</p>
            )}
          </div>
          
          {/* Price Data Table */}
          <div>
            <h3 className="font-semibold mb-2">Price Data Table (First 5 Records):</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full border border-gray-200">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 border">Date</th>
                    <th className="px-4 py-2 border">Ticker</th>
                    <th className="px-4 py-2 border">Metric</th>
                    <th className="px-4 py-2 border">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {pricesData.slice(0, 5).map((price, index) => (
                    <tr key={index}>
                      <td className="px-4 py-2 border">{price.date}</td>
                      <td className="px-4 py-2 border">{price.ticker}</td>
                      <td className="px-4 py-2 border">{price.metric}</td>
                      <td className="px-4 py-2 border">${price.value.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Summary Information */}
          <div>
            <h3 className="font-semibold mb-2">Total Records: {pricesData.length}</h3>
          </div>

          <div>
            <h3 className="font-semibold mb-2">Current Selected Ticker: {selectedTicker || 'None'}</h3>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
