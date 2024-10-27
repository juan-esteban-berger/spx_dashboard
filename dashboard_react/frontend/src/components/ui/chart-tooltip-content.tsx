"use client"
import { cn } from "@/lib/utils"

interface ChartTooltipContentProps {
  active?: boolean
  payload?: Array<{ value: number; name: string }>
  label?: string
  hideLabel?: boolean
  prefix?: string
  className?: string
}

export function ChartTooltipContent({
  active,
  payload,
  label,
  hideLabel = false,
  prefix = "",
  className,
}: ChartTooltipContentProps) {
  if (!active || !payload) return null

  return (
    <div
      className={cn(
        "rounded-lg border bg-background p-2 shadow-sm",
        className
      )}
    >
      {!hideLabel && (
        <div className="text-xs text-muted-foreground">{label}</div>
      )}
      {payload.map((item, index) => (
        <div key={index} className="text-sm font-medium">
          {prefix}
          {typeof item.value === 'number' 
            ? item.value.toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })
            : item.value}
        </div>
      ))}
    </div>
  )
}
