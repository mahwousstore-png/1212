import { Employee } from "@/types";

export const MOCK_EMPLOYEES: Employee[] = [
  {
    id: "1",
    name: "أحمد محمد",
    role: "مدير مبيعات",
    salary: 5000,
    joinDate: "2023-01-15",
    custodyBalance: 1500,
    email: "ahmed@example.com"
  },
  {
    id: "2",
    name: "سارة علي",
    role: "محاسب",
    salary: 4500,
    joinDate: "2023-03-10",
    custodyBalance: 500,
    email: "sara@example.com"
  },
  {
    id: "3",
    name: "خالد عمر",
    role: "مندوب",
    salary: 3500,
    joinDate: "2023-06-01",
    custodyBalance: 2000,
    email: "khaled@example.com"
  }
];
