import { dateFormatter } from '@/utils/formatters';

{/*****************************************************************************/}
{/* AG-Grid Column Definitions */}
// Defines the structure and behavior of each column in the company grid
export const infoColumns = [
  // Basic Company Information
  { 
    field: 'symbol',             // Stock symbol
    headerName: 'Symbol', 
    filter: true, 
    sortable: true 
  },
  { 
    field: 'security',           // Company name
    headerName: 'Security', 
    filter: true, 
    sortable: true 
  },
  
  // Industry Classification
  { 
    field: 'gics_sector',        // Industry sector
    headerName: 'Sector', 
    filter: true, 
    sortable: true 
  },
  { 
    field: 'gics_sub_industry',  // Sub-industry category
    headerName: 'Sub Industry', 
    filter: true, 
    sortable: true 
  },
  
  // Additional Company Details
  { 
    field: 'headquarters_location', // Company location
    headerName: 'Location', 
    filter: true, 
    sortable: true 
  },
  { 
    field: 'date_added',         // Date added to S&P 500
    headerName: 'Date Added', 
    filter: true, 
    sortable: true,
    valueFormatter: dateFormatter // Custom date formatting
  },
  { 
    field: 'cik',               // SEC identifier
    headerName: 'CIK', 
    filter: true, 
    sortable: true 
  },
  { 
    field: 'founded',           // Company founding date
    headerName: 'Founded', 
    filter: true, 
    sortable: true 
  }
];
