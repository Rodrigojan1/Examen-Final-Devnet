import requests

API_KEY = "6d55bc3f-2455-4371-ade9-a0bbe75783a2"

print("=== RUTA ENTRE CHILE Y ARGENTINA ===")

while True:
    origen = input("Ciudad de Origen (o v para salir): ")

    if origen.lower() == "v":
        print("Programa finalizado.")
        break

    destino = input("Ciudad de Destino: ")

    print("\nSeleccione medio de transporte:")
    print("1. Automóvil")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Opción: ")

    if opcion == "1":
        perfil = "car"
    elif opcion == "2":
        perfil = "bike"
    elif opcion == "3":
        perfil = "foot"
    else:
        print("Opción no válida.")
        continue

    # Obtener coordenadas de las ciudades
    def obtener_coordenadas(ciudad):
        url = "https://graphhopper.com/api/1/geocode"

        parametros = {
            "q": ciudad,
            "locale": "es",
            "limit": 1,
            "key": API_KEY
        }

        respuesta = requests.get(url, params=parametros)
        datos = respuesta.json()

        if not datos.get("hits"):
            return None

        return (
            datos["hits"][0]["point"]["lat"],
            datos["hits"][0]["point"]["lng"]
        )

    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)

    if coord_origen is None or coord_destino is None:
        print("No fue posible encontrar una de las ciudades.")
        continue

    # Solicitar la ruta
    url = "https://graphhopper.com/api/1/route"

    parametros = {
        "point": [
            f"{coord_origen[0]},{coord_origen[1]}",
            f"{coord_destino[0]},{coord_destino[1]}"
        ],
        "profile": perfil,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)
    datos = respuesta.json()

    if "paths" not in datos:
        print("No fue posible calcular la ruta.")
        continue

    ruta = datos["paths"][0]

    kilometros = ruta["distance"] / 1000
    millas = kilometros * 0.621371
    minutos = ruta["time"] / 60000

    horas = int(minutos // 60)
    minutos_restantes = int(minutos % 60)

    print("\n=== RESULTADO DEL VIAJE ===")
    print(f"Ciudad de Origen: {origen}")
    print(f"Ciudad de Destino: {destino}")
    print(f"Distancia: {kilometros:.2f} km")
    print(f"Distancia: {millas:.2f} millas")
    print(
        f"Duración aproximada: "
        f"{horas} horas y {minutos_restantes} minutos"
    )

    print("\n=== NARRATIVA DEL VIAJE ===")

    for instruccion in ruta["instructions"]:
        print("-", instruccion["text"])

    print()