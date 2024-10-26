import { Company } from '@/types/interfaces';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

{/*****************************************************************************/}
{/* Interface Definitions */}

interface StatsCardsProps {
  companies: Company[]  // Array of company data to display statistics for
}

{/*****************************************************************************/}
{/* StatsCards Component */}
// Displays overview statistics about the companies in a grid of cards
export const StatsCards = ({ companies }: StatsCardsProps) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Total Companies Card */}
      <Card>
        <CardHeader>
          <CardTitle>Total Companies</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{companies.length}</p>
        </CardContent>
      </Card>

      {/* Unique Sectors Card */}
      <Card>
        <CardHeader>
          <CardTitle>Unique Sectors</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">
            {new Set(companies.map(item => item.gics_sector)).size}
          </p>
        </CardContent>
      </Card>

      {/* Unique Sub-Industries Card */}
      <Card>
        <CardHeader>
          <CardTitle>Unique Sub-Industries</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">
            {new Set(companies.map(item => item.gics_sub_industry)).size}
          </p>
        </CardContent>
      </Card>
    </div>
  );
};
