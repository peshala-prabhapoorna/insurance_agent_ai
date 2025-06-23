-- policies table
CREATE TABLE policies (
  policy_id INTEGER PRIMARY KEY,
  policy_name TEXT NOT NULL,
  description TEXT,
  premium REAL NOT NULL,
  coverage_amount REAL NOT NULL
);

-- plans table
CREATE TABLE plans (
  plan_id INTEGER PRIMARY KEY,
  plan_name TEXT NOT NULL,
  policy_id INTEGER NOT NULL,
  term_years INTEGER NOT NULL,
  monthly_cost REAL NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

-- Expanded Seed: Policies
INSERT INTO policies (policy_name, description, premium, coverage_amount) VALUES
  ('Auto Basic', 'Entry-level auto coverage with minimal deductible', 500.00, 20000.00),
  ('Auto Plus', 'Enhanced auto coverage with roadside assistance', 650.00, 30000.00),
  ('Home Secure', 'Comprehensive home insurance', 1200.00, 150000.00),
  ('Home Secure Plus', 'Includes flood and earthquake riders', 1500.00, 200000.00),
  ('Health Basic', 'Basic health insurance plan', 600.00, 30000.00),
  ('Health Plus', 'Standard health insurance plan', 800.00, 50000.00),
  ('Life Secure', 'Term life insurance, 20-year term', 450.00, 100000.00),
  ('Life Premium', 'Whole life coverage with cash value', 900.00, 250000.00),
  ('Travel Explorer', 'International travel medical and trip cancellation', 150.00, 10000.00),
  ('Pet Care', 'Accident & illness coverage for pets', 200.00, 5000.00);

-- Expanded Seed: Plans (3 plans per policy)
INSERT INTO plans (plan_name, policy_id, term_years, monthly_cost) VALUES
  -- Auto Basic
  ('Auto Basic – 1 year',       1, 1, 45.00),
  ('Auto Basic – 5 years',      1, 5, 40.00),
  ('Auto Basic – 10 years',     1, 10, 38.00),

  -- Auto Plus
  ('Auto Plus – 1 year',        2, 1, 55.00),
  ('Auto Plus – 5 years',       2, 5, 50.00),
  ('Auto Plus – 10 years',      2, 10, 47.00),

  -- Home Secure
  ('Home Secure – 5 years',     3, 5, 95.00),
  ('Home Secure – 10 years',    3, 10, 100.00),
  ('Home Secure – 30 years',    3, 30, 85.00),

  -- Home Secure Plus
  ('Home Plus – 5 years',       4, 5, 120.00),
  ('Home Plus – 10 years',      4, 10, 140.00),
  ('Home Plus – 30 years',      4, 30, 110.00),

  -- Health Basic
  ('Health Basic – 1 year',     5, 1, 55.00),
  ('Health Basic – 3 years',    5, 3, 52.00),
  ('Health Basic – 5 years',    5, 5, 50.00),

  -- Health Plus
  ('Health Plus – 1 year',      6, 1, 70.00),
  ('Health Plus – 3 years',     6, 3, 67.00),
  ('Health Plus – 5 years',     6, 5, 65.00),

  -- Life Secure
  ('Life Secure – 10 years',    7, 10, 35.00),
  ('Life Secure – 20 years',    7, 20, 30.00),
  ('Life Secure – 30 years',    7, 30, 28.00),

  -- Life Premium
  ('Life Premium – Whole Life', 8, 0, 75.00),  -- 0 = whole life
  ('Life Premium – 20 yr term', 8, 20, 60.00),
  ('Life Premium – 30 yr term', 8, 30, 58.00),

  -- Travel Explorer
  ('Travel Explorer – Single Trip', 9, 0, 12.00),
  ('Travel Explorer – Annual',      9, 1, 30.00),
  ('Travel Explorer – Frequent',    9, 1, 45.00),

  -- Pet Care
  ('Pet Care – Dogs',           10, 1, 18.00),
  ('Pet Care – Cats',           10, 1, 15.00),
  ('Pet Care – Multi-Pet',      10, 1, 25.00);
