import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { dataService } from "@/lib/data-service";
import { EXPENSE_TYPES, Expense } from "@/types";
import { zodResolver } from "@hookform/resolvers/zod";
import { PlusIcon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const formSchema = z.object({
  amount: z.coerce.number().min(1, "المبلغ مطلوب"),
  type: z.string().min(1, "نوع المصروف مطلوب"),
  date: z.string().min(1, "التاريخ مطلوب"),
  notes: z.string().optional(),
});

interface AddExpenseDialogProps {
  employeeId: string;
  onSuccess: () => void;
}

export function AddExpenseDialog({ employeeId, onSuccess }: AddExpenseDialogProps) {
  const [open, setOpen] = useState(false);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      amount: 0,
      type: "work_expense",
      date: new Date().toISOString().split("T")[0],
      notes: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      // Auto-convert to negative if it's a work expense (custody deduction)
      // But keep positive for display, the backend/service handles the debit logic
      // Actually, let's make it explicit here as requested
      
      // The user enters a positive number (e.g. 50).
      // If type is 'work_expense', we want to deduct it.
      // The dataService.addExpense handles the debit/credit logic based on type.
      // So we just pass the positive amount and let the service handle the sign in the DB transaction.
      
      const newExpense: Omit<Expense, "id" | "createdAt"> = {
        confirmedByEmployee: false,
        employeeId,
        employeeName: "", // Will be filled by backend/service
        type: values.type as any,
        amount: values.amount,
        date: values.date,
        month: values.date.substring(0, 7),
        paymentMethod: "cash",
        status: "pending",
        notes: values.notes,
        createdBy: "employee", // Default, will be overridden by service based on actual user
      };

      await dataService.addExpense(newExpense);
      toast.success("تم إضافة المصروف بنجاح");
      setOpen(false);
      form.reset();
      onSuccess();
    } catch (error) {
      toast.error("حدث خطأ أثناء إضافة المصروف");
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <PlusIcon className="h-4 w-4" />
          إضافة مصروف جديد
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>إضافة مصروف جديد</DialogTitle>
          <DialogDescription>
            أدخل تفاصيل المصروف ليتم خصمه من العهدة أو إضافته.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="type"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>نوع العملية</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="اختر النوع" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {EXPENSE_TYPES.map((type) => (
                        <SelectItem key={type.value} value={type.value}>
                          {type.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="amount"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>المبلغ (ر.س)</FormLabel>
                  <FormControl>
                    <Input type="number" step="0.01" {...field} value={field.value as number} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="date"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>التاريخ</FormLabel>
                  <FormControl>
                    <Input type="date" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="notes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>ملاحظات / وصف</FormLabel>
                  <FormControl>
                    <Textarea {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button type="submit">حفظ العملية</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
