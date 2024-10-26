import * as React from "react"
import * as SelectPrimitive from "@radix-ui/react-select"
import { cn } from "@/lib/utils"
import { Check } from "lucide-react"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

{/*****************************************************************************/}
{/* Component Interfaces */}

// Single option structure for the select
interface Option {
  label: string  // Display text
  value: string  // Unique identifier
}

// Props for the MultiSelect component
interface MultiSelectProps {
  options: Option[]                      // Array of all possible options
  selected: Option[]                     // Currently selected options
  onChange: (options: Option[]) => void  // Handler for selection changes
  placeholder?: string                   // Optional placeholder text
  className?: string                     // Optional CSS classes
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
  {/*****************************************************************************/}
  {/* Event Handlers */}

  // Handles the selection/deselection of individual options
  const handleSelect = (value: string) => {
    // Find the selected option in the options array
    const option = options.find(opt => opt.value === value);
    if (!option) return;

    // Check if option is already selected
    const isSelected = selected.some(
      selectedOption => selectedOption.value === option.value
    );

    // If selected, remove it; if not selected, add it
    if (isSelected) {
      onChange(selected.filter(opt => opt.value !== option.value));
    } else {
      onChange([...selected, option]);
    }
  };

  // Handles clearing all selections
  const clearSelections = (e: React.MouseEvent) => {
    e.stopPropagation();  // Prevent event bubbling
    onChange([]);         // Clear all selections
  };

  {/*****************************************************************************/}
  {/* Component Render */}

  return (
    <div className="relative">
      {/* Main Select Component */}
      <Select
        value={selected.map(opt => opt.value).join(",")}
        onValueChange={handleSelect}
      >
        {/* Select Trigger Button */}
        <SelectTrigger className={cn("w-full", className)}>
          <SelectValue placeholder={placeholder}>
            {/* Show placeholder or number of selected items */}
            {selected.length === 0
              ? placeholder
              : `${selected.length} selected`}
          </SelectValue>
        </SelectTrigger>

        {/* Dropdown Content */}
        <SelectContent>
          {/* Clear All Button - Only shown when items are selected */}
          {selected.length > 0 && (
            <div className="p-2 flex justify-end border-b">
              <button
                onClick={clearSelections}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Clear all
              </button>
            </div>
          )}

          {/* Options List */}
          <SelectGroup>
            {options.map((option) => (
              <SelectItem
                key={option.value}
                value={option.value}
                className="flex items-center gap-2"
              >
                {/* Option with Checkbox */}
                <div className="flex items-center gap-2">
                  {/* Custom Checkbox */}
                  <div className="w-4 h-4 border rounded flex items-center justify-center">
                    {selected.some(opt => opt.value === option.value) && (
                      <Check className="w-3 h-3" />
                    )}
                  </div>
                  {/* Option Label */}
                  {option.label}
                </div>
              </SelectItem>
            ))}
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>
  );
}
