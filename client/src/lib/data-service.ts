import { CustodyConfirmationRequest, Employee, Expense } from "@/types";
import { MOCK_EMPLOYEES } from "./mock-data";

// LocalStorage keys
const STORAGE_KEYS = {
  EXPENSES: "app_expenses",
  EMPLOYEES: "app_employees",
  CUSTODY_CONFIRMATIONS: "app_custody_confirmations",
};

// Helper to simulate delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Initialize storage with mock data if empty
function initStorage() {
  if (!localStorage.getItem(STORAGE_KEYS.EMPLOYEES)) {
    localStorage.setItem(
      STORAGE_KEYS.EMPLOYEES,
      JSON.stringify(MOCK_EMPLOYEES)
    );
  }
  if (!localStorage.getItem(STORAGE_KEYS.EXPENSES)) {
    localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify([]));
  }
}

// Fetch expenses from LocalStorage
async function fetchExpenses(): Promise<Expense[]> {
  await delay(500); // Simulate network delay
  initStorage();
  try {
    const expensesStr = localStorage.getItem(STORAGE_KEYS.EXPENSES);
    return expensesStr ? JSON.parse(expensesStr) : [];
  } catch (err) {
    console.error("Error fetching expenses:", err);
    return [];
  }
}

// Fetch employees from LocalStorage
async function fetchEmployees(): Promise<Employee[]> {
  await delay(500);
  initStorage();
  try {
    const employeesStr = localStorage.getItem(STORAGE_KEYS.EMPLOYEES);
    return employeesStr ? JSON.parse(employeesStr) : MOCK_EMPLOYEES;
  } catch (err) {
    console.error("Error fetching employees:", err);
    return MOCK_EMPLOYEES;
  }
}

// Add a new expense
async function addExpense(
  expense: Omit<Expense, "id" | "createdAt">
): Promise<Expense | null> {
  await delay(500);
  try {
    const expenses = await fetchExpenses();
    const employees = await fetchEmployees();

    // Find employee name
    const employee = employees.find(e => e.id === expense.employeeId);
    const employeeName = employee ? employee.name : "غير معروف";

    // LOGIC: Amount signs are now handled in the UI layer (AddExpenseDialog)
    // The amount comes in with the correct sign already applied
    let finalAmount = expense.amount;

    const newExpense: Expense = {
      ...expense,
      employeeName,
      amount: finalAmount,
      id: Math.random().toString(36).substr(2, 9),
      createdAt: new Date().toISOString(),
      confirmedByEmployee: false,
      // Ensure createdBy is set
      createdBy: expense.createdBy || "employee",
      createdByName: expense.createdByName,
    };

    expenses.unshift(newExpense); // Add to top
    localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify(expenses));

    // Update employee balance
    await updateEmployeeBalance(expense.employeeId, finalAmount);

    return newExpense;
  } catch (err) {
    console.error("Error adding expense:", err);
    return null;
  }
}

// Update employee balance helper
async function updateEmployeeBalance(employeeId: string, amountChange: number) {
  const employees = await fetchEmployees();
  const employeeIndex = employees.findIndex(e => e.id === employeeId);
  if (employeeIndex >= 0) {
    employees[employeeIndex].custodyBalance =
      (employees[employeeIndex].custodyBalance || 0) + amountChange;
    localStorage.setItem(STORAGE_KEYS.EMPLOYEES, JSON.stringify(employees));
  }
}

// Confirm an expense
async function confirmExpense(id: string): Promise<boolean> {
  await delay(300);
  try {
    const expenses = await fetchExpenses();
    const index = expenses.findIndex(e => e.id === id);
    if (index >= 0) {
      expenses[index].status = "paid";
      expenses[index].confirmedByEmployee = true;
      expenses[index].confirmedAt = new Date().toISOString();
      localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify(expenses));
      return true;
    }
    return false;
  } catch (err) {
    console.error("Error confirming expense:", err);
    return false;
  }
}

// Reject an expense
async function rejectExpense(id: string): Promise<boolean> {
  await delay(300);
  try {
    const expenses = await fetchExpenses();
    const index = expenses.findIndex(e => e.id === id);
    if (index >= 0) {
      expenses[index].status = "rejected";
      expenses[index].confirmedByEmployee = false;
      expenses[index].confirmedAt = new Date().toISOString();
      localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify(expenses));
      return true;
    }
    return false;
  } catch (err) {
    console.error("Error rejecting expense:", err);
    return false;
  }
}

