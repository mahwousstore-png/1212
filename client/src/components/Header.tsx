import { Button } from "@/components/ui/button";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/contexts/ThemeContext";

export function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 hidden md:flex">
          <a className="mr-6 flex items-center space-x-2" href="/">
            <span className="hidden font-bold sm:inline-block">
              نظام إدارة مصروفات الموظفين
            </span>
          </a>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            {/* يمكن إضافة شريط بحث هنا لاحقاً */}
          </div>
          <nav className="flex items-center">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              title="تبديل السمة"
            >
              {theme === "light" ? (
                <Moon className="h-4 w-4" />
              ) : (
                <Sun className="h-4 w-4" />
              )}
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
}