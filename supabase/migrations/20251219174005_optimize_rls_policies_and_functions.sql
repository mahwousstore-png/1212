-- Optimize RLS Policies and Functions
--
-- This migration addresses:
-- 1. RLS policy performance: Cache auth functions with SELECT statements
-- 2. Function search_path: Make it immutable for better performance
-- 3. Notes on unused indexes: They are intentional and will be used once data grows

-- Drop and recreate trigger function with immutable search_path
DROP TRIGGER IF EXISTS update_employees_updated_at ON employees;
DROP TRIGGER IF EXISTS update_expenses_updated_at ON expenses;
DROP FUNCTION IF EXISTS update_updated_at_column();

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
STABLE
SET search_path = public
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- Recreate triggers
CREATE TRIGGER update_employees_updated_at
  BEFORE UPDATE ON employees
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_expenses_updated_at
  BEFORE UPDATE ON expenses
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Drop old RLS policies
DROP POLICY IF EXISTS "Admins can insert employees" ON employees;
DROP POLICY IF EXISTS "Admins can update employees" ON employees;
DROP POLICY IF EXISTS "Users can view own expenses, admins view all" ON expenses;
DROP POLICY IF EXISTS "Employees can create own expenses" ON expenses;
DROP POLICY IF EXISTS "Admins can update expenses" ON expenses;
DROP POLICY IF EXISTS "Admins can delete expenses" ON expenses;

-- Recreate RLS policies with optimized auth function calls using SELECT
-- This caches the auth function result instead of re-evaluating per row

-- Employees insert policy
CREATE POLICY "Admins can insert employees"
  ON employees
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  );

-- Employees update policy
CREATE POLICY "Admins can update employees"
  ON employees
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  );

-- Expenses select policy
CREATE POLICY "Users can view own expenses, admins view all"
  ON expenses
  FOR SELECT
  TO authenticated
  USING (
    employee_id::text = (SELECT auth.uid()::text)
    OR EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  );

-- Expenses insert policy
CREATE POLICY "Employees can create own expenses"
  ON expenses
  FOR INSERT
  TO authenticated
  WITH CHECK (
    employee_id::text = (SELECT auth.uid()::text)
    OR EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  );

-- Expenses update policy
CREATE POLICY "Admins can update expenses"
  ON expenses
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  );

-- Expenses delete policy
CREATE POLICY "Admins can delete expenses"
  ON expenses
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = (SELECT auth.uid())
      AND auth.users.raw_app_meta_data->>'role' = 'admin'
    )
  );