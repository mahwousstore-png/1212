import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users, DollarSign, FileText, TrendingUp, Plus, Eye } from "lucide-react";
import { Link } from "wouter";

/**
 * لوحة التحكم الرئيسية لنظام إدارة مصروفات الموظفين
 */
export default function Home() {
  // بيانات تجريبية - في التطبيق الحقيقي ستأتي من API
  const stats = {
    totalEmployees: 25,
    totalBalance: 125000,
    pendingExpenses: 8,
    approvedExpenses: 45
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* رأس الصفحة */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">لوحة التحكم</h1>
          <p className="text-muted-foreground">
            مرحباً بك في نظام إدارة مصروفات الموظفين
          </p>
        </div>
        <div className="flex gap-2">
          <Button asChild>
            <Link href="/expenses">
              <Plus className="mr-2 h-4 w-4" />
              إضافة مصروف جديد
            </Link>
          </Button>
          <Button asChild variant="outline">
            <Link href="/expenses">
              <Eye className="mr-2 h-4 w-4" />
              عرض المصروفات
            </Link>
          </Button>
        </div>
      </div>

      {/* إحصائيات سريعة */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">إجمالي الموظفين</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalEmployees}</div>
            <p className="text-xs text-muted-foreground">
              موظف نشط
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">إجمالي الرصيد</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalBalance.toLocaleString()} ر.س</div>
            <p className="text-xs text-muted-foreground">
              الرصيد المتاح
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">مصروفات معلقة</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pendingExpenses}</div>
            <p className="text-xs text-muted-foreground">
              تحتاج موافقة
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">مصروفات مكتملة</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.approvedExpenses}</div>
            <p className="text-xs text-muted-foreground">
              هذا الشهر
            </p>
          </CardContent>
        </Card>
      </div>

      {/* الإجراءات السريعة */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="cursor-pointer hover:shadow-md transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="h-5 w-5" />
              إضافة مصروف جديد
            </CardTitle>
            <CardDescription>
              أضف مصروف أو صرف عهدة جديد للموظف
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link href="/expenses">ابدأ الآن</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5" />
              عرض جميع المصروفات
            </CardTitle>
            <CardDescription>
              استعرض وأدر جميع المصروفات والمعاملات
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="outline" className="w-full">
              <Link href="/expenses">عرض المصروفات</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="cursor-pointer hover:shadow-md transition-shadow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              إدارة الموظفين
            </CardTitle>
            <CardDescription>
              أضف وأدر بيانات الموظفين والأرصدة
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild variant="outline" className="w-full" disabled>
              <span>قريباً</span>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* آخر الأنشطة */}
      <Card>
        <CardHeader>
          <CardTitle>آخر الأنشطة</CardTitle>
          <CardDescription>
            آخر المعاملات والتحديثات في النظام
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">تم تأكيد مصروف للموظف أحمد محمد</p>
                <p className="text-xs text-muted-foreground">منذ 5 دقائق</p>
              </div>
              <Badge variant="secondary">مكتمل</Badge>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">طلب مصروف جديد من فاطمة علي</p>
                <p className="text-xs text-muted-foreground">منذ 15 دقيقة</p>
              </div>
              <Badge variant="outline">معلق</Badge>
            </div>

            <div className="flex items-center gap-4">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <div className="flex-1">
                <p className="text-sm font-medium">تم إضافة موظف جديد: محمد حسن</p>
                <p className="text-xs text-muted-foreground">منذ ساعة</p>
              </div>
              <Badge variant="secondary">معلومات</Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
