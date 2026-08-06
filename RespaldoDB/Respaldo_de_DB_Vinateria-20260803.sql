-- ============================================================
-- BACKUP DE BASE DE DATOS 'Vinateria'
-- Fecha: 2026-08-03 20:44:23
-- ============================================================

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- ------------------------------------------------------------
-- Tabla: articulos
-- ------------------------------------------------------------

DROP TABLE IF EXISTS articulos CASCADE;
CREATE TABLE articulos (
    articulo_id integer,
    articulo_articulo character varying,
    articulo_categoria integer,
    articulo_imagen character varying,
    articulo_precio numeric,
    articulo_stock integer,
    articulo_proveedor integer
);

INSERT INTO articulos (articulo_id, articulo_articulo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor) VALUES
(1, 'Cabernet Sauvignon', 4, 'imagen1.jpg', '89.00', 15, NULL),
(2, 'Merlot', 8, 'imagen.jpg', '150.00', 86, NULL),
(3, 'Tempranillo', 5, 'imagen2.jpg', '399.00', 21, NULL),
(4, 'Chardonnay', 3, 'imagen3.jpg', '125.00', 50, NULL),
(5, 'Malbec', 1, 'imagen4.jpg', '200.00', 12, NULL),
(6, 'Champagne', 7, 'imagen5.jpg', '99.00', 1, NULL),
(7, 'Pink Flamingo', 2, 'imagen6.jpg', '320.00', 66, NULL),
(8, 'Riesling', 6, 'imagen7.jpg', '500.00', 45, NULL),
(10, 'Lunaclara Reserve', 8, 'imagen9.jpg', '189.00', 15, NULL),
(11, 'Blue Label Modificado', 1, 'imagen_blue_label.jpg', '1599.99', 6, NULL),
(14, 'Prueba_1_Modificado', 1, 'imagen_prueba_1_modificado.jpg', '1000.00', 1, 2);

-- ------------------------------------------------------------
-- Tabla: articulos_1
-- ------------------------------------------------------------

DROP TABLE IF EXISTS articulos_1 CASCADE;
CREATE TABLE articulos_1 (
    articulo_id integer,
    articulo_articulo character varying,
    articulo_codigo character varying,
    articulo_categoria integer,
    articulo_imagen character varying,
    articulo_precio numeric,
    articulo_stock integer,
    articulo_proveedor integer,
    articulo_vendidos integer DEFAULT 0
);

