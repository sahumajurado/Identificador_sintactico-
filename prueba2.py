def identificador():
    # Lista con conjugaciones del verbo ser/estar
    verbo_estar_ser = [
        "soy", "eres", "es", "somos", "sois", "son",  # Presente (Ser)
        "estoy", "estás", "está", "estamos", "estáis", "están",  # Presente (Estar)
        "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron",  # Pretérito Perfecto Simple (Ser)
        "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron",  # Pretérito Perfecto Simple (Estar)
        "era", "eras", "era", "éramos", "erais", "eran",  # Pretérito Imperfecto (Ser)
        "estaba", "estabas", "estaba", "estábamos", "estabais", "estaban",  # Pretérito Imperfecto (Estar)
        "seré", "serás", "será", "seremos", "seréis", "serán",  # Futuro del Indicativo (ser)
        "estaré", "estarás", "estará", "estaremos", "estaréis", "estarán",  # Futuro del Indicativo (Estar)
        "sido",  # Pretérito Perfecto Compuesto (Ser)
        "estado",  # Pretérito Perfecto Compuesto, pretérito pluscuamperfecto (Estar)
        "sido"]  # Pretérito Pluscuamperfecto (Ser)

    # Lista de terminaciones regulares del participio regular
    terminaciones_regulares = ["ado", "ados", "ada", "adas", "idos", "ido", "idas", "idos", "idas", "idos", "iendo", "ando", "ida"]

    # Lista de terminaciones irregulares del participio irregular
    terminaciones_irregulares = ["cho", "lto", "sto", "to", "scho", "rto", "sisto", "rcho",
                                 "visto", "ccho", "chcho", "mcho", "lcho", "so", "tos", "sos",
                                 "ta", "sa", "cha", "tas", "sas", "chas"]

    # Ingresar la oración
    oracion = input("Ingresar una oración: ")
    palabras = oracion.split()

    for i in range(len(palabras) - 1):
        palabra1, palabra2 = palabras[i], palabras[i + 1]

        # Verificar si la primera palabra es un verbo de ser/estar
        if palabra1.lower() in verbo_estar_ser:

            # Verificar las terminaciones de la segunda palabra
            for terminacion_regular in terminaciones_regulares:
                if palabra2.lower().endswith(terminacion_regular) and len(palabra2) >= len(terminacion_regular):
                    print("La oración ingresada es una oración pasiva regular.")
                    return

            for terminacion_irregular in terminaciones_irregulares:
                if palabra2.lower().endswith(terminacion_irregular) and len(palabra2) >= len(terminacion_irregular):
                    print("La oración ingresada es una oración pasiva irregular.")
                    return

    print("La oración no es una oración pasiva.")

# Llamada a la función
identificador()
