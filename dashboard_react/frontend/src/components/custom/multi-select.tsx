import * as React from "react"
import { useRef, useEffect } from "react"
import { cn } from "@/lib/utils"
import { Check, Search, X } from "lucide-react"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Command, CommandGroup, CommandInput, CommandItem } from "@/components/ui/command"

{/*****************************************************************************/}
{/* Component Interfaces */}

interface Option {
  label: string
  value: string
}

interface MultiSelectProps {
  options: Option[]
  selected: Option[]
  onChange: (options: Option[]) => void
  placeholder?: string
  className?: string
}

{/*****************************************************************************/}
{/* MultiSelect Component */}

export function MultiSelect({
  options,
  selected,
  onChange,
  placeholder = "Select options...",
  className
}: MultiSelectProps) {
  const [open, setOpen] = React.useState(false)
  const [search, setSearch] = React.useState("")
  const containerRef = useRef<HTMLDivElement>(null)

  {/*****************************************************************************/}
  {/* Click Outside Handler */}

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  {/*****************************************************************************/}
  {/* Event Handlers */}

  // Handle toggling of individual options
  const handleToggle = (option: Option) => {
    const isSelected = selected.some(item => item.value === option.value)
    if (isSelected) {
      onChange(selected.filter(item => item.value !== option.value))
    } else {
      onChange([...selected, option])
    }
  }

  // Handle clearing all selections
  const clearSelections = (e: React.MouseEvent) => {
    e.stopPropagation()
    onChange([])
    setSearch("")
  }

  // Remove individual selection
  const removeSelection = (optionToRemove: Option) => {
    onChange(selected.filter(item => item.value !== optionToRemove.value))
  }

  // Filter options based on search
  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(search.toLowerCase())
  )

  {/*****************************************************************************/}
  {/* Component Render */}

  return (
    <div 
      ref={containerRef}
      className="relative" 
      onKeyDown={(e) => {
        if (e.key === "Escape") setOpen(false)
      }}
    >
      <div
        onClick={() => setOpen(!open)}
        className={cn(
          "flex min-h-[2.5rem] w-full items-center justify-between rounded-md border border-input bg-transparent px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
      >
        <div className="flex flex-wrap gap-1">
          {selected.length === 0 && (
            <span className="text-muted-foreground">{placeholder}</span>
          )}
          {selected.map((option) => (
            <div
              key={option.value}
              className="flex items-center gap-1 rounded-md bg-secondary px-1 py-0.5"
            >
              <span className="text-sm">{option.label}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  removeSelection(option)
                }}
                className="ml-1 rounded-sm hover:bg-secondary-foreground/20"
              >
                <X className="h-3 w-3" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {open && (
        <div className="absolute z-50 mt-1 w-full rounded-md border bg-popover text-popover-foreground shadow-md outline-none animate-in">
          <div className="flex items-center border-b px-3">
            <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
            <input
              placeholder="Search..."
              className="flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onClick={(e) => e.stopPropagation()} // Prevent dropdown from closing when clicking the search input
            />
          </div>
          {selected.length > 0 && (
            <div className="border-b px-2 py-1.5">
              <button
                onClick={clearSelections}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Clear all {selected.length} selected items
              </button>
            </div>
          )}
          <div className="max-h-[300px] overflow-auto">
            {filteredOptions.length === 0 ? (
              <p className="p-2 text-sm text-center text-muted-foreground">No results found</p>
            ) : (
              filteredOptions.map((option) => {
                const isSelected = selected.some(item => item.value === option.value)
                return (
                  <div
                    key={option.value}
                    onClick={(e) => {
                      e.stopPropagation() // Prevent dropdown from closing when selecting an option
                      handleToggle(option)
                    }}
                    className={cn(
                      "flex cursor-pointer items-center gap-2 px-2 py-1.5 hover:bg-accent",
                      isSelected && "bg-accent"
                    )}
                  >
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 border rounded flex items-center justify-center">
                        {isSelected && <Check className="w-3 h-3" />}
                      </div>
                      <span>{option.label}</span>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </div>
      )}
    </div>
  )
}
