
 
CREATE TABLE users (
    id NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY,
    name VARCHAR2(50) NOT NULL,
    lastname VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    password VARCHAR2(100) NOT NULL,
    id_rol number not null, --Nuevo entry en la tabla users.
    CONSTRAINT users_pk PRIMARY KEY (id),
    CONSTRAINT email_unique UNIQUE (email)
);


-- Crear Tabla de roles. 
CREATE TABLE roles (
id_rol number primary key, 
descripcion varchar (50)
);

-- Rol 1
INSERT INTO roles (id_rol, descripcion)
VALUES (1, 'Admin');

-- Rol 2
INSERT INTO roles (id_rol, descripcion)
VALUES (1, 'User');
 
COMMIT;
SELECT * FROM USERS;



-- Crear la tabla Cliente
CREATE TABLE Cliente (
    id_cliente NUMBER PRIMARY KEY,
    Nombre VARCHAR2(50),
    Apellido VARCHAR2(50),
    Correo_electronico VARCHAR2(100),
    Contraseña VARCHAR2(50),
    Membresia VARCHAR2(20)
);


-- Cliente 1
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (2, 'Juan', 'Perez', 'juan.perez@example.com', 'clave123', 'Premium');

-- Cliente 2
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (3, 'María', 'López', 'maria.lopez@example.com', 'clave456', 'Básica');

-- Cliente 3
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (4, 'Carlos', 'González', 'carlos.gonzalez@example.com', 'clave789', 'Premium');

-- Cliente 4
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (5, 'Laura', 'Rodríguez', 'laura.rodriguez@example.com', 'claveabc', 'Básica');

-- Cliente 5
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (6, 'Daniel', 'Martínez', 'daniel.martinez@example.com', 'clave456', 'Premium');

-- Cliente 6
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (7, 'Ana', 'Sánchez', 'ana.sanchez@example.com', 'clave789', 'Básica');

-- Cliente 7
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (8, 'Pedro', 'Ramírez', 'pedro.ramirez@example.com', 'claveabc', 'Premium');

-- Cliente 8
INSERT INTO Cliente (id_cliente, Nombre, Apellido, Correo_electronico, Contraseña, Membresia)
VALUES (9, 'Isabel', 'Díaz', 'isabel.diaz@example.com', 'clave123', 'Básica');

-- Crear la tabla Factura
CREATE TABLE Factura (
    id_factura NUMBER PRIMARY KEY,
    fecha_factura DATE,
    id_cliente NUMBER,
    total NUMBER,
    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);
-- Tabla de Usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    correo_electronico VARCHAR(255),
    contrasena VARCHAR(255)
);




-- Clientes
-- Insertar nuevo cliente
CREATE OR REPLACE PROCEDURE insertar_nuevo_cliente AS
    v_id_cliente NUMBER := 1; -- Asigna un valor adecuado
    v_nombre VARCHAR2(50) := 'Juan';
    v_apellido VARCHAR2(50) := 'Pérez';
    v_correo VARCHAR2(100) := 'juan@example.com';
    v_contrasena VARCHAR2(50) := 'contraseña123';
    v_membresia VARCHAR2(20) := 'Premium';
BEGIN
    INSERT INTO Cliente VALUES (v_id_cliente, v_nombre, v_apellido, v_correo, v_contrasena, v_membresia);
    COMMIT;
END insertar_nuevo_cliente;
/



-- Actualizar cliente
CREATE OR REPLACE PROCEDURE actualizar_cliente AS
    v_id_cliente NUMBER := 1; -- Asigna el ID del cliente que deseas actualizar
    v_nuevo_nombre VARCHAR2(50) := 'NuevoNombre';
BEGINnte_y_facturas AS
    v_id_cliente NUMBER := 1; -- Asigna el ID del cliente que deseas eliminar
BEGIN
    DELETE FROM Factura WHERE id_c
    UPDATE Cliente SET Nombre = v_nuevo_nombre WHERE id_cliente = v_id_cliente;
    COMMIT;