INSERT INTO articulos_1 (articulo_id, articulo_articulo, articulo_codigo, articulo_categoria, articulo_imagen, articulo_precio, articulo_stock, articulo_proveedor, articulo_vendidos) VALUES
(42, 'Francisco', '12324', 4, 'imagen.jpg', '99.99', 2, 8, 0),
(78, 'ohscaouhf', 'aiphonc', 1, 'images (5)_20260802_213654.jpg', '90.00', 2, 1, 0),
(77, 'Pezcado', '2328798798', 3, 'fish-bone-skeleton-icon-silhouette-free-vector_20260802_213135.webp', '99.99', 0, 9, 8),
(43, 'prueba_15', '21763', 4, 'imagen.html', '99.99', 90, 2, 0),
(38, 'Reisling', '345-354-22', 3, 'imagen_ejemplo.jpg', '1200.00', 0, 3, 8),
(79, 'fut', '3423512', 1, 'folleto-liga-futbol-balon-estilo-plano_20260803_115231.jpg', '10000.00', 1, 1, 0),
(80, 'ejem', '34235', 1, 'logo_metegol_v3_20260803_115403.png', '99.99', 1, 1, 0),
(50, 'Prueba_16', '13879472', 3, 'Diagrama_de_Ishikawa-Proyecto_Integrador-v2.0_20260803_115432.png', '9.00', 34, 2, 15),
(48, 'paco', '1912937197', 8, 'lg-661dcdd59f379-Visual-Studio-Code_20260803_115441.webp', '1279173.44', 0, 10, 1),
(81, 'ejemplo_imagen_5', '2248712789', 1, 'botella_negra_default_Punto_de_Venta_20260803_115819.jpg', '11231.00', 3, 1, 0),
(8, 'paco', 'FLBK', 5, '159-1595977_flask-python-logo-hd-png-download_20260803_125219.webp', '14.00', 0, 3, 3),
(40, 'Prueba_14', '592-617-23', 1, 'javier.img', '12.42', 0, 8, 0),
(73, 'Prueba_imagen_4', '1287192878', 9, 'hq720 (1)_20260801_194115.jpg', '720.20', 0, 4, 20),
(1, 'Blue Label', 'DObKV', 9, 'hq720 (1)_20260803_173618.jpg', '2000.50', 21, 1, 0),
(67, 'Prueba_CAM_vendidos', '2139397', 1, 'ima', '8860.00', 1, 1, 0),
(44, 'Paco', '14144', 5, 'img', '2423.00', 12, 3, 8),
(45, 'preuba_15', '2124708008', 4, 'imagen.html', '14.99', 3, 4, 0),
(52, 'Turnet', '199119', 1, 'iimg', '124.00', 0, 1, 4),
(46, 'Francisco Javier', '1271298370', 3, 'imagen.img', '10.10', 9, 9, 0),
(9, 'paco', 'FLBK', 1, 'imagen', '14.00', 3, 1, 0),
(37, 'Cabernet Sauvignon', '565-218-0', 7, 'imagen_Cabernet_editado.png', '89.99', 8, 8, 6),
(68, 'Pruabe_imagen', '9999999999', 1, 'bottle-with-a-liquid-on-a-solid-color-background-ai-generative-free-photo_20260801_182407.webp', '6720.00', 3, 1, 0),
(69, 'Prueba_imagen_2', '287129', 1, 'glass-and-bottle-of-red-wine-splash-on-black-photo_20260801_182822.webp', '1474.00', 1, 1, 0),
(70, 'Prueba_imagen_3', '7983798172', 10, '01k8v6n48ma4whd3a7g9.webp', '8490.00', 3, 4, 0),
(71, 'Prueba_imagen_3', '22222999', 1, 'depositphotos_88939030-stock-illustration-flag-football-club-real-madrid_20260801_185000.webp', '21930.00', 2, 1, 0),
(72, 'Paco', '1244444444', 1, '📁 visily-multicomponents (2).png', '99999.00', 9, 1, 0),
(75, 'Prueba_6', 'wq8e9q8e89', 1, 'free-javascript-logo-icon-svg-download-png-2284965_20260801_195124.webp', '2173.00', 1, 1, 0),
(76, 'Prueba_7', '20910921', 1, 'free-javascript-logo-icon-svg-download-png-2284965_20260801_195308.webp', '1983.00', 1, 1, 0),
(74, 'Prueba_imagen_5', '2198765432', 9, 'python-logo-icon-programming-language-free-vector_20260802_140808.webp', '1290.00', 2, 10, 0);

-- ------------------------------------------------------------
-- Tabla: categorias
-- ------------------------------------------------------------

DROP TABLE IF EXISTS categorias CASCADE;
CREATE TABLE categorias (
    categoria_id integer,
    categoria_categoria character varying,
    categoria_tipo character varying,
    categoria_descripcion character varying
);

INSERT INTO categorias (categoria_id, categoria_categoria, categoria_tipo, categoria_descripcion) VALUES
(3, 'Rosado', 'Vino', 'Maceración'),
(4, 'Joven', 'Vino', 'Segunda fermentación con gas carbónico'),
(6, 'Secos', 'Licor', '12-20% de azúcar'),
(7, 'Dulces', 'Licor', '22-30% de azúcar'),
(8, 'Finos', 'Licor', '40-60% de azúcar'),
(9, 'Aperitivos', 'Licor', 'Se toman antes de comer para estimular el apetito'),
(2, 'Blanco', 'Vino', 'Sin hollejos'),
(1, 'Tinto', 'Vino', 'Fermentación'),
(5, 'Extra secos', 'Licor', 'Hasta 12% de azúcar'),
(13, 'Francisco', 'Vino', 'Entre más viejo, más bueno'),
(14, 'Tequilas', 'Licor', 'hola'),
(15, 'Tequilas', 'Licor', 'hola2');

