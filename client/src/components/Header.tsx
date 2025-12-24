import { Button } from "@/components/ui/button";
import { Moon, Sun, Sparkles, Circle } from "lucide-react";
import { useTheme } from "@/contexts/ThemeContext";

export function Header() {
  const { theme, toggleTheme } = useTheme();

  // Get appropriate icon and label for current theme
  const getThemeIcon = () => {
    switch (theme) {
      case "light":
        return { icon: <Moon className="h-4 w-4" />, label: "تبديل إلى الوضع الداكن" };
      case "dark":
        return { icon: <Sparkles className="h-4 w-4" />, label: "تبديل إلى الوضع الذهبي" };
      case "gold":
        return { icon: <Circle className="h-4 w-4 fill-current" />, label: "تبديل إلى الوضع الأسود" };
      case "black":
        return { icon: <Sun className="h-4 w-4" />, label: "تبديل إلى الوضع الفاتح" };
      default:
        return { icon: <Moon className="h-4 w-4" />, label: "تبديل السمة" };
    }
  };

  const { icon, label } = getThemeIcon();

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
              title={label}
              aria-label={label}
            >
              {icon}
            </Button>
          </nav>
        </div>
      </div>
    </header>
  );
}