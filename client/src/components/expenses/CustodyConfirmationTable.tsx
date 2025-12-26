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
import { CUSTODY_CONFIRMATION_STATUSES, CustodyConfirmationRequest } from "@/types";
import { ArrowLeftRight, CheckCircle2, Trash2, X } from "lucide-react";
import { toast } from "sonner";

interface CustodyConfirmationTableProps {
  confirmations: CustodyConfirmationRequest[];
  currentUserId: string;
  onUpdate: () => void;
}

export function CustodyConfirmationTable({
  confirmations,
  currentUserId,
  onUpdate,
}: CustodyConfirmationTableProps) {
  const getStatusLabel = (status: string) => {
    return CUSTODY_CONFIRMATION_STATUSES.find(s => s.value === status)?.label || status;
  };

  const getStatusColor = (status: string) => {
    return (
      CUSTODY_CONFIRMATION_STATUSES.find(s => s.value === status)?.color ||
      "bg-gray-100 text-gray-800"
    );
  };

  const handleConfirm = async (id: string) => {
    const success = await dataService.confirmCustodyRequest(id);
    if (success) {
      toast.success("تم تأكيد استلام العهدة بنجاح");
      onUpdate();
    } else {
      toast.error("حدث خطأ أثناء التأكيد");
    }
  };

  const handleReject = async (id: string) => {
    if (confirm("هل أنت متأكد من رفض طلب تحويل العهدة؟")) {
      const success = await dataService.rejectCustodyRequest(id);
      if (success) {
        toast.success("تم رفض طلب تحويل العهدة");
        onUpdate();
      } else {
        toast.error("حدث خطأ أثناء الرفض");
      }
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("هل أنت متأكد من حذف هذا الطلب؟")) {
      const success = await dataService.deleteCustodyRequest(id);
      if (success) {
        toast.success("تم حذف الطلب بنجاح");
        onUpdate();
      } else {
        toast.error("حدث خطأ أثناء الحذف");
      }
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("ar-SA", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="text-right">التاريخ</TableHead>
            <TableHead className="text-right">من</TableHead>
            <TableHead className="text-right">إلى</TableHead>
            <TableHead className="text-right">المبلغ</TableHead>
            <TableHead className="text-right">الحالة</TableHead>
            <TableHead className="text-right">ملاحظات</TableHead>
            <TableHead className="text-right">إجراءات</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {confirmations.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={7}
                className="text-center py-8 text-muted-foreground"
              >
                <div className="flex flex-col items-center gap-2">
                  <ArrowLeftRight className="h-8 w-8 text-muted-foreground/50" />
                  <span>لا توجد طلبات تأكيد عهدة</span>
                </div>
              </TableCell>
            </TableRow>
          ) : (
            confirmations.map(confirmation => (
              <TableRow key={confirmation.id}>
                <TableCell className="text-sm">
                  {formatDate(confirmation.requestedAt)}
                </TableCell>
                <TableCell className="font-medium">
                  {confirmation.fromEmployeeName}
                </TableCell>
                <TableCell className="font-medium">
                  {confirmation.toEmployeeName}
                </TableCell>
                <TableCell className="font-bold text-primary">
                  {confirmation.amount.toLocaleString()} ر.س
                </TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    className={getStatusColor(confirmation.status)}
                  >
                    {getStatusLabel(confirmation.status)}
                  </Badge>
                </TableCell>
                <TableCell
                  className="max-w-[200px] truncate text-sm"
                  title={confirmation.notes}
                >
                  {confirmation.notes || "-"}
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {confirmation.status === "pending" &&
                      confirmation.toEmployeeId === currentUserId && (
                        <>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleConfirm(confirmation.id)}
                            title="تأكيد استلام العهدة"
                            className="hover:bg-green-100"
                          >
                            <CheckCircle2 className="h-4 w-4 text-green-600" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleReject(confirmation.id)}
                            title="رفض طلب التحويل"
                            className="hover:bg-red-100"
                          >
                            <X className="h-4 w-4 text-red-600" />
                          </Button>
                        </>
                      )}
                    {confirmation.status !== "pending" && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDelete(confirmation.id)}
                        title="حذف"
                        className="hover:bg-red-100"
                      >
                        <Trash2 className="h-4 w-4 text-red-600" />
                      </Button>
                    )}
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