// Delete expense (Reverse transaction)
async function deleteExpense(id: string): Promise<boolean> {
  await delay(300);
  try {
    const expenses = await fetchExpenses();
    const expense = expenses.find(e => e.id === id);

    if (expense) {
      // Reverse the balance effect
      // If it was negative (deduction), we add it back (positive)
      // If it was positive (credit), we subtract it (negative)
      await updateEmployeeBalance(expense.employeeId, -expense.amount);

      const newExpenses = expenses.filter(e => e.id !== id);
      localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify(newExpenses));
      return true;
    }
    return false;
  } catch (err) {
    console.error("Error deleting expense:", err);
    return false;
  }
}

// ==================== Custody Confirmation Functions ====================

// Fetch custody confirmation requests from LocalStorage
async function fetchCustodyConfirmations(): Promise<CustodyConfirmationRequest[]> {
  await delay(300);
  try {
    const confirmationsStr = localStorage.getItem(STORAGE_KEYS.CUSTODY_CONFIRMATIONS);
    return confirmationsStr ? JSON.parse(confirmationsStr) : [];
  } catch (err) {
    console.error("Error fetching custody confirmations:", err);
    return [];
  }
}

// Create a new custody confirmation request
async function createCustodyConfirmationRequest(
  request: Omit<CustodyConfirmationRequest, "id" | "requestedAt" | "status">
): Promise<CustodyConfirmationRequest | null> {
  await delay(300);
  try {
    const confirmations = await fetchCustodyConfirmations();
    const employees = await fetchEmployees();

    // Get employee names
    const fromEmployee = employees.find(e => e.id === request.fromEmployeeId);
    const toEmployee = employees.find(e => e.id === request.toEmployeeId);

    const newRequest: CustodyConfirmationRequest = {
      ...request,
      id: Math.random().toString(36).substr(2, 9),
      fromEmployeeName: fromEmployee?.name || "غير معروف",
      toEmployeeName: toEmployee?.name || "غير معروف",
      requestedAt: new Date().toISOString(),
      status: "pending",
    };

    confirmations.unshift(newRequest);
    localStorage.setItem(STORAGE_KEYS.CUSTODY_CONFIRMATIONS, JSON.stringify(confirmations));

    return newRequest;
  } catch (err) {
    console.error("Error creating custody confirmation request:", err);
    return null;
  }
}

// Confirm a custody confirmation request (by the receiving employee)
async function confirmCustodyRequest(id: string): Promise<boolean> {
  await delay(300);
  try {
    const confirmations = await fetchCustodyConfirmations();
    const index = confirmations.findIndex(c => c.id === id);

    if (index >= 0) {
      const request = confirmations[index];

      // Update request status
      confirmations[index].status = "confirmed";
      confirmations[index].confirmedAt = new Date().toISOString();
      localStorage.setItem(STORAGE_KEYS.CUSTODY_CONFIRMATIONS, JSON.stringify(confirmations));

      // Transfer the custody balance
      // Deduct from sender
      await updateEmployeeBalance(request.fromEmployeeId, -request.amount);
      // Add to receiver
      await updateEmployeeBalance(request.toEmployeeId, request.amount);

      return true;
    }
    return false;
  } catch (err) {
    console.error("Error confirming custody request:", err);
    return false;
  }
}

// Reject a custody confirmation request
async function rejectCustodyRequest(id: string): Promise<boolean> {
  await delay(300);
  try {
    const confirmations = await fetchCustodyConfirmations();
    const index = confirmations.findIndex(c => c.id === id);

    if (index >= 0) {
      confirmations[index].status = "rejected";
      confirmations[index].confirmedAt = new Date().toISOString();
      localStorage.setItem(STORAGE_KEYS.CUSTODY_CONFIRMATIONS, JSON.stringify(confirmations));
      return true;
    }
    return false;
  } catch (err) {
    console.error("Error rejecting custody request:", err);
    return false;
  }
}

// Delete a custody confirmation request
async function deleteCustodyRequest(id: string): Promise<boolean> {
  await delay(300);
  try {
    const confirmations = await fetchCustodyConfirmations();
    const newConfirmations = confirmations.filter(c => c.id !== id);
    localStorage.setItem(STORAGE_KEYS.CUSTODY_CONFIRMATIONS, JSON.stringify(newConfirmations));
    return true;
  } catch (err) {
    console.error("Error deleting custody request:", err);
    return false;
  }
}

export const dataService = {
  getExpenses: fetchExpenses,
  getEmployees: fetchEmployees,
  addExpense,
  confirmExpense,
  rejectExpense,
  deleteExpense,
  // Custody confirmation functions
  getCustodyConfirmations: fetchCustodyConfirmations,
  createCustodyConfirmationRequest,
  confirmCustodyRequest,
  rejectCustodyRequest,
  deleteCustodyRequest,
};
