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
import { Employee } from "@/types";
import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowLeftRight } from "lucide-react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

const formSchema = z.object({
  toEmployeeId: z.string().min(1, "يجب اختيار الموظف المستلم"),
  amount: z.coerce
    .number({ message: "يجب إدخال رقم صحيح" })
    .positive({ message: "المبلغ يجب أن يكون أكبر من صفر" }),
  notes: z.string().optional(),
});

interface CustodyConfirmationDialogProps {
  fromEmployeeId: string;
  onSuccess: () => void;
}

export function CustodyConfirmationDialog({
  fromEmployeeId,
  onSuccess,
}: CustodyConfirmationDialogProps) {
  const [open, setOpen] = useState(false);
  const [employees, setEmployees] = useState<Employee[]>([]);

  useEffect(() => {
    const loadEmployees = async () => {
      const data = await dataService.getEmployees();
      setEmployees(data);
    };
    loadEmployees();
  }, []);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      toEmployeeId: "",
      amount: 0,
      notes: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    try {
      // Create custody confirmation request
      const result = await dataService.createCustodyConfirmationRequest({
        fromEmployeeId,
        fromEmployeeName: "", // Will be populated by service
        toEmployeeId: values.toEmployeeId,
        toEmployeeName: "", // Will be populated by service
        amount: values.amount,
        notes: values.notes,
        requestedBy: "admin",
      });

      if (result) {
        toast.success("تم إنشاء طلب تأكيد العهدة بنجاح");
        setOpen(false);
        form.reset({
          toEmployeeId: "",
          amount: 0,
          notes: "",
        });
        onSuccess();
      } else {
        toast.error("حدث خطأ أثناء إنشاء الطلب");
      }
    } catch {
      toast.error("حدث خطأ أثناء إنشاء طلب تأكيد العهدة");
    }
  }

  // Filter out the current employee from the list
  const availableEmployees = employees.filter(e => e.id !== fromEmployeeId);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="gap-2">
          <ArrowLeftRight className="h-4 w-4" />
          تحويل عهدة
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>طلب تأكيد تحويل عهدة</DialogTitle>
          <DialogDescription>
            قم بإنشاء طلب لتحويل مبلغ من العهدة إلى موظف آخر. سيتم إرسال الطلب للموظف المستلم للتأكيد.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="toEmployeeId"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>الموظف المستلم</FormLabel>
                  <Select
                    onValueChange={field.onChange}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="اختر الموظف المستلم" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {availableEmployees.map(employee => (
                        <SelectItem key={employee.id} value={employee.id}>
                          {employee.name} - {employee.role}
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
                      min="0"
                      placeholder="أدخل المبلغ"
                      value={field.value as number}
                      onChange={(e) => field.onChange(e.target.value)}
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
              name="notes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>ملاحظات</FormLabel>
                  <FormControl>
                    <Textarea placeholder="أدخل أي ملاحظات إضافية" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <DialogFooter>
              <Button type="submit">إرسال طلب التأكيد</Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
