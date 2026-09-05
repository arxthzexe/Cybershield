-- Create reports table for public incident submissions
CREATE TABLE public.reports (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  category TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.reports ENABLE ROW LEVEL SECURITY;

-- Allow anyone to insert reports (public form)
CREATE POLICY "Anyone can submit reports" 
ON public.reports 
FOR INSERT 
WITH CHECK (true);

-- Create le_transactions table for law enforcement console
CREATE TABLE public.le_transactions (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  account_id TEXT NOT NULL,
  risk_score INTEGER NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
  amount DECIMAL(12,2),
  transaction_type TEXT,
  source TEXT,
  destination TEXT,
  risk_level TEXT NOT NULL,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Enable RLS (access controlled, no public policies)
ALTER TABLE public.le_transactions ENABLE ROW LEVEL SECURITY;

-- Insert sample data for LE console
INSERT INTO public.le_transactions (account_id, risk_score, amount, transaction_type, source, destination, risk_level, notes) VALUES
('ACC-2024-0891', 85, 15000.00, 'Wire Transfer', 'Unknown', 'Offshore Account', 'high', 'Multiple rapid transfers detected'),
('ACC-2024-1234', 45, 2500.00, 'Card Payment', 'Local Bank', 'E-commerce', 'medium', 'Unusual purchase pattern'),
('ACC-2024-0456', 15, 150.00, 'ATM Withdrawal', 'Local ATM', 'Cash', 'low', 'Normal activity'),
('ACC-2024-0789', 92, 50000.00, 'Crypto Exchange', 'Unknown Wallet', 'Exchange', 'high', 'Large crypto movement'),
('ACC-2024-0123', 30, 800.00, 'Online Transfer', 'Savings', 'Checking', 'low', 'Internal transfer');