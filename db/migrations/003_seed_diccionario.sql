INSERT INTO diccionario_categorias (categoria_real, subcategoria_real, categoria_plan, subcategoria_plan)
VALUES
('Obra Civil', 'Pilotes', 'Obra Civil', 'Pilotes')
ON CONFLICT DO NOTHING;
