export type UserRole = "admin" | "user" | "owner";

export interface UserProfile {
  id: string;
  email: string;
  full_name?: string;
  role: UserRole;
  created_at: string;
}

export interface Employee {
  id: string;
  name: string;
  role: string;
  salary: number;
  joinDate: string;
  custodyBalance: number;
  email?: string;
}

export type ExpenseType =
  | "work_expense"
  | "custody_payment"
  | "salary"
  | "bonus"
  | "deduction"
  | "loan"
  | "other";

export interface Expense {
  id: string;
  employeeId: string;
  employeeName: string;
  type: ExpenseType;
  amount: number;
  date: string;
  month: string;
  paymentMethod: "cash" | "bank_transfer" | "check";
  status: "pending" | "paid" | "rejected";
  notes?: string;
  receiptUrl?: string;
  createdAt: string;
  confirmedByEmployee: boolean;
  confirmedAt?: string;
  createdBy: "admin" | "employee";
  createdByName?: string;
}

// Custody Confirmation Request - for confirming custody transfers between employees
export type CustodyConfirmationStatus = "pending" | "confirmed" | "rejected";

export interface CustodyConfirmationRequest {
  id: string;
  fromEmployeeId: string;
  fromEmployeeName: string;
  toEmployeeId: string;
  toEmployeeName: string;
  amount: number;
  requestedAt: string;
  confirmedAt?: string;
  status: CustodyConfirmationStatus;
  notes?: string;
  requestedBy: "admin" | "employee";
}

export const EXPENSE_TYPES: {
  value: ExpenseType;
  label: string;
  color: string;
}[] = [
  {
    value: "work_expense",
    label: "مصروفات عمل (عهدة)",
    color: "bg-red-100 text-red-800",
  },
  {
    value: "custody_payment",
    label: "صرف عهدة",
    color: "bg-green-100 text-green-800",
  },
  { value: "salary", label: "راتب شهري", color: "bg-blue-100 text-blue-800" },
  {
    value: "bonus",
    label: "مكافأة / حافز",
    color: "bg-purple-100 text-purple-800",
  },
  {
    value: "deduction",
    label: "خصم / جزاء",
    color: "bg-orange-100 text-orange-800",
  },
  { value: "loan", label: "سلفة", color: "bg-yellow-100 text-yellow-800" },
  { value: "other", label: "أخرى", color: "bg-gray-100 text-gray-800" },
];

export const PAYMENT_STATUSES = [
  { value: "pending", label: "معلق", color: "bg-yellow-100 text-yellow-800" },
  { value: "paid", label: "مكتمل", color: "bg-green-100 text-green-800" },
  { value: "rejected", label: "مرفوض", color: "bg-red-100 text-red-800" },
];

export const CUSTODY_CONFIRMATION_STATUSES = [
  { value: "pending", label: "في انتظار التأكيد", color: "bg-amber-100 text-amber-800" },
  { value: "confirmed", label: "تم التأكيد", color: "bg-emerald-100 text-emerald-800" },
  { value: "rejected", label: "مرفوض", color: "bg-red-100 text-red-800" },
];