END actualizar_cliente;
/

-- Eliminar cliente y facturas asociadas
CREATE OR REPLACE PROCEDURE eliminar_clieliente = v_id_cliente;
    DELETE FROM Cliente WHERE id_cliente = v_id_cliente;
    COMMIT;
END eliminar_cliente_y_facturas;
/

-- Consultar clientes
CREATE OR REPLACE PROCEDURE consultar_clientes AS
BEGIN
    FOR cliente IN (SELECT * FROM Cliente) LOOP
        DBMS_OUTPUT.PUT_LINE('ID Cliente: ' || cliente.id_cliente || ', Nombre: ' || cliente.Nombre || ', Apellido: ' || cliente.Apellido || ', Correo: ' || cliente.Correo || ', Membresía: ' || cliente.Membresia);
    END LOOP;
END consultar_clientes;
/

-- Facturas
CREATE OR REPLACE PROCEDURE insertar_nueva_factura (
    v_fecha_factura VARCHAR2,
    v_id_cliente NUMBER,
    v_total NUMBER
) AS
    fecha_factura DATE;
BEGIN
    -- Convertir la cadena de fecha a un tipo de dato DATE
    fecha_factura := TO_DATE(v_fecha_factura, 'YYYY-MM-DD');

    -- Insertar la nueva factura en la tabla
    INSERT INTO Factura VALUES (SEQ_FACTURA.NEXTVAL, fecha_factura, v_id_cliente, v_total);
    
    -- Realizar COMMIT para confirmar la transacción
    COMMIT;
END insertar_nueva_factura;
/
SELECT * FROM ALL_SEQUENCES WHERE SEQUENCE_NAME = 'SEQ_FACTURA';
CREATE SEQUENCE SEQ_FACTURA START WITH 1 INCREMENT BY 1;

-- Actualizar factura
CREATE OR REPLACE PROCEDURE actualizar_factura(
    p_id_factura IN NUMBER,
    p_nuevo_total IN NUMBER
) AS
BEGIN
    UPDATE Factura SET total = p_nuevo_total WHERE id_factura = p_id_factura;
    COMMIT;
END actualizar_factura;
/

-- Eliminar factura
CREATE OR REPLACE PROCEDURE eliminar_factura(p_id_factura NUMBER) AS
BEGIN
    DELETE FROM Factura WHERE id_factura = p_id_factura;
    COMMIT;
END eliminar_factura;
/

-- Consultar facturas
CREATE OR REPLACE PROCEDURE consultar_facturas AS
BEGIN
    FOR factura IN (SELECT * FROM Factura) LOOP
        DBMS_OUTPUT.PUT_LINE('ID Factura: ' || factura.id_factura || ', Fecha: ' || factura.fecha_factura || ', ID Cliente: ' || factura.id_cliente || ', Total: ' || factura.total);
    END LOOP;
END consultar_facturas;
/



-- Crea una secuencia para generar automáticamente IDs de reserva
CREATE SEQUENCE reservaciones_seq START WITH 1 INCREMENT BY 1;

-- Crea la tabla de reservaciones
CREATE TABLE reservaciones (
    reserva_id NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    fecha DATE NOT NULL  
);

-- Crea un trigger para insertar automáticamente el ID de reserva
CREATE OR REPLACE TRIGGER tr_reservaciones
BEFORE INSERT ON reservaciones
FOR EACH ROW
BEGIN
    SELECT reservaciones_seq.NEXTVAL
    INTO :NEW.reserva_id
    FROM dual;
END;
/

/// Datos de pagos 

CREATE TABLE Pagos (
    ID_pago NUMBER PRIMARY KEY,
    id_factura NUMBER REFERENCES Factura(id_factura),
    metodo_pago VARCHAR2(50),
    monto_pagado NUMBER,
    fecha_hora_pago TIMESTAMP
);
-- Modificar la definición de la columna fecha_hora_pago
ALTER TABLE Pagos MODIFY fecha_hora_pago DATE;

-- Actualizar los datos existentes al nuevo formato
UPDATE Pagos SET fecha_hora_pago = TO_DATE(TO_CHAR(fecha_hora_pago, 'YYYY-MM-DD'), 'YYYY-MM-DD');


-- Insertar un pago
CREATE OR REPLACE PROCEDURE insertar_pago(
    p_ID_pago IN NUMBER,
    p_ID_factura IN NUMBER,
    p_metodo_pago IN VARCHAR2,
    p_monto_pagado IN NUMBER,
    p_fecha_hora_pago IN TIMESTAMP
)
AS
BEGIN
    INSERT INTO Pagos(ID_pago, ID_factura, metodo_pago, monto_pagado, fecha_hora_pago)
    VALUES (p_ID_pago, p_ID_factura, p_metodo_pago, p_monto_pagado, p_fecha_hora_pago);
    COMMIT;
END insertar_pago;
/

CREATE OR REPLACE PROCEDURE actualizar_pago(
    p_ID_pago IN NUMBER,
    p_metodo_pago IN VARCHAR2,
    p_monto_pagado IN NUMBER,
    p_fecha_hora_pago_str IN VARCHAR2
)
AS
    v_fecha_hora_pago TIMESTAMP; -- Variable para almacenar la fecha y hora convertidas
BEGIN
    -- Intentar convertir la cadena a TIMESTAMP con el formato "YYYY-MM-DDTHH24:MI:SS"
    BEGIN
        v_fecha_hora_pago := TO_TIMESTAMP(p_fecha_hora_pago_str, 'YYYY-MM-DD"T"HH24:MI:SS');
    EXCEPTION
        WHEN OTHERS THEN
            -- En caso de error, imprimir la cadena de fecha y hora recibida
            DBMS_OUTPUT.PUT_LINE('Error al convertir la cadena: ' || p_fecha_hora_pago_str);
            -- Reraise para propagar la excepción original
            RAISE;
    END;

    -- Actualizar el pago
    UPDATE Pagos
    SET metodo_pago = p_metodo_pago,
        monto_pagado = p_monto_pagado,
        fecha_hora_pago = v_fecha_hora_pago
    WHERE ID_pago = p_ID_pago;

    COMMIT;
END actualizar_pago;
/

DROP PROCEDURE actualizar_pago;


-- Eliminar un pago
CREATE OR REPLACE PROCEDURE eliminar_pago(
    p_ID_pago IN NUMBER
)
AS
BEGIN
    DELETE FROM Pagos WHERE ID_pago = p_ID_pago;
    COMMIT;
END eliminar_pago;
/

-- Obtener todos los pagos
CREATE OR REPLACE FUNCTION obtener_pagos RETURN SYS_REFCURSOR
AS
    v_cursor SYS_REFCURSOR;
BEGIN
    OPEN v_cursor FOR
        SELECT * FROM Pagos;
    RETURN v_cursor;
END obtener_pagos;
/



///Datos de empleados 

///Empleados 
-- Tabla de Empleados
CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    puesto VARCHAR(255),
    fecha_contratacion DATE,
    id_usuario INT
);

--crear empleados 
CREATE OR REPLACE PROCEDURE crear_empleado(
    p_id_empleado INT,
    p_nombre VARCHAR2,
    p_apellido VARCHAR2,
    p_direccion VARCHAR2,
    p_telefono VARCHAR2,
    p_puesto VARCHAR2,
    p_fecha_contratacion DATE,
    p_id_usuario INT
)
AS
BEGIN
    INSERT INTO empleados (id_empleado, nombre, apellido, direccion, telefono, puesto, fecha_contratacion, id_usuario)
    VALUES (p_id_empleado, p_nombre, p_apellido, p_direccion, p_telefono, p_puesto, p_fecha_contratacion, p_id_usuario);
    COMMIT;
END;
/

---Actualizar un empleado 

CREATE OR REPLACE PROCEDURE actualizar_empleado(
    p_id_empleado INT,
    p_nombre VARCHAR2,
    p_apellido VARCHAR2,
    p_direccion VARCHAR2,
    p_telefono VARCHAR2,
    p_puesto VARCHAR2,
    p_fecha_contratacion DATE,
    p_id_usuario INT
)
AS
BEGIN
    UPDATE empleados
    SET nombre = p_nombre,
        apellido = p_apellido,
        direccion = p_direccion,
        telefono = p_telefono,
        puesto = p_puesto,
        fecha_contratacion = p_fecha_contratacion,
        id_usuario = p_id_usuario
    WHERE id_empleado = p_id_empleado;
    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE editar_empleado(
    p_id_empleado INT,
    p_nombre VARCHAR2,
    p_apellido VARCHAR2,
    p_direccion VARCHAR2,
    p_telefono VARCHAR2,
    p_puesto VARCHAR2,
    p_fecha_contratacion DATE,
    p_id_usuario INT
)
AS
BEGIN
    UPDATE empleados
    SET nombre = p_nombre,
        apellido = p_apellido,
        direccion = p_direccion,
        telefono = p_telefono,
        puesto = p_puesto,
        fecha_contratacion = p_fecha_contratacion,
        id_usuario = p_id_usuario
    WHERE id_empleado = TO_NUMBER(p_id_empleado);

    COMMIT;
END;
/


---Eliminar un empleado 

CREATE OR REPLACE PROCEDURE eliminar_empleado(p_id_empleado INT)
AS
BEGIN
    DELETE FROM empleados WHERE id_empleado = p_id_empleado;
    COMMIT;
END;
/


-- Insertar Empleado 1
INSERT INTO empleados VALUES (1, 'Nombre1', 'Apellido1', 'Direccion1', 'Telefono1', 'Puesto1', TO_DATE('2023-01-01', 'YYYY-MM-DD'), 101);

-- Insertar Empleado 2
INSERT INTO empleados VALUES (2, 'Nombre2', 'Apellido2', 'Direccion2', 'Telefono2', 'Puesto2', TO_DATE('2023-02-01', 'YYYY-MM-DD'), 102);

-- Insertar Empleado 3
INSERT INTO empleados VALUES (3, 'Nombre3', 'Apellido3', 'Direccion3', 'Telefono3', 'Puesto3', TO_DATE('2023-03-01', 'YYYY-MM-DD'), 103);

-- Insertar Empleado 4
INSERT INTO empleados VALUES (4, 'Nombre4', 'Apellido4', 'Direccion4', 'Telefono4', 'Puesto4', TO_DATE('2023-04-01', 'YYYY-MM-DD'), 104);



---Provedores 


CREATE TABLE Proveedor (
    ID_PROVEEDOR NUMBER PRIMARY KEY,
    NOMBRE_EMPRESA VARCHAR2(100),
    NOMBRE_CONTACTO VARCHAR2(100),
    TELEFONO VARCHAR2(20),
    CORREO_ELECTRONICO VARCHAR2(100)
);







---Procedimientos pl/sql 

-- Crear un nuevo proveedor
CREATE OR REPLACE PROCEDURE CrearProveedor(
    p_IDProveedor IN NUMBER,
    p_NombreEmpresa IN VARCHAR2,
    p_NombreContacto IN VARCHAR2,
    p_Telefono IN VARCHAR2,
    p_CorreoElectronico IN VARCHAR2
) AS
BEGIN
    INSERT INTO Proveedor (ID_PROVEEDOR, NOMBRE_EMPRESA, NOMBRE_CONTACTO, TELEFONO, CORREO_ELECTRONICO)
    VALUES (p_IDProveedor, p_NombreEmpresa, p_NombreContacto, p_Telefono, p_CorreoElectronico);
    COMMIT;
END CrearProveedor;
/

-- Obtener información de un proveedor
CREATE OR REPLACE FUNCTION ObtenerProveedor(p_IDProveedor IN NUMBER) RETURN Proveedor%ROWTYPE AS
    v_Proveedor Proveedor%ROWTYPE;
