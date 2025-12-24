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
import { AlertCircle, CheckCircle, Users, Wallet } from "lucide-react";
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

  // Count pending expenses that need confirmation
  const pendingExpenses = useMemo(() => {
    return filteredExpenses.filter((e) => e.status === "pending");
  }, [filteredExpenses]);

  // Count confirmed expenses
  const confirmedExpenses = useMemo(() => {
    return filteredExpenses.filter((e) => e.status === "paid" && e.confirmedByEmployee);
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
      <main className="flex-1 container px-3 sm:px-4 lg:px-6 py-4 sm:py-6 lg:py-8">
        <div className="space-y-4 sm:space-y-6 lg:space-y-8">
          {/* Employee Selection */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border p-4 sm:p-6">
            <div className="flex flex-col gap-4">
              <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4">
                <div className="flex items-center gap-2 shrink-0">
                  <Users className="w-5 h-5 text-primary" />
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    اختر الموظف:
                  </label>
                </div>
                <Select
                  value={selectedEmployeeId}
                  onValueChange={setSelectedEmployeeId}
                >
                  <SelectTrigger className="w-full sm:w-[280px]">
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
                <div className="sm:self-end">
                  <AddExpenseDialog
                    employeeId={selectedEmployeeId}
                    onSuccess={handleRefresh}
                  />
                </div>
              )}
            </div>
          </div>

          {/* Employee Stats */}
          {selectedEmployee && (
            <div className="grid gap-3 sm:gap-4 lg:gap-6 grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
              {/* Employee Card */}
              <Card className="col-span-2 sm:col-span-1 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-blue-200 dark:border-blue-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-3 p-3 sm:p-6">
                  <CardTitle className="text-xs sm:text-sm font-semibold text-blue-900 dark:text-blue-100">
                    الموظف المحدد
                  </CardTitle>
                  <Users className="h-4 w-4 sm:h-5 sm:w-5 text-blue-600 dark:text-blue-400" />
                </CardHeader>
                <CardContent className="p-3 sm:p-6 pt-0">
                  <div className="text-lg sm:text-2xl font-bold text-blue-900 dark:text-blue-100 mb-1 truncate">
                    {selectedEmployee.name}
                  </div>
                  <p className="text-xs sm:text-sm text-blue-700 dark:text-blue-300 truncate">
                    {selectedEmployee.role}
                  </p>
                </CardContent>
              </Card>

              {/* Custody Balance Card */}
              <Card className={`bg-gradient-to-br ${selectedEmployee.custodyBalance >= 0 ? 'from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-green-200 dark:border-green-800' : 'from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-red-200 dark:border-red-800'}`}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-3 p-3 sm:p-6">
                  <CardTitle className={`text-xs sm:text-sm font-semibold ${selectedEmployee.custodyBalance >= 0 ? 'text-green-900 dark:text-green-100' : 'text-red-900 dark:text-red-100'}`}>
                    رصيد العهدة
                  </CardTitle>
                  <Wallet className={`h-4 w-4 sm:h-5 sm:w-5 ${selectedEmployee.custodyBalance >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`} />
                </CardHeader>
                <CardContent className="p-3 sm:p-6 pt-0">
                  <div
                    className={`text-lg sm:text-2xl font-bold mb-1 ${selectedEmployee.custodyBalance >= 0 ? 'text-green-900 dark:text-green-100' : 'text-red-900 dark:text-red-100'}`}
                  >
                    {selectedEmployee.custodyBalance.toLocaleString()} <span className="text-xs sm:text-sm">ر.س</span>
                  </div>
                  <p className={`text-xs sm:text-sm ${selectedEmployee.custodyBalance >= 0 ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'}`}>
                    الرصيد الحالي
                  </p>
                </CardContent>
              </Card>

              {/* Pending Confirmation Card */}
              <Card className={`bg-gradient-to-br ${pendingExpenses.length > 0 ? 'from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-800/20 border-yellow-200 dark:border-yellow-800' : 'from-gray-50 to-gray-100 dark:from-gray-900/20 dark:to-gray-800/20 border-gray-200 dark:border-gray-700'}`}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-3 p-3 sm:p-6">
                  <CardTitle className={`text-xs sm:text-sm font-semibold ${pendingExpenses.length > 0 ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-gray-100'}`}>
                    بانتظار التأكيد
                  </CardTitle>
                  <AlertCircle className={`h-4 w-4 sm:h-5 sm:w-5 ${pendingExpenses.length > 0 ? 'text-yellow-600 dark:text-yellow-400 animate-pulse motion-reduce:animate-none' : 'text-gray-400'}`} />
                </CardHeader>
                <CardContent className="p-3 sm:p-6 pt-0">
                  <div className={`text-lg sm:text-2xl font-bold mb-1 ${pendingExpenses.length > 0 ? 'text-yellow-900 dark:text-yellow-100' : 'text-gray-900 dark:text-gray-100'}`}>
                    {pendingExpenses.length}
                  </div>
                  <p className={`text-xs sm:text-sm ${pendingExpenses.length > 0 ? 'text-yellow-700 dark:text-yellow-300' : 'text-gray-500'}`}>
                    {pendingExpenses.length > 0 ? 'تحتاج تأكيد' : 'لا يوجد'}
                  </p>
                </CardContent>
              </Card>

              {/* Confirmed Card */}
              <Card className="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/20 border-emerald-200 dark:border-emerald-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-3 p-3 sm:p-6">
                  <CardTitle className="text-xs sm:text-sm font-semibold text-emerald-900 dark:text-emerald-100">
                    تم التأكيد
                  </CardTitle>
                  <CheckCircle className="h-4 w-4 sm:h-5 sm:w-5 text-emerald-600 dark:text-emerald-400" />
                </CardHeader>
                <CardContent className="p-3 sm:p-6 pt-0">
                  <div className="text-lg sm:text-2xl font-bold text-emerald-900 dark:text-emerald-100 mb-1">
                    {confirmedExpenses.length}
                  </div>
                  <p className="text-xs sm:text-sm text-emerald-700 dark:text-emerald-300">
                    عمليات مؤكدة
                  </p>
                </CardContent>
              </Card>

              {/* Total Operations Card */}
              <Card className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border-purple-200 dark:border-purple-800">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 sm:pb-3 p-3 sm:p-6">
                  <CardTitle className="text-xs sm:text-sm font-semibold text-purple-900 dark:text-purple-100">
                    إجمالي العمليات
                  </CardTitle>
                  <div className="h-4 w-4 sm:h-5 sm:w-5 rounded-full bg-purple-600 dark:bg-purple-400 flex items-center justify-center">
                    <span className="text-[10px] sm:text-xs font-bold text-white">{filteredExpenses.length}</span>
                  </div>
                </CardHeader>
                <CardContent className="p-3 sm:p-6 pt-0">
                  <div className="text-lg sm:text-2xl font-bold text-purple-900 dark:text-purple-100 mb-1">
                    {filteredExpenses.length}
                  </div>
                  <p className="text-xs sm:text-sm text-purple-700 dark:text-purple-300">
                    عملية مسجلة
                  </p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Expenses Table */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border overflow-hidden">
            <div className="p-4 sm:p-6 border-b">
              <h2 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <div className="w-5 h-5 sm:w-6 sm:h-6 bg-primary rounded flex items-center justify-center">
                  <span className="text-[10px] sm:text-xs font-bold text-primary-foreground">📊</span>
                </div>
                سجل العمليات المالية
              </h2>
              <p className="text-xs sm:text-sm text-muted-foreground mt-1">
                جميع العمليات المالية المسجلة للموظف المحدد
              </p>
            </div>
            <div className="p-3 sm:p-6 overflow-x-auto">
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
