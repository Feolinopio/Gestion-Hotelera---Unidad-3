
from datetime import date

class Habitacion:
    def __init__(self, numero, precio, foto):
        self.numero = numero
        self.precio = precio
        self.foto = foto
        self.disponible = True

    def mostrarFoto(self):
        print("Mostrando foto de la habitación", self.numero, ":", self.foto)


class Sencilla(Habitacion):
    def __init__(self, numero, precio, foto, exterior=True):
        Habitacion.__init__(self, numero, precio, foto)
        self.exterior = exterior


class Doble(Habitacion):
    def __init__(self, numero, precio, foto, tipoCama="matrimonial"):
        Habitacion.__init__(self, numero, precio, foto)
        self.tipoCama = tipoCama


class Suite(Habitacion):
    def __init__(self, numero, precio, foto, banera=False, sauna=False, mirador=False):
        Habitacion.__init__(self, numero, precio, foto)
        self.banera = banera
        self.sauna = sauna
        self.mirador = mirador


class Cliente:
    def __init__(self, nombre, direccion, telefono):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono


class Habitual(Cliente):
    def __init__(self, nombre, direccion, telefono, descuento=10.0):
        Cliente.__init__(self, nombre, direccion, telefono)
        self.descuento = descuento


class Esporadico(Cliente):
    def __init__(self, nombre, direccion, telefono, recibirOfertas=True):
        Cliente.__init__(self, nombre, direccion, telefono)
        self.recibirOfertas = recibirOfertas


class Reserva:
    def __init__(self, cliente, habitacion, fechaEntrada, dias):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fechaEntrada = fechaEntrada
        self.dias = dias


class Hotel:
    def __init__(self, nombre, estrellas):
        self.nombre = nombre
        self.estrellas = estrellas
        self.habitaciones = []
        self.reservas = []

    def agregarHabitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def listarDisponibles(self, tipo=None):
        disponibles = []
        for h in self.habitaciones:
            if h.disponible:
                if tipo is None:
                    disponibles.append(h)
                else:
                    if isinstance(h, tipo):
                        disponibles.append(h)
        return disponibles

    def precioPorTipo(self, tipo):
        for h in self.habitaciones:
            if isinstance(h, tipo):
                return h.precio
        return None

    def cambiarPrecio(self, tipo, nuevoPrecio):
        cambios = 0
        for h in self.habitaciones:
            if isinstance(h, tipo):
                h.precio = nuevoPrecio
                cambios += 1
        return cambios

    def reservar(self, numero, cliente, fechaEntrada, dias):
        for h in self.habitaciones:
            if h.numero == numero and h.disponible:
                h.disponible = False
                reserva = Reserva(cliente, h, fechaEntrada, dias)
                self.reservas.append(reserva)
                return reserva
        return None


def calcularPrecioConDescuento(precioBase, porcentaje):
    return precioBase * (1 - (porcentaje / 100.0))


def esClienteHabitual(telefono, listaTelefonosHabituales):
    return telefono in listaTelefonosHabituales