BEGIN
    SELECT * INTO v_Proveedor FROM Proveedor WHERE ID_PROVEEDOR = p_IDProveedor;
    RETURN v_Proveedor;
END ObtenerProveedor;
/

-- Actualizar información de un proveedor
CREATE OR REPLACE PROCEDURE ActualizarProveedor(
    p_IDProveedor IN NUMBER,
    p_NuevoNombreEmpresa IN VARCHAR2,
    p_NuevoNombreContacto IN VARCHAR2,
    p_NuevoTelefono IN VARCHAR2,
    p_NuevoCorreoElectronico IN VARCHAR2
) AS
BEGIN
    UPDATE Proveedor
    SET NOMBRE_EMPRESA = p_NuevoNombreEmpresa,
        NOMBRE_CONTACTO = p_NuevoNombreContacto,
        TELEFONO = p_NuevoTelefono,
        CORREO_ELECTRONICO = p_NuevoCorreoElectronico
    WHERE ID_PROVEEDOR = p_IDProveedor;
    COMMIT;
END ActualizarProveedor;
/

-- Eliminar un proveedor
CREATE OR REPLACE PROCEDURE EliminarProveedor(p_IDProveedor IN NUMBER) AS
BEGIN
    DELETE FROM Proveedor WHERE ID_PROVEEDOR = p_IDProveedor;
    COMMIT;
END EliminarProveedor;
/

--mesas
CREATE TABLE Mesas (
    ID_DE_MESA NUMBER PRIMARY KEY,
    NUMERO_DE_MESA NUMBER,
    CAPACIDAD NUMBER
);
CREATE SEQUENCE SEQ_MESAS START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE PROCEDURE CrearMesa(
    p_numero_mesa IN NUMBER,
    p_capacidad IN NUMBER
) AS
BEGIN
    INSERT INTO Mesas (ID_DE_MESA, NUMERO_DE_MESA, CAPACIDAD)
    VALUES (SEQ_MESAS.NEXTVAL, p_numero_mesa, p_capacidad);
    COMMIT;
END CrearMesa;
/

CREATE OR REPLACE FUNCTION ObtenerMesa(p_id_mesa IN NUMBER) RETURN Mesas%ROWTYPE AS
    v_mesa Mesas%ROWTYPE;
BEGIN
    SELECT *
    INTO v_mesa
    FROM Mesas
    WHERE ID_DE_MESA = p_id_mesa;

    RETURN v_mesa;
END ObtenerMesa;
/

CREATE OR REPLACE PROCEDURE ActualizarMesa(
    p_id_mesa IN NUMBER,
    p_numero_mesa IN NUMBER,
    p_capacidad IN NUMBER
) AS
BEGIN
    UPDATE Mesas
    SET
        NUMERO_DE_MESA = p_numero_mesa,
        CAPACIDAD = p_capacidad
    WHERE ID_DE_MESA = p_id_mesa;
    COMMIT;
END ActualizarMesa;
/

CREATE OR REPLACE PROCEDURE EliminarMesa(p_id_mesa IN NUMBER) AS
BEGIN
    DELETE FROM Mesas WHERE ID_DE_MESA = p_id_mesa;
    COMMIT;
END EliminarMesa;
/


--PLATILLOS

-- Crear la tabla
CREATE TABLE Platillos (
    IDPlatillo NUMBER PRIMARY KEY,
    Nombre VARCHAR2(50),
    Descripcion VARCHAR2(200),
    Precio NUMBER,
    TipoPlatillo VARCHAR2(50)
);

-- Bloque PL/SQL para INSERTAR un platillo
CREATE OR REPLACE PROCEDURE InsertarPlatillo (
    p_IDPlatillo IN NUMBER,
    p_Nombre IN VARCHAR2,
    p_Descripcion IN VARCHAR2,
    p_Precio IN NUMBER,
    p_TipoPlatillo IN VARCHAR2
) AS
BEGIN
    INSERT INTO Platillos (IDPlatillo, Nombre, Descripcion, Precio, TipoPlatillo)
    VALUES (p_IDPlatillo, p_Nombre, p_Descripcion, p_Precio, p_TipoPlatillo);
    COMMIT;
