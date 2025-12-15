import { Employee, Expense } from '@/types';
import { MOCK_EMPLOYEES } from './mock-data';

// LocalStorage keys
const STORAGE_KEYS = {
  EXPENSES: 'app_expenses',
  EMPLOYEES: 'app_employees'
};

// Helper to simulate delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Initialize storage with mock data if empty
function initStorage() {
  if (!localStorage.getItem(STORAGE_KEYS.EMPLOYEES)) {
    localStorage.setItem(STORAGE_KEYS.EMPLOYEES, JSON.stringify(MOCK_EMPLOYEES));
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
    console.error('Error fetching expenses:', err);
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
    console.error('Error fetching employees:', err);
    return MOCK_EMPLOYEES;
  }
}

// Add a new expense
async function addExpense(expense: Omit<Expense, 'id' | 'createdAt'>): Promise<Expense | null> {
  await delay(500);
  try {
    const expenses = await fetchExpenses();
    
    // LOGIC: Auto-convert to negative if it's a work expense
    // This ensures the deduction logic requested by the user
    let finalAmount = expense.amount;
    if (expense.type === 'work_expense' || expense.type === 'deduction') {
       finalAmount = -Math.abs(expense.amount);
    } else if (expense.type === 'custody_payment' || expense.type === 'salary' || expense.type === 'bonus') {
       finalAmount = Math.abs(expense.amount);
    }

    const newExpense: Expense = {
      ...expense,
      amount: finalAmount,
      id: Math.random().toString(36).substr(2, 9),
      createdAt: new Date().toISOString(),
      confirmedByEmployee: false,
      // Ensure createdBy is set
      createdBy: expense.createdBy || 'employee',
      createdByName: expense.createdByName
    };

    expenses.unshift(newExpense); // Add to top
    localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify(expenses));
    
    // Update employee balance
    await updateEmployeeBalance(expense.employeeId, finalAmount);

    return newExpense;
  } catch (err) {
    console.error('Error adding expense:', err);
    return null;
  }
}

// Update employee balance helper
async function updateEmployeeBalance(employeeId: string, amountChange: number) {
  const employees = await fetchEmployees();
  const employeeIndex = employees.findIndex(e => e.id === employeeId);
  if (employeeIndex >= 0) {
    employees[employeeIndex].custodyBalance = (employees[employeeIndex].custodyBalance || 0) + amountChange;
    localStorage.setItem(STORAGE_KEYS.EMPLOYEES, JSON.stringify(employees));
  }
}

// Confirm an expense
async function confirmExpense(id: string, userId: string): Promise<boolean> {
  await delay(300);
  try {
    const expenses = await fetchExpenses();
    const index = expenses.findIndex(e => e.id === id);
    if (index >= 0) {
      expenses[index].status = 'paid';
      expenses[index].confirmedByEmployee = true;
      expenses[index].confirmedAt = new Date().toISOString();
      localStorage.setItem(STORAGE_KEYS.EXPENSES, JSON.stringify(expenses));
      return true;
    }
    return false;
  } catch (err) {
    console.error('Error confirming expense:', err);
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
    console.error('Error deleting expense:', err);
    return false;
  }
}

export const dataService = {
  getExpenses: fetchExpenses,
  getEmployees: fetchEmployees,
  addExpense,
  confirmExpense,
  deleteExpense
};
