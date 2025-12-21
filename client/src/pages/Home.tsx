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
import { Users, Wallet } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

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

  // Re-fetch employees when data changes to get updated balances
  const selectedEmployee = initialized 
    ? employees.find((e) => e.id === selectedEmployeeId) 
    : undefined;

  const filteredExpenses = selectedEmployeeId
    ? expenses.filter((e) => e.employeeId === selectedEmployeeId)
    : expenses;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">جاري التحميل...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col" dir="rtl">
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between px-4">
          <h1 className="text-xl font-bold">نظام إدارة مصروفات الموظفين</h1>
        </div>
      </header>

      <main className="flex-1 container px-4 py-6">
        <div className="space-y-6">
          {/* Employee Selection */}
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div className="flex items-center gap-4">
              <Select
                value={selectedEmployeeId}
                onValueChange={setSelectedEmployeeId}
              >
                <SelectTrigger className="w-[250px]">
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

          {/* Employee Stats */}
          {selectedEmployee && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    الموظف المحدد
                  </CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {selectedEmployee.name}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    {selectedEmployee.role}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    رصيد العهدة
                  </CardTitle>
                  <Wallet className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div
                    className={`text-2xl font-bold ${selectedEmployee.custodyBalance >= 0 ? "text-green-600" : "text-red-600"}`}
                  >
                    {selectedEmployee.custodyBalance.toLocaleString()} ر.س
                  </div>
                  <p className="text-xs text-muted-foreground">
                    الرصيد الحالي للعهدة
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    إجمالي العمليات
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {filteredExpenses.length}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    عدد العمليات المسجلة
                  </p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Expenses Table */}
          <div>
            <h2 className="text-lg font-semibold mb-4">سجل العمليات المالية</h2>
            <ExpensesTable
              expenses={filteredExpenses}
              currentUserId={selectedEmployeeId}
              onUpdate={handleRefresh}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