END InsertarPlatillo;

-- Bloque PL/SQL para ACTUALIZAR un platillo
CREATE OR REPLACE PROCEDURE ActualizarPlatillo (
    p_IDPlatillo IN NUMBER,
    p_Nombre IN VARCHAR2,
    p_Descripcion IN VARCHAR2,
    p_Precio IN NUMBER,
    p_TipoPlatillo IN VARCHAR2
) AS
BEGIN
    UPDATE Platillos
    SET Nombre = p_Nombre,
        Descripcion = p_Descripcion,
        Precio = p_Precio,
        TipoPlatillo = p_TipoPlatillo
    WHERE IDPlatillo = p_IDPlatillo;
    COMMIT;
END ActualizarPlatillo;

-- Bloque PL/SQL para ELIMINAR un platillo
CREATE OR REPLACE PROCEDURE EliminarPlatillo (p_IDPlatillo IN NUMBER) AS
BEGIN
    DELETE FROM Platillos WHERE IDPlatillo = p_IDPlatillo;
    COMMIT;
END EliminarPlatillo;

-- Bloque PL/SQL para OBTENER todos los platillos
CREATE OR REPLACE FUNCTION ObtenerPlatillos RETURN SYS_REFCURSOR AS
    platillos_cursor SYS_REFCURSOR;
BEGIN
    OPEN platillos_cursor FOR
        SELECT * FROM Platillos;
    RETURN platillos_cursor;
END ObtenerPlatillos;

INSERT INTO Platillos (IDPlatillo, Nombre, Descripcion, Precio, TipoPlatillo)
VALUES (1, 'Ensalada César', 'Ensalada fresca con pollo a la parrilla y aderezo César', 8.99, 'Ensalada');

INSERT INTO Platillos (IDPlatillo, Nombre, Descripcion, Precio, TipoPlatillo)
VALUES (2, 'Pizza Margarita', 'Pizza clásica con tomate, mozzarella y albahaca', 12.99, 'Pizza');

INSERT INTO Platillos (IDPlatillo, Nombre, Descripcion, Precio, TipoPlatillo)
VALUES (3, 'Pasta Alfredo', 'Pasta con salsa Alfredo y pollo', 11.99, 'Pasta');

-- Crear la tabla Pedidos
CREATE TABLE Pedidos (
    ID_pedido NUMBER PRIMARY KEY,
    Fecha_hora_pedido TIMESTAMP,
    Estado_pedido VARCHAR2(50),
    ID_cliente NUMBER,
    ID_empleado NUMBER,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado)
);

