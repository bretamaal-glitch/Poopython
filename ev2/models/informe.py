from validaciones import validar_texto


class Informe:
    TIPOS: set[str] = {"empleado", "proyecto", "registro_tiempo"}

    def __init__(self, id_informe: str, tipo: str, formato: str = "PDF"):
        self.id_informe = id_informe
        self.tipo = tipo
        self.formato = formato
        self._contenido = ""

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
            opciones = ", ".join(self.TIPOS)
            raise ValueError(f"Tipo '{tipo}' no válido. Opciones permitidas: {opciones}.")
        self._tipo = tipo

    @property
    def formato(self) -> str:
        return self._formato

    @formato.setter
    def formato(self, formato: str) -> None:
        self._formato = validar_texto(formato, "formato").upper()

    @property
    def contenido(self) -> str:
        return self._contenido

    def generar(self, empleados=(), proyectos=(), registros=()) -> None:
        """Arma el texto del informe con los datos recibidos. No los guarda."""
        if self.tipo == "empleado":
            lineas = [
                f"{e.id_empleado};{e.nombre};{e.estado};"
                f"{e.departamento.nombre if e.departamento else 'Sin departamento'}"
                for e in empleados
            ]
        elif self.tipo == "proyecto":
            lineas = [
                f"{p.id_proyecto};{p.nombre};{p.fecha_inicio.isoformat()};"
                f"{len(p.empleados)} empleados"
                for p in proyectos
            ]
        else:
            lineas = [
                f"{r.id_registro};{r.fecha.isoformat()};{r.horas_trabajadas};{r.proyecto.id_proyecto}"
                for r in registros
            ]
        self._contenido = "\n".join([f"Informe {self.id_informe} ({self.tipo})", *lineas])

    def exportar(self, ruta: str) -> None:
        """Escribe el contenido en texto plano. La salida PDF requiere una librería externa."""
        if not self._contenido:
            raise ValueError("Primero debe generar el informe.")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(self._contenido)

    def __str__(self) -> str:
        return f"Informe | ID: {self.id_informe} | Tipo: {self.tipo} | Formato: {self.formato}"

    def __repr__(self) -> str:
        return f"Informe(id_informe='{self.id_informe}', tipo='{self.tipo}', formato='{self.formato}')"
