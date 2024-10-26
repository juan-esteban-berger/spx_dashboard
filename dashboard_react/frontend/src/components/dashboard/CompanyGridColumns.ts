import { dateFormatter } from '@/utils/formatters';
import { ColDef } from 'ag-grid-community';

export const infoColumns: ColDef[] = [
  { 
    field: 'symbol',
    headerName: 'Symbol',
    sortable: true,
    width: 120,
    suppressMovable: true
  },
  { 
    field: 'security',
    headerName: 'Security',
    sortable: true,
    flex: 1,
    suppressMovable: true
  },
  { 
    field: 'gics_sector',
    headerName: 'Sector',
    sortable: true,
    width: 160,
    suppressMovable: true
  },
  { 
    field: 'gics_sub_industry',
    headerName: 'Sub Industry',
    sortable: true,
    width: 200,
    suppressMovable: true
  },
  { 
    field: 'headquarters_location',
    headerName: 'Location',
    sortable: true,
    width: 150,
    suppressMovable: true
  },
  { 
    field: 'date_added',
    headerName: 'Date Added',
    sortable: true,
    width: 150,
    valueFormatter: dateFormatter,
    suppressMovable: true
  },
  { 
    field: 'cik',
    headerName: 'CIK',
    sortable: true,
    width: 120,
    suppressMovable: true
  },
  { 
    field: 'founded',
    headerName: 'Founded',
    sortable: true,
    width: 120,
    suppressMovable: true
  }
];
