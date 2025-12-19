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
  amount: z.coerce
    .number({ message: "يجب إدخال رقم صحيح" })
    .refine(val => val !== 0, {
      message: "المبلغ يجب أن يكون مختلف عن صفر (يمكن إدخال قيم موجبة أو سالبة)",
    }),
  type: z.string().min(1, "نوع المصروف مطلوب"),
  date: z.string().min(1, "التاريخ مطلوب"),
  notes: z.string().optional(),
});

interface AddExpenseDialogProps {
  employeeId: string;
  onSuccess: () => void;
}

export function AddExpenseDialog({
  employeeId,
  onSuccess,
}: AddExpenseDialogProps) {
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
      // Handle amount logic based on type
      let finalAmount = values.amount;

      // Special handling for custody_payment (صرف عهدة)
      // If it's custody_payment, treat it as a deduction (negative)
      // Users can enter positive amounts, they will be converted to negative
      if (values.type === "custody_payment") {
        finalAmount = -Math.abs(values.amount);
      }

      // For Abu Tamim custody operations
      // Check if this is for Abu Tamim employee
      const isAbuTamimOperation = employeeId === "abu_tamim";

      const newExpense: Omit<Expense, "id" | "createdAt"> = {
        confirmedByEmployee: false,
        employeeId,
        employeeName: "", // Will be populated by dataService
        type: values.type as any,
        amount: finalAmount,
        date: values.date,
        month: values.date.substring(0, 7),
        paymentMethod: "cash",
        status: "pending",
        notes: isAbuTamimOperation && values.type === "custody_payment"
          ? `${values.notes || ""} [Source: Abu Tamim Custody]`.trim()
          : values.notes,
        createdBy: "employee", // Default, will be overridden by service based on actual user
        createdByName: isAbuTamimOperation ? "Abu Tamim" : undefined,
      };

      await dataService.addExpense(newExpense);
      toast.success("تم إضافة العملية بنجاح");
      setOpen(false);
      form.reset();
      onSuccess();
    } catch {
      toast.error("حدث خطأ أثناء إضافة العملية");
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <PlusIcon className="h-4 w-4" />
          إضافة عملية جديدة
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>إضافة عملية جديدة</DialogTitle>
          <DialogDescription>
            أدخل تفاصيل العملية المالية. لصرف العهدة، أدخل المبلغ وسيتم خصمه تلقائياً من رصيد العهدة.
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
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="اختر النوع" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {EXPENSE_TYPES.map(type => (
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
                    <Input
                      type="number"
                      step="0.01"
                      placeholder="أدخل المبلغ (موجب أو سالب)"
                      value={field.value as number}
                      onChange={field.onChange}
                      onBlur={field.onBlur}
                      name={field.name}
                      ref={field.ref}
                    />
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
