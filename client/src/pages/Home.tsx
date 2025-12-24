import { AddExpenseDialog } from "@/components/expenses/AddExpenseDialog";
import { ExpensesTable } from "@/components/expenses/ExpensesTable";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { dataService } from "@/lib/data-service";
import { Employee, Expense } from "@/types";
import { Users, Wallet, Clock, CheckCircle2 } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

export default function Home() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [selectedEmployeeId, setSelectedEmployeeId] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [initialized, setInitialized] = useState(false);

  const loadData = useCallback(async () => {
    const [employeesData, expensesData] = await Promise.all([
      dataService.getEmployees(),
      dataService.getExpenses(),
    ]);
    setEmployees(employeesData);
    setExpenses(expensesData);
    return employeesData;
  }, []);

  // Initial data load
  useEffect(() => {
    let isMounted = true;
    
    const initializeData = async () => {
      const employeesData = await loadData();
      if (isMounted) {
        if (employeesData.length > 0) {
          setSelectedEmployeeId(employeesData[0].id);
        }
        setLoading(false);
        setInitialized(true);
      }
    };

    initializeData();

    return () => {
      isMounted = false;
    };
  }, [loadData]);

  // Refresh data handler (for child components)
  const handleRefresh = useCallback(async () => {
    await loadData();
  }, [loadData]);

  // Memoize selected employee to avoid recalculating on every render
  const selectedEmployee = useMemo(() => {
    if (!initialized) return undefined;
    return employees.find((e) => e.id === selectedEmployeeId);
  }, [initialized, employees, selectedEmployeeId]);

  // Memoize filtered expenses to avoid recalculating on every render
  const filteredExpenses = useMemo(() => {
    if (!selectedEmployeeId) return expenses;
    return expenses.filter((e) => e.employeeId === selectedEmployeeId);
  }, [expenses, selectedEmployeeId]);

  // Memoize pending expenses count
  const pendingExpensesCount = useMemo(() => {
    return filteredExpenses.filter((e) => e.status === "pending").length;
  }, [filteredExpenses]);

  // Memoize confirmed (paid) expenses count
  const confirmedExpensesCount = useMemo(() => {
    return filteredExpenses.filter((e) => e.status === "paid").length;
  }, [filteredExpenses]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center" dir="rtl">
        <div className="text-center bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 border">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            جاري تحميل البيانات
          </h2>
          <p className="text-muted-foreground">
            يرجى الانتظار حتى يتم تحميل جميع البيانات...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900" dir="rtl">
      <header className="border-b bg-white dark:bg-gray-800 shadow-sm">
        <div className="container flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Wallet className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              نظام إدارة مصروفات الموظفين
            </h1>
          </div>
          <div className="text-sm text-muted-foreground">
            مرحباً بك في لوحة التحكم
          </div>
        </div>
      </header>

      <main className="flex-1 container px-4 py-8">
        <div className="space-y-8">
          {/* Employee Selection */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border p-6">
            <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-primary" />
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    اختر الموظف:
                  </label>
                </div>
                <Select
                  value={selectedEmployeeId}
                  onValueChange={setSelectedEmployeeId}
                >
                  <SelectTrigger className="w-[280px]">
                    <SelectValue placeholder="اختر الموظف" />
                  </SelectTrigger>
                  <SelectContent>
                    {employees.map((employee) => (
                      <SelectItem key={employee.id} value={employee.id}>
                        {employee.name} - {employee.role}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              {selectedEmployeeId && (
                <AddExpenseDialog
                  employeeId={selectedEmployeeId}
                  onSuccess={handleRefresh}
                />
              )}
            </div>
          </div>

          {/* Employee Stats */}
          {selectedEmployee && (
            <div className="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
              <Card className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-blue-200 dark:border-blue-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                  <CardTitle className="text-sm font-semibold text-blue-900 dark:text-blue-100">
                    الموظف المحدد
                  </CardTitle>
                  <Users className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-900 dark:text-blue-100 mb-1 truncate" title={selectedEmployee.name}>
                    {selectedEmployee.name}
                  </div>
                  <p className="text-sm text-blue-700 dark:text-blue-300 truncate" title={selectedEmployee.role}>
                    {selectedEmployee.role}
                  </p>
                </CardContent>
              </Card>

              <Card className={`bg-gradient-to-br ${selectedEmployee.custodyBalance >= 0 ? 'from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-green-200 dark:border-green-800' : 'from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-red-200 dark:border-red-800'}`}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                  <CardTitle className={`text-sm font-semibold ${selectedEmployee.custodyBalance >= 0 ? 'text-green-900 dark:text-green-100' : 'text-red-900 dark:text-red-100'}`}>
                    رصيد العهدة
                  </CardTitle>
                  <Wallet className={`h-5 w-5 ${selectedEmployee.custodyBalance >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`} />
                </CardHeader>
                <CardContent>
                  <div
                    className={`text-2xl font-bold mb-1 ${selectedEmployee.custodyBalance >= 0 ? 'text-green-900 dark:text-green-100' : 'text-red-900 dark:text-red-100'}`}
                  >
                    {selectedEmployee.custodyBalance.toLocaleString()} ر.س
                  </div>
                  <p className={`text-sm ${selectedEmployee.custodyBalance >= 0 ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'}`}>
                    الرصيد الحالي للعهدة
                  </p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border-purple-200 dark:border-purple-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                  <CardTitle className="text-sm font-semibold text-purple-900 dark:text-purple-100">
                    إجمالي العمليات
                  </CardTitle>
                  <div className="h-5 w-5 rounded-full bg-purple-600 dark:bg-purple-400 flex items-center justify-center">
                    <span className="text-xs font-bold text-white">{filteredExpenses.length}</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-purple-900 dark:text-purple-100 mb-1">
                    {filteredExpenses.length}
                  </div>
                  <p className="text-sm text-purple-700 dark:text-purple-300">
                    عدد العمليات المسجلة
                  </p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-800/20 border-yellow-200 dark:border-yellow-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                  <CardTitle className="text-sm font-semibold text-yellow-900 dark:text-yellow-100">
                    العمليات المعلقة
                  </CardTitle>
                  <Clock className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-yellow-900 dark:text-yellow-100 mb-1">
                    {pendingExpensesCount}
                  </div>
                  <p className="text-sm text-yellow-700 dark:text-yellow-300">
                    بانتظار التأكيد
                  </p>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/20 border-emerald-200 dark:border-emerald-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                  <CardTitle className="text-sm font-semibold text-emerald-900 dark:text-emerald-100">
                    العمليات المكتملة
                  </CardTitle>
                  <CheckCircle2 className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-emerald-900 dark:text-emerald-100 mb-1">
                    {confirmedExpensesCount}
                  </div>
                  <p className="text-sm text-emerald-700 dark:text-emerald-300">
                    تم التأكيد والاكتمال
                  </p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Expenses Table */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border overflow-hidden">
            <div className="p-6 border-b">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <div className="w-6 h-6 bg-primary rounded flex items-center justify-center">
                  <span className="text-xs font-bold text-primary-foreground">📊</span>
                </div>
                سجل العمليات المالية
              </h2>
              <p className="text-sm text-muted-foreground mt-1">
                جميع العمليات المالية المسجلة للموظف المحدد
              </p>
            </div>
            <div className="p-6">
              <ExpensesTable
                expenses={filteredExpenses}
                currentUserId={selectedEmployeeId}
                onUpdate={handleRefresh}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