-- ------------------------------------------------------------
-- Tabla: privilegios
-- ------------------------------------------------------------

DROP TABLE IF EXISTS privilegios CASCADE;
CREATE TABLE privilegios (
    privilegio_id integer,
    privilegio_privilegio character varying
);

INSERT INTO privilegios (privilegio_id, privilegio_privilegio) VALUES
(2, 'Supervisor'),
(3, 'Cajero'),
(1, 'Administrador');

-- ------------------------------------------------------------
-- Tabla: proveedores
-- ------------------------------------------------------------

DROP TABLE IF EXISTS proveedores CASCADE;
CREATE TABLE proveedores (
    proveedor_id integer,
    proveedor_proveedor character varying,
    proveedor_apaterno character varying,
    proveedor_amaterno character varying,
    proveedor_telefono character varying,
    proveedor_direccion character varying,
    proveedor_correo character varying
);

INSERT INTO proveedores (proveedor_id, proveedor_proveedor, proveedor_apaterno, proveedor_amaterno, proveedor_telefono, proveedor_direccion, proveedor_correo) VALUES
(2, 'Severo', 'Granados', 'Iglesia', '(564) 235-567', '77 Lyme Street', 'bhima@me.com'),
(3, 'Luch', 'Andreu', 'Amat', '(679) 236-265', '9448 Fairfield St.', 'psichel@sdoj.com'),
(4, 'Matías Mauricio', 'Castillo', 'Barrera', '(341) 681-225', '8143 College St.', 'tbeck@optoline.net'),
(7, 'Soraya', 'Morere', 'Lago', '(845) 486-685', '9001 Creek Street', 'wrojf@outlook.com'),
(8, 'Victoriano', 'Tapia', 'Cabanillas', '(344) 457-346', '57 Green Drive', 'flaket@verixon.net'),
(9, 'Nidia', 'Saez', 'Campoy', '(237) 784-357', '86 Surrey St.', 'uncle@hotmail.com'),
(10, 'Teófila', 'Villanueva', 'Molina', '(436) 597-678', '8728 Boston Street', 'slaff@icloud.com'),
(19, 'Francisco Javier', 'Sánchez', 'Islas', '23523325', 'Olivos', 'ejemplo@gmail.com'),
(5, 'Mauricio', 'Guijarro', 'Castelló', '(078) 124-568', '9893 W. Vale Ave', 'eegsa@yahoo.ca'),
(6, 'Isaura Leyre', 'Avilés', 'Pelayo', '(437) 658-235', '8094 Albany Drive', 'barlow@verizon.net'),
(1, 'Leandra Anna', 'Perex', 'de la Rosq', '90-235-574', 'Ejemplo', 'ejemplo@gmail.com');

-- ------------------------------------------------------------
-- Tabla: usuarios
-- ------------------------------------------------------------

DROP TABLE IF EXISTS usuarios CASCADE;
CREATE TABLE usuarios (
    usuario_id integer,
    usuario_usuario character varying,
    usuario_apaterno character varying,
    usuario_amaterno character varying,
    usuario_nuempleado integer,
    usuario_correo character varying,
    usuario_contrasenia character varying,
    usuario_privilegio integer
);

