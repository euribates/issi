insert into juriscan_juriscan(id_juriscan, titulo, created, updated, checked)
values (
    5559,
    'Ley 2/1984, 11 abril, de Premios Canarias',
    current_timestamp,
    current_timestamp,
    current_timestamp
    );


insert into juriscan_juriscan(id_juriscan, titulo, created, updated, checked)
values (
    71248,
    'Ley 3/1997, 8 mayo, de Incompatibilidades de los miembros del Gobierno y altos cargos de la Administración Pública de la Comunidad Autónoma de Canarias', 
    current_timestamp,
    current_timestamp,
    current_timestamp
    );

insert into juriscan_juriscan(id_juriscan, titulo, created, updated, checked)
values (
    22137,
    'Decreto 73/1995, 7 abril, por el que se crea el Registro de Sociedades Agrarias de Transformación de Canarias',
    current_timestamp,
    current_timestamp,
    current_timestamp
    );

INSERT INTO sistemas_juriscansistema (
    id, juriscan_id, sistema_id)
VALUES (
    1, 22137, 37
);