def leerCliente(listaTelefonosHabituales, descuentoHabitual=12.0):
    print("\n=== Datos del cliente ===")
    nombre = input("Nombre: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()

    if esClienteHabitual(telefono, listaTelefonosHabituales):
        print("Cliente habitual detectado.")
        return Habitual(nombre, direccion, telefono, descuento=descuentoHabitual)
    else:
        print("Cliente esporádico, informar de las promociones que maneja el hotel.")
        return Esporadico(nombre, direccion, telefono, recibirOfertas=True)


def elegirTipoHabitacion():
    print("\nTipos: sencilla / doble / suite")
    t = input("Tipo de habitación: ").strip().lower()
    if t not in ("sencilla", "doble", "suite"):
        print("Tipo inválido.")
        return None
    return t


def pedirOpcionesHabitacion(tipo):
    """
    Devuelve un diccionario con las opciones elegidas según el tipo:
    - sencilla: interior/exterior
    - doble: matrimonial/mixta
    - suite: banera/sauna/mirador (sí/no)
    """
    if tipo == "sencilla":
        val = input("¿Desea EXTERIOR? (s/n) [s = exterior, n = interior]: ").strip().lower()
        exterior = (val == "s")
        return {"exterior": exterior}

    elif tipo == "doble":
        val = input("Tipo de cama (matrimonial/mixta): ").strip().lower()
        if val not in ("matrimonial", "mixta"):
            print("Opción inválida, se usará 'matrimonial' por defecto.")
            val = "matrimonial"
        return {"tipoCama": val}

    elif tipo == "suite":
        b = input("¿Bañera? (s/n): ").strip().lower() == "s"
        s = input("¿Sauna? (s/n): ").strip().lower() == "s"
        m = input("¿Mirador? (s/n): ").strip().lower() == "s"
        return {"banera": b, "sauna": s, "mirador": m}

    return {}


def formatearPrecio(v):
    try:
        return "${:,.0f}".format(float(v))
    except:
        return "$" + str(v)


def mostrarListaDisponibles(hotel, tipoClase=None):
    lista = hotel.listarDisponibles(tipoClase)
    if len(lista) == 0:
        print("No hay habitaciones disponibles para ese criterio.")
        return
    print("\nDisponibles:")
    for h in lista:
        clase = h.__class__.__name__
        estado = "DISPONIBLE" if h.disponible else "OCUPADA"
        print("-", clase, "#"+str(h.numero), "— precio:", formatearPrecio(h.precio), "—", estado)


def obtenerClasePorTexto(texto):
    if texto == "sencilla":
        return Sencilla
    if texto == "doble":
        return Doble
    if texto == "suite":
        return Suite
    return None


def main():
    hotel = Hotel("Hotel Cacique Toné", 4)

    hotel.agregarHabitacion(Sencilla(101, 150000, "foto101.jpg", exterior=True))  
    hotel.agregarHabitacion(Sencilla(102, 145000, "foto102.jpg", exterior=False)) 

    hotel.agregarHabitacion(Doble(201, 240000, "foto201.jpg", tipoCama="matrimonial"))
    hotel.agregarHabitacion(Doble(202, 230000, "foto202.jpg", tipoCama="mixta"))

    hotel.agregarHabitacion(Suite(301, 420000, "foto301.jpg", banera=True, sauna=False, mirador=True))
    hotel.agregarHabitacion(Suite(302, 450000, "foto302.jpg", banera=True, sauna=True, mirador=False))

    telefonosHabituales = {"3001234567", "3210000000", "3111111111"}
    descuentoHabitual = 12.0 

    while True:
        print("\n=== Gestión Hotelera — Hotel Cacique Toné ===")
        print("1) Listar habitaciones disponibles por tipo")
        print("2) Consultar precio por tipo (considera cliente habitual/esporádico)")
        print("3) Reservar habitación por número (considera habitual/descuento)")
        print("4) Cambiar precio por tipo")
        print("0) Salir")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("¡Hasta luego!")
            break

        elif opcion == "1":
            t = elegirTipoHabitacion()
            if t is None:
                continue
            clase = obtenerClasePorTexto(t)
            mostrarListaDisponibles(hotel, clase)

        elif opcion == "2":
            cliente = leerCliente(telefonosHabituales, descuentoHabitual)

            t = elegirTipoHabitacion()
            if t is None:
                continue
            clase = obtenerClasePorTexto(t)
            precio = hotel.precioPorTipo(clase)
            if precio is None:
                print("No hay habitaciones de ese tipo en el sistema.")
                continue

            if isinstance(cliente, Habitual):
                precioFinal = calcularPrecioConDescuento(precio, cliente.descuento)
                print("Precio base para", clase.__name__, ":", formatearPrecio(precio))
                print("Cliente habitual con descuento de", str(cliente.descuento)+"%",
                      "=> Precio final:", formatearPrecio(precioFinal))
            else:
                print("Cliente esporádico, informar de las promociones que maneja el hotel.")
                print("Precio para", clase.__name__, ":", formatearPrecio(precio))

        elif opcion == "3":
            cliente = leerCliente(telefonosHabituales, descuentoHabitual)

            numeroTxt = input("Número de habitación a reservar: ").strip()
            diasTxt = input("Número de días: ").strip()
            if not numeroTxt.isdigit() or not diasTxt.isdigit():
                print("Entrada inválida.")
                continue

            numero = int(numeroTxt)
            dias = int(diasTxt)

            reserva = hotel.reservar(numero, cliente, date.today(), dias)
            if reserva is None:
                print("No se pudo reservar: número inválido o no disponible.")
                continue

            precioBase = reserva.habitacion.precio
            if isinstance(cliente, Habitual):
                precioFinal = calcularPrecioConDescuento(precioBase, cliente.descuento)
                print("Reserva confirmada para", cliente.nombre, "en habitación #"+str(numero), "por", dias, "día(s).")
                print("Precio base:", formatearPrecio(precioBase),
                      "=> Descuento", str(cliente.descuento)+"%",
                      "=> Precio final:", formatearPrecio(precioFinal))
            else:
                print("Cliente esporádico, informar de las promociones que maneja el hotel.")
                print("Reserva confirmada para", cliente.nombre, "en habitación #"+str(numero), "por", dias, "día(s).")
                print("Precio:", formatearPrecio(precioBase))

        elif opcion == "4":
            t = elegirTipoHabitacion()
            if t is None:
                continue
            clase = obtenerClasePorTexto(t)

            nuevoTxt = input("Nuevo precio: ").strip()
            try:
                nuevo = float(nuevoTxt)
            except:
                print("Precio inválido.")
                continue

            n = hotel.cambiarPrecio(clase, nuevo)
            if n == 0:
                print("No se encontraron habitaciones de ese tipo para actualizar.")
            else:
                print("Precio actualizado para", n, "habitación(es)", clase.__name__, "a", formatearPrecio(nuevo))

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
