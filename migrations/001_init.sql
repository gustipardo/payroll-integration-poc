CREATE TABLE IF NOT EXISTS employees (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
external_id TEXT UNIQUE NOT NULL,
name TEXT NOT NULL,
role TEXT,
created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE TABLE IF NOT EXISTS hours (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
employee_id UUID REFERENCES employees(id) ON DELETE CASCADE,
work_date DATE NOT NULL,
hours NUMERIC NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
CREATE TABLE IF NOT EXISTS overtime_requests (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
employee_id UUID REFERENCES employees(id),
period_start DATE,
period_end DATE,
calculated_hours NUMERIC,
status TEXT DEFAULT 'pending', -- pending, approved, rejected
created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
approved_at TIMESTAMP WITH TIME ZONE
);