"use client"
import * as React from "react"
import { ResponsiveContainer } from "recharts"

export interface ChartConfig {
  [key: string]: {
    label: string
    color: string
  }
}

interface ChartContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
  config: ChartConfig
}

export function ChartContainer({
  children,
  config,
  className,
  ...props
}: ChartContainerProps) {
  React.useEffect(() => {
    const root = document.documentElement
    Object.entries(config).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value.color)
    })
  }, [config])

  return (
    <div {...props} className="h-[400px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        {children}
      </ResponsiveContainer>
    </div>
  )
}

export function ChartTooltip({
  active,
  payload,
  label,
  hideLabel = false,
}: {
  active?: boolean
  payload?: Array<{ value: number }>
  label?: string
  hideLabel?: boolean
}) {
  if (!active || !payload) return null
  return (
    <div className="rounded-md border bg-background p-2 shadow-sm">
      {!hideLabel && <div className="text-sm text-muted-foreground">{label}</div>}
      {payload.map((entry, i) => (
        <div key={i} className="flex items-center gap-2">
          <div className="font-medium">{entry.value.toFixed(2)}</div>
        </div>
      ))}
    </div>
  )
}