-- Crear la tabla Reseñas
CREATE TABLE Reseñas (
    ID_reseña NUMBER PRIMARY KEY,
    Comentario VARCHAR2(255),
    Calificación NUMBER,
    Fecha_reseña TIMESTAMP,
    ID_cliente NUMBER,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

--/////////////     INGREDIENTES     ///////////////

CREATE TABLE ingredientes(
id_in number primary key,
nombre_in varchar(200),
proveedor number,
precio number, 
foreign key (proveedor) references proveedor(id_proveedor)
)

--procedure para agregar ingrediente
CREATE OR REPLACE PROCEDURE INSERT_INGREDIENTE (
   id_in IN NUMBER,
   nombre_in IN VARCHAR2,
   proveedor IN NUMBER,
   precio IN NUMBER
) AS
BEGIN
   -- Check if the selected proveedor exists in the proveedores table
   DECLARE
      v_proveedor_count NUMBER;
   BEGIN
      SELECT COUNT(1) INTO v_proveedor_count FROM proveedor WHERE id_proveedor = proveedor;

      IF v_proveedor_count = 0 THEN
         -- Raise an exception if the proveedor doesn't exist
         RAISE_APPLICATION_ERROR(-20001, 'Proveedor no existe');
      END IF;
   END;

   -- The selected proveedor exists, proceed with the ingredientes insertion
   INSERT INTO ingredientes (id_in, nombre_in, proveedor, precio)
   VALUES (id_in, nombre_in, proveedor, precio);
END INSERT_INGREDIENTE;


--//editar//
CREATE OR REPLACE PROCEDURE editar_ingrediente (
    p_id_in IN NUMBER,
    p_nombre_in IN VARCHAR2,
    p_proveedor IN NUMBER,
    p_precio IN NUMBER
)
AS
BEGIN
    UPDATE ingredientes
    SET
        nombre_in = p_nombre_in,
        proveedor = p_proveedor,
        precio = p_precio
    WHERE id_in = p_id_in;
    
    COMMIT;
END editar_ingrediente;
/

--//eliminar
CREATE OR REPLACE PROCEDURE eliminar_ingrediente(i_id IN VARCHAR2) AS
BEGIN
    DELETE FROM Ingredientes WHERE id = p_id;
    COMMIT;
END eliminar_ingrediente;

--/////////////     PROMOCIONES     ///////////////

create table promociones (
id number primary key,
titulo varchar(20),
descripcion varchar(50),
fecha varchar(10),
archivo blob
)

CREATE OR REPLACE PROCEDURE eliminar_promo(p_id IN VARCHAR2) AS
BEGIN
    DELETE FROM Promociones WHERE id = p_id;
    COMMIT;
END eliminar_promo;
/

CREATE OR REPLACE PROCEDURE editar_promo(
    p_id IN VARCHAR2,
    p_titulo IN VARCHAR2,
    p_descripcion IN VARCHAR2,
    p_fecha IN VARCHAR2,
    p_archivo IN BLOB
)
IS
BEGIN
    UPDATE promociones
    SET titulo = p_titulo,
        descripcion = p_descripcion,
        fecha = p_fecha,
        archivo = p_archivo
    WHERE id = p_id;
    
    COMMIT;
END editar_promo;


-- CRUD PEDIDOS
-- CREATE
CREATE OR REPLACE PROCEDURE Insertar_Pedido(
    p_ID_pedido IN NUMBER,
    p_Fecha_hora_pedido IN TIMESTAMP,
    p_Estado_pedido IN VARCHAR2,
    p_ID_cliente IN NUMBER,
    p_ID_empleado IN NUMBER
) AS
BEGIN
    INSERT INTO Pedidos(ID_pedido, Fecha_hora_pedido, Estado_pedido, ID_cliente, ID_empleado)
    VALUES (p_ID_pedido, p_Fecha_hora_pedido, p_Estado_pedido, p_ID_cliente, p_ID_empleado);
END Insertar_Pedido;
/

-- READ
CREATE OR REPLACE FUNCTION Obtener_Pedido_3 RETURN SYS_REFCURSOR AS
    v_result SYS_REFCURSOR;
BEGIN
    OPEN v_result FOR
        SELECT * FROM Pedidos;
    RETURN v_result;
END Obtener_Pedido_3;

-- UPDATE
CREATE OR REPLACE PROCEDURE Actualizar_Pedido(
    p_ID_pedido IN NUMBER,
    p_Fecha_hora_pedido IN TIMESTAMP,
    p_Estado_pedido IN VARCHAR2,
    p_ID_cliente IN NUMBER,
    p_ID_empleado IN NUMBER
) AS
BEGIN
    UPDATE Pedidos
    SET Fecha_hora_pedido = p_Fecha_hora_pedido,
        Estado_pedido = p_Estado_pedido,
        ID_cliente = p_ID_cliente,
        ID_empleado = p_ID_empleado
    WHERE ID_pedido = p_ID_pedido;
END Actualizar_Pedido;

-- DELETE
CREATE OR REPLACE PROCEDURE Eliminar_Pedido(p_ID_pedido IN NUMBER) AS
BEGIN
    DELETE FROM Pedidos WHERE ID_pedido = p_ID_pedido;
END Eliminar_Pedido;