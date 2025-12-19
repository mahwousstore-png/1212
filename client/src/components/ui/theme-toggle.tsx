import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useTheme } from "@/contexts/ThemeContext";
import { PaletteIcon } from "lucide-react";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const themes = [
    { value: "light", label: "فاتح", icon: "☀️" },
    { value: "dark", label: "مظلم", icon: "🌙" },
    { value: "gold", label: "ذهبي", icon: "✨" },
    { value: "black", label: "أسود", icon: "🌑" },
  ] as const;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="icon" className="relative">
          <PaletteIcon className="h-4 w-4" />
          <span className="sr-only">تغيير الثيم</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-40">
        {themes.map((themeOption) => (
          <DropdownMenuItem
            key={themeOption.value}
            onClick={() => setTheme?.(themeOption.value)}
            className={`flex items-center gap-2 ${
              theme === themeOption.value ? "bg-accent" : ""
            }`}
          >
            <span className="text-lg">{themeOption.icon}</span>
            <span>{themeOption.label}</span>
            {theme === themeOption.value && (
              <span className="ml-auto text-xs">✓</span>
            )}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}