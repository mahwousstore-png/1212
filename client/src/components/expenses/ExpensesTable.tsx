import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { dataService } from "@/lib/data-service";
import { EXPENSE_TYPES, Expense, PAYMENT_STATUSES } from "@/types";
import { CheckCircle2, Trash2, User, X } from "lucide-react";
import { toast } from "sonner";

interface ExpensesTableProps {
  expenses: Expense[];
  currentUserId: string;
  onUpdate: () => void;
}

export function ExpensesTable({
  expenses,
  currentUserId,
  onUpdate,
}: ExpensesTableProps) {
  const getTypeLabel = (type: string) => {
    return EXPENSE_TYPES.find(t => t.value === type)?.label || type;
  };

  const getTypeColor = (type: string) => {
    return (
      EXPENSE_TYPES.find(t => t.value === type)?.color ||
      "bg-gray-100 text-gray-800"
    );
  };

  const getStatusLabel = (status: string) => {
    return PAYMENT_STATUSES.find(s => s.value === status)?.label || status;
  };

  const getStatusColor = (status: string) => {
    return (
      PAYMENT_STATUSES.find(s => s.value === status)?.color ||
      "bg-gray-100 text-gray-800"
    );
  };

  const handleConfirm = async (id: string) => {
    const success = await dataService.confirmExpense(id);
    if (success) {
      toast.success("تم تأكيد الاستلام بنجاح");
      onUpdate();
    } else {
      toast.error("حدث خطأ أثناء التأكيد");
    }
  };

  const handleReject = async (id: string) => {
    if (confirm("هل أنت متأكد من رفض هذا المصروف؟")) {
      const success = await dataService.rejectExpense(id);
      if (success) {
        toast.success("تم رفض المصروف بنجاح");
        onUpdate();
      } else {
        toast.error("حدث خطأ أثناء الرفض");
      }
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("هل أنت متأكد من حذف هذا المصروف؟ سيتم عكس العملية المالية.")) {
      const success = await dataService.deleteExpense(id);
      if (success) {
        toast.success("تم حذف المصروف بنجاح");
        onUpdate();
      } else {
        toast.error("حدث خطأ أثناء الحذف");
      }
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-right">التاريخ</TableHead>
            <TableHead className="text-right">الموظف</TableHead>
            <TableHead className="text-right">النوع</TableHead>
            <TableHead className="text-right">المبلغ</TableHead>
            <TableHead className="text-right">الحالة</TableHead>
            <TableHead className="text-right">المصدر</TableHead>
            <TableHead className="text-right">ملاحظات</TableHead>
            <TableHead className="text-right">إجراءات</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {expenses.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={8}
                className="text-center py-8 text-muted-foreground"
              >
                لا توجد مصروفات مسجلة
              </TableCell>
            </TableRow>
          ) : (
            expenses.map(expense => (
              <TableRow key={expense.id}>
                <TableCell>{expense.date}</TableCell>
                <TableCell>{expense.employeeName}</TableCell>
                <TableCell>
                  <Badge
                    variant="secondary"
                    className={getTypeColor(expense.type)}
                  >
                    {getTypeLabel(expense.type)}
                  </Badge>
                </TableCell>
                <TableCell
                  className={`font-bold ${expense.amount < 0 ? "text-red-600" : "text-green-600"}`}
                >
                  {Math.abs(expense.amount).toLocaleString()} ر.س
                </TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={getStatusColor(expense.status)}
                  >
                    {getStatusLabel(expense.status)}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <User className="h-3 w-3" />
                    {expense.createdBy === "employee"
                      ? "عهدة الموظف"
                      : `بواسطة: ${expense.createdByName || "الإدارة"}`}
                  </div>
                </TableCell>
                <TableCell
                  className="max-w-[200px] truncate"
                  title={expense.notes}
                >
                  {expense.notes}
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {expense.status === "pending" &&
                      expense.employeeId === currentUserId && (
                        <>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleConfirm(expense.id)}
                            title="تأكيد الاستلام"
                          >
                            <CheckCircle2 className="h-4 w-4 text-green-600" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleReject(expense.id)}
                            title="رفض المصروف"
                          >
                            <X className="h-4 w-4 text-red-600" />
                          </Button>
                        </>
                      )}
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDelete(expense.id)}
                      title="حذف"
                    >
                      <Trash2 className="h-4 w-4 text-red-600" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
}
