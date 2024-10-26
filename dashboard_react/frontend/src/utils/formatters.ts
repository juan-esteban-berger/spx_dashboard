import { format } from 'date-fns';

export const dateFormatter = (params: any) => {
  return params.value ? format(new Date(params.value), 'MM/dd/yyyy') : '';
};

export const currencyFormatter = (value: number | null | undefined) => {
  if (value === null || value === undefined || !isFinite(value)) {
    return 'N/A';
  }
  return `$${value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
};
