import { AddExpenseDialog } from "@/components/expenses/AddExpenseDialog";
import { ExpensesTable } from "@/components/expenses/ExpensesTable";
import { dataService } from "@/lib/data-service";
import { Expense } from "@/types";
import { useEffect, useState } from "react";

export default function TestExpenses() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [loading, setLoading] = useState(true);

  const loadExpenses = async () => {
    setLoading(true);
    const data = await dataService.getExpenses();
    setExpenses(data);
    setLoading(false);
  };

  useEffect(() => {
    loadExpenses();
  }, []);

  return (
    <div className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">
              اختبار عمليات العهدة - أبو تميم
            </h1>
            <AddExpenseDialog
              employeeId="abu_tamim"
              onSuccess={loadExpenses}
            />
          </div>
          
          <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded">
            <h2 className="font-semibold text-blue-900 mb-2">إرشادات الاختبار:</h2>
            <ul className="list-disc list-inside space-y-1 text-blue-800 text-sm">
              <li>اختر نوع العملية "صرف عهدة" للاختبار</li>
              <li>أدخل مبلغ موجب (مثلاً: 500) - سيتم تحويله تلقائياً إلى سالب (خصم من العهدة)</li>
              <li>يمكنك أيضاً إدخال مبلغ سالب مباشرة (مثلاً: -300)</li>
              <li>سيتم إضافة علامة "[Source: Abu Tamim Custody]" تلقائياً للعمليات</li>
            </ul>
          </div>

          {loading ? (
            <div className="text-center py-8">جاري التحميل...</div>
          ) : (
            <ExpensesTable
              expenses={expenses}
              currentUserId="abu_tamim"
              onUpdate={loadExpenses}
            />
          )}
        </div>
      </div>
    </div>
  );
}