INSERT INTO usuarios (usuario_id, usuario_usuario, usuario_apaterno, usuario_amaterno, usuario_nuempleado, usuario_correo, usuario_contrasenia, usuario_privilegio) VALUES
(3, 'Guillem', 'San', 'Martín', 3, 'zennay343@gmail.com', '2%fdbc-t', 3),
(4, 'Estrella', 'Tala', 'Vera', 4, 'diwa61@gmail.com', '3&36881bv', 2),
(5, 'Maria', 'Victoria', 'Salguero', 5, 'troudir42@gmail.com', 'Q242hdf%3', 3),
(7, 'Omar', 'Caceres', 'Mercedes', 7, 'wolilie05@gmail.com', '(%&[6rghd', 3),
(10, 'Adam', 'Camboy', 'Huevara', 9, 'rojo62@gmail.com', '976drth974', 2),
(6, 'Maria Agustina', 'del', 'Olmo', 7, 'mefrinn23@gmail.com', '<>54Bfvd(6', 2),
(9, 'Gabriela', 'Trinidad', 'Rosales', 98, 'trecoho@gmail.com', '*DFd@bsxbx', 1),
(1, 'Francisco Javier', 'Sánchez', 'Islas', 1, 'javsani95@gmial.com', '´ñ,´p,p,m+,', 1),
(8, 'Constantin', 'Trinidad', 'Rosales', 8, 'mecroi165@gmail.com', '*/HFn5$gxv', 2),
(2, 'Delfina', 'del', 'Olmo', 3, 'gabiya5923@gmail.com', '#6bfh43c', 3),
(13, 'José Gerardo', 'Flores', 'Ortega', 1, 'ejemplo@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 3),
(20, 'ejemplo', 'contraseña', '1', 17, 'ejemplo_contrasenia_1@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 3),
(21, 'ejemplo', 'contraseña', '2', 18, 'ejemplo_contrasenia_2@gmail.com', 'a17444550e2c127b02ea1c197bcffa422c21713040f53d5c2ca7925419bccf7f', 3);

-- ------------------------------------------------------------
-- Tabla: ventas
-- ------------------------------------------------------------

DROP TABLE IF EXISTS ventas CASCADE;
CREATE TABLE ventas (
    venta_id integer,
    venta_venta character varying,
    venta_fecha date DEFAULT CURRENT_DATE,
    venta_ganancia numeric,
    venta_usuario integer,
    venta_articulo ARRAY,
    venta_estado character varying
);

INSERT INTO ventas (venta_id, venta_venta, venta_fecha, venta_ganancia, venta_usuario, venta_articulo, venta_estado) VALUES
(11, 'VEN-20260728_191145-VINATA', '2026-07-28', '89.99', 1, ARRAY[37], 'Concluida'),
(12, 'VEN-20260728_214326-VINATA', '2026-07-28', '14.00', 1, ARRAY[8], 'Concluida'),
(13, 'VEN-20260728_214736-VINATA', '2026-07-28', '2423.00', 1, ARRAY[44], 'Concluida'),
(17, 'VEN-Paco-VINATA', '2026-07-29', '2000.50', 1, ARRAY[1], 'Pendiente'),
(18, 'VEN-20260729_131340-VINATA', '2026-07-29', '2090.49', 1, ARRAY[1, 37], 'Concluida'),
(19, 'VEN-20260729_192025-VINATA', '2026-07-29', '1739.94', 1, ARRAY[37, 38], 'Concluida'),
(20, 'VEN-Prueba-1_Continuar-VINATA', '2026-07-30', '6110.19', 1, ARRAY[37, 38, 46], 'Pendiente'),
(21, 'VEN-20260730_133223-VINATA', '2026-07-30', '3633.10', 1, ARRAY[38, 46, 44], 'Concluida'),
(23, 'VEN-20260730_153650-VINATA', '2026-07-30', '9701.09', 1, ARRAY[37, 38, 46, 50, 44], 'Concluida'),
(24, 'VEN-PENDIENTE_1-VINATA', '2026-07-30', '5619.43', 1, ARRAY[1, 37, 50], 'Concluida'),
(25, 'VEN-PENDIENTE_2-VINATA', '2026-07-30', '3115.41', 1, ARRAY[40, 43, 50, 8], 'Concluida'),
(28, 'VEN-20260730_190955-VINATA', '2026-07-30', '3951.01', 1, ARRAY[40, 43, 50], 'Concluida'),
(30, 'VEN-Prueba_stock_guargar-VINATA', '2026-07-30', '62.10', 1, ARRAY[40], 'Pendiente'),
(31, 'VEN-20260730_211317-VINATA', '2026-07-30', '62.10', 1, ARRAY[40], 'Concluida'),
(32, 'VEN-20260731_102043-VINATA', '2026-07-31', '12.42', 1, ARRAY[40], 'Concluida'),
(34, 'VEN-20260731_102350-VINATA', '2026-07-31', '12115.00', 1, ARRAY[44], 'Concluida'),
(10, 'VEN-editado-VINATA', '2026-06-28', '10.10', 1, ARRAY[46], 'Concluida'),
(33, 'VEN-20260731_102212-VINATA', '2026-06-30', '12.42', 1, ARRAY[40], 'Concluida'),
(35, 'VEN-20260731_102536-VINATA', '2026-06-30', '49999995.00', 1, ARRAY[50], 'Concluida'),
(15, 'VEN-20260728_Editado-VINATA', '2026-08-28', '1279173.44', 1, ARRAY[48], 'Concluida'),
(36, 'VEN-20260731_130142-VINATA', '2026-07-31', '89.99', 1, ARRAY[37], 'Concluida'),
(37, 'VEN-20260731_143907-VINATA', '2026-07-31', '9999.95', 1, ARRAY[51], 'Concluida'),
(38, 'VEN-20260731_171640-VINATA', '2026-07-31', '372.00', 1, ARRAY[52], 'Concluida'),
(39, 'VEN-20260731_174535-VINATA', '2026-07-31', '12115.00', 1, ARRAY[44], 'Concluida'),
(40, 'VEN-20260731_175105-VINATA', '2026-07-31', '7393.00', 1, ARRAY[44, 52], 'Concluida'),
(41, 'VEN-20260731_183122-VINATA', '2026-07-31', '4800.00', 1, ARRAY[38], 'Concluida'),
(42, 'VEN-20260731_183429-VINATA', '2026-07-31', '1279713.38', 1, ARRAY[37, 48], 'Concluida'),
(43, 'VEN-20260802_165006-VINATA', '2026-08-02', '7202.00', 1, ARRAY[73], 'Concluida'),
(45, 'VEN-20260802_214311-VINATA', '2026-08-02', '799.92', 1, ARRAY[77], 'Concluida'),
(46, 'VEN-20260803_085537-VINATA', '2026-08-03', '720.20', 1, ARRAY[73], 'Concluida'),
(47, 'VEN-20260803_115215-VINATA', '2026-08-03', '4800.00', 1, ARRAY[38], 'Concluida'),
(48, 'VEN-20260803_125318-VINATA', '2026-08-03', '42.00', 1, ARRAY[8], 'Concluida'),
(49, 'VEN-20260803_125427-VINATA', '2026-08-03', '6481.80', 1, ARRAY[73], 'Concluida');

-- ------------------------------------------------------------
-- Resetear secuencias
-- ------------------------------------------------------------

SELECT setval('articulo_articulo_id_seq', COALESCE((SELECT MAX(id) FROM articulo_articulo), 1));
SELECT setval('usuarios_usuario_id_seq', COALESCE((SELECT MAX(id) FROM usuarios_usuario), 1));
SELECT setval('privilegios_privilegio_id_seq', COALESCE((SELECT MAX(id) FROM privilegios_privilegio), 1));
SELECT setval('categorias_categoria_id_seq', COALESCE((SELECT MAX(id) FROM categorias_categoria), 1));
SELECT setval('ventas_venta_id_seq', COALESCE((SELECT MAX(id) FROM ventas_venta), 1));
SELECT setval('articulos_1_articulo_id_seq', COALESCE((SELECT MAX(id) FROM articulos_1_articulo), 1));

-- ============================================================
-- FIN DEL BACKUP
-- ============================================================
