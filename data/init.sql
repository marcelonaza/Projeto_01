CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL
);

-- Insert dummy sales data
INSERT INTO sales (sale_date, product_name, quantity, unit_price, category) VALUES
('2026-01-05', 'Notebook Pro 15', 2, 1200.00, 'Eletrônicos'),
('2026-01-07', 'Teclado Mecânico RGB', 5, 80.00, 'Periféricos'),
('2026-01-12', 'Monitor UltraWide 29', 1, 350.00, 'Eletrônicos'),
('2026-01-15', 'Cadeira Gamer Ergonomica', 1, 250.00, 'Móveis'),
('2026-01-20', 'Mouse Gamer Sem Fio', 10, 45.00, 'Periféricos'),
('2026-02-02', 'Notebook Pro 15', 1, 1200.00, 'Eletrônicos'),
('2026-02-10', 'Fone de Ouvido Noise Cancelling', 4, 150.00, 'Periféricos'),
('2026-02-15', 'Mesa de Escritório Regulável', 2, 400.00, 'Móveis'),
('2026-02-22', 'Teclado Mecânico RGB', 3, 80.00, 'Periféricos'),
('2026-03-01', 'Monitor UltraWide 29', 2, 350.00, 'Eletrônicos'),
('2026-03-05', 'Mouse Gamer Sem Fio', 6, 45.00, 'Periféricos'),
('2026-03-12', 'Cadeira Gamer Ergonomica', 3, 250.00, 'Móveis'),
('2026-03-18', 'Notebook Pro 15', 3, 1200.00, 'Eletrônicos'),
('2026-04-02', 'Teclado Mecânico RGB', 2, 80.00, 'Periféricos'),
('2026-04-10', 'Monitor UltraWide 29', 3, 350.00, 'Eletrônicos'),
('2026-04-25', 'Fone de Ouvido Noise Cancelling', 8, 150.00, 'Periféricos'),
('2026-05-05', 'Mesa de Escritório Regulável', 1, 400.00, 'Móveis'),
('2026-05-14', 'Notebook Pro 15', 1, 1200.00, 'Eletrônicos'),
('2026-05-20', 'Teclado Mecânico RGB', 4, 80.00, 'Periféricos'),
('2026-05-29', 'Cadeira Gamer Ergonomica', 2, 250.00, 'Móveis');
