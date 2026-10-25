from models.validaciones import validar_texto


class Informe:
    """
    Modelo (DTO) para la entidad Informe.
    Tabla: informe (id_informe, tipo, formato, contenido). No tiene claves foráneas:
    recibe los datos como parámetros y guarda solo el texto generado.
    """
    TIPOS: set[str] = {"empleado", "proyecto", "departamento", "registro_tiempo"}
    FORMATOS: set[str] = {"CSV"}   # CSV se abre directamente en Excel

    def __init__(self, id_informe: str, tipo: str, formato: str = "CSV", contenido: str | None = None):
        self.id_informe = id_informe
        self.tipo = tipo
        self.formato = formato
        self._contenido = contenido or ""

    @property
    def id_informe(self) -> str:
        return self._id_informe

    @id_informe.setter
    def id_informe(self, id_informe: str) -> None:
        self._id_informe = validar_texto(id_informe, "id_informe").upper()

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, tipo: str) -> None:
        if tipo not in self.TIPOS:
            opciones = ", ".join(sorted(self.TIPOS))
            raise ValueError(f"Tipo '{tipo}' no válido. Opciones permitidas: {opciones}.")
        self._tipo = tipo

    @property
    def formato(self) -> str:
        return self._formato

    @formato.setter
    def formato(self, formato: str) -> None:
        formato = validar_texto(formato, "formato").upper()
        if formato not in self.FORMATOS:
            raise ValueError(f"Formato '{formato}' no soportado. Opciones: {', '.join(sorted(self.FORMATOS))}.")
        self._formato = formato

    @property
    def contenido(self) -> str:
        return self._contenido

    @staticmethod
    def _celda(valor) -> str:
        # El separador es ';', así que se reemplaza dentro de cada celda.
        return str(valor).replace(";", ",").replace("\n", " ")

    def generar(self, empleados=(), proyectos=(), departamentos=(), registros=()) -> None:
        """Arma el texto del informe con los datos recibidos. No los guarda en la base."""
        if self.tipo == "empleado":
            encabezado = "id;nombre;estado;departamento"
            filas = [[e.id_empleado, e.nombre, e.estado,
                      e.departamento.nombre if e.departamento else "Sin departamento"] for e in empleados]
        elif self.tipo == "proyecto":
            encabezado = "id;nombre;descripcion;fecha_inicio;empleados"
            filas = [[p.id_proyecto, p.nombre, p.descripcion, p.fecha_inicio.isoformat(),
                      len(p.empleados)] for p in proyectos]
        elif self.tipo == "departamento":
            encabezado = "id;nombre;gerente;empleados"
            filas = [[d.id_departamento, d.nombre, d.gerente.nombre if d.gerente else "Sin gerente",
                      len(d.empleados)] for d in departamentos]
        else:
            encabezado = "id;fecha;horas;proyecto;empleado;descripcion"
            filas = [[r.id_registro, r.fecha.isoformat(), r.horas_trabajadas, r.proyecto.id_proyecto,
                      r.id_empleado, r.descripcion] for r in registros]
        lineas = [f"Informe {self.id_informe} ({self.tipo})", encabezado]
        lineas += [";".join(self._celda(c) for c in fila) for fila in filas]
        self._contenido = "\n".join(lineas)

    def exportar(self, ruta: str) -> None:
        """Escribe el informe en un archivo CSV (UTF-8) que Excel puede abrir."""
        if not self._contenido:
            raise ValueError("Primero debe generar el informe.")
        with open(ruta, "w", encoding="utf-8-sig", newline="") as archivo:
            archivo.write(self._contenido)

    def __str__(self) -> str:
        return f"Informe | ID: {self.id_informe} | Tipo: {self.tipo} | Formato: {self.formato}"

    def __repr__(self) -> str:
        return f"Informe(id_informe='{self.id_informe}', tipo='{self.tipo}', formato='{self.formato}')"
