from .models import TipoAbono, Productos

# Definimos las reglas de recomendación
REGLAS_ABONOS = [

    # 🌱 MITACA
    # Clima frío
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 4.5<=ph<=5.2 and 35<=h<=50 and 12<=t<=18,
     "nombre":"Nutrimon produccion 17-6-18-2","fallback":"Mitaca ácido-seco (N/K con Mg)"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 5.3<=ph<=5.8 and 51<=h<=65 and 12<=t<=18,
     "nombre":"NUTRIMON 15-15-15","fallback":"Mitaca balanceado en frío"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 5.9<=ph<=6.5 and 66<=h<=80 and 12<=t<=18,
     "nombre":"Yara18-18-18","fallback":"Mitaca neutro-húmedo en frío"},

    # Clima templado
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 4.5<=ph<=5.2 and 40<=h<=55 and 19<=t<=25,
     "nombre":"Urea 46-0-0","fallback":"Mitaca ácido con N rápido"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 5.3<=ph<=5.8 and 56<=h<=70 and 19<=t<=25,
     "nombre":"YaraMila integrador 15-9-20-4","fallback":"Mitaca medio con K priorizado"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 5.9<=ph<=6.5 and 50<=h<=65 and 19<=t<=25,
     "nombre":"NUTRIMON 15-15-15","fallback":"Mitaca neutro balanceado"},

    # Clima cálido
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 4.5<=ph<=5.2 and 35<=h<=55 and 26<=t<=32,
     "nombre":"Urea 46-0-0","fallback":"Mitaca ácido-cálido (N rápido)"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 5.3<=ph<=5.8 and 51<=h<=65 and 26<=t<=32,
     "nombre":"Nutrimon produccion 17-6-18-2","fallback":"Mitaca medio cálido con Mg"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Mitaca" and 5.9<=ph<=6.5 and 66<=h<=80 and 26<=t<=32,
     "nombre":"Yara18-18-18","fallback":"Mitaca neutro cálido-húmedo"},

    # 🌾 COSECHA
    # Clima frío
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 4.5<=ph<=5.2 and 35<=h<=50 and 12<=t<=18,
     "nombre":"KATIUSKA 18 – 6 – 18 – 2 (MgO) – 2 (S)","fallback":"Cosecha ácido-seco en frío"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 5.3<=ph<=5.8 and 51<=h<=65 and 12<=t<=18,
     "nombre":"Ecofertil 25-4-24","fallback":"Cosecha potásico frío medio"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 5.9<=ph<=6.5 and 66<=h<=80 and 12<=t<=18,
     "nombre":"BONANZA 19 9 19-1(CAO)","fallback":"Cosecha balanceado frío-húmedo"},

    # Clima templado
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 4.5<=ph<=5.2 and 40<=h<=55 and 19<=t<=25,
     "nombre":"Nitrosoil 23-4-20-3","fallback":"Cosecha ácido-templado nitrogenado"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 5.3<=ph<=5.8 and 56<=h<=70 and 19<=t<=25,
     "nombre":"Yara18-18-18","fallback":"Cosecha templada balanceada"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 5.9<=ph<=6.5 and 50<=h<=65 and 19<=t<=25,
     "nombre":"Cloruro de Potasio KCL Gr 0-0-60","fallback":"Cosecha potásico templado"},

    # Clima cálido
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 4.5<=ph<=5.2 and 35<=h<=55 and 26<=t<=32,
     "nombre":"YaraVera AMIDAS 40-5-35-5.6(s)","fallback":"Cosecha ácido cálido estable"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 5.3<=ph<=5.8 and 51<=h<=65 and 26<=t<=32,
     "nombre":"Agrocosecha 26-4-22","fallback":"Cosecha N/K cálido medio"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Cosecha" and 5.9<=ph<=6.5 and 66<=h<=80 and 26<=t<=32,
     "nombre":"BONANZA 19 9 19-1(CAO)","fallback":"Cosecha cálido-húmedo balanceado"},

    # 🌿 Recuperacion
    # Clima frío
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 4.5<=ph<=5.2 and 35<=h<=50 and 12<=t<=18,
     "nombre":"NUTRIMON Sulfato de Amonio 21-0-0-24(s)","fallback":"Recuperacion ácido-seco frío"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 5.3<=ph<=5.8 and 51<=h<=65 and 12<=t<=18,
     "nombre":"REMITAL 17 – 6 – 18 + 2 (MgO)","fallback":"Recuperacion medio frío Mg"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 5.9<=ph<=6.5 and 66<=h<=80 and 12<=t<=18,
     "nombre":"YaraMila HYDROCOMPLEX 12-11-18","fallback":"Recuperacion neutro frío balanceado"},

    # Clima templado
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 4.5<=ph<=5.2 and 40<=h<=55 and 19<=t<=25,
     "nombre":"NUTRICARGA 19 – 4 – 18 – 3 (MgO) – 2 (S) – 0.1 (B) – 0.1 (Zn)","fallback":"Recuperacion ácido templado vigor"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 5.2<=ph<=5.8 and 56<=h<=70 and 19<=t<=25,
     "nombre":"EMBAJADOR KS 20-3-18-3MgO-2S-0.1Zn-0.1B","fallback":"Recuperacion medio templado micros"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 5.9<=ph<=6.5 and 50<=h<=65 and 19<=t<=25,
     "nombre":"ABOTEK 15 – 4 – 23 + 4% MgO + 2% S + 0.1% B + 0.1% Zn","fallback":"Recuperacion neutro templado con micros"},

    # Clima cálido
    {"condicion": lambda ph,h,t,temporada: temporada=="R" and 4.5<=ph<=5.2 and 35<=h<=55 and 26<=t<=32,
     "nombre":"NUTRIMON Sulfato de Amonio 21-0-0-24(s)","fallback":"Recuperacion ácido cálido estable"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 5.3<=ph<=5.8 and 51<=h<=65 and 26<=t<=32,
     "nombre":"NITRAX-S 28-4-0-6S","fallback":"Recuperacion medio cálido con azufre"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Recuperacion" and 5.9<=ph<=6.5 and 66<=h<=80 and 26<=t<=32,
     "nombre":"YaraMila HYDROCOMPLEX 12-11-18","fallback":"Recuperacion cálido-húmedo balanceado"},

    # 🌸 Florescencia
    # Clima frío
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 4.5<=ph<=5.2 and 35<=h<=50 and 12<=t<=18,
     "nombre":"Fosfato Diamónico 18-46-0","fallback":"Florescencia ácido-seco P alto"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5.3<=ph<=5.8 and 51<=h<=65 and 12<=t<=18,
     "nombre":"Nutrimon 10-20-20","fallback":"Florescencia medio frío P/K"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5.9<=ph<=6.5 and 66<=h<=80 and 12<=t<=18,
     "nombre":"Yara 10-30-10","fallback":"Florescencia neutro frío fosfatado"},
     {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5<=ph<=6 and 50<=h<=70 and 19<=t<=25,
 "nombre": "YaraMila HYDRAN 19-4-19",
 "fallback": "Floración medio templado balanceado"},

    # Clima templado
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 4.5<=ph<=5.2 and 40<=h<=55 and 19<=t<=25,
     "nombre":"NUTRIMON MicroEssentials 12-40-0-10(s)","fallback":"Florescencia ácido templado P+Zn"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5.3<=ph<=5.8 and 56<=h<=70 and 19<=t<=25,
     "nombre":"YaraMila HYDRAN 19-4-19","fallback":"Florescencia medio templado balanceado"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5.9<=ph<=6.5 and 50<=h<=65 and 19<=t<=25,
     "nombre":"YaraVita Zintrac MgB","fallback":"Florescencia neutro templado foliar Zn/Mg/B"},

    # Clima cálido
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 4.5<=ph<=5.2 and 35<=h<=55 and 26<=t<=32,
     "nombre":"Fosfato Diamónico 18-46-0","fallback":"Florescencia ácido cálido P alto"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5.3<=ph<=5.8 and 51<=h<=65 and 26<=t<=32,
     "nombre":"YaraVita CaBtrac","fallback":"Florescencia medio cálido Ca+B"},
    {"condicion": lambda ph,h,t,temporada: temporada=="Florescencia" and 5.9<=ph<=6.5 and 66<=h<=80 and 26<=t<=32,
     "nombre":"YaraMila HYDRAN 19-4-19","fallback":"Florescencia cálido-húmedo balanceado"},

    # ⚠️ CONTINGENCIAS
    {"condicion": lambda ph,h,t,temporada: ph<=4.2,
     "nombre":"NUTRIMON Sulfato de Amonio 21-0-0-24(s)","fallback":"Suelo muy ácido, considerar encalado"},
    {"condicion": lambda ph,h,t,temporada: ph>=6.6,
     "nombre":"Fosfato Diamónico 18-46-0","fallback":"Suelo alcalino, fósforo ayuda"},
    {"condicion": lambda ph,h,t,temporada: h<=34,
     "nombre":"Urea 46-0-0","fallback":"Sequía extrema, solo aplicar con lluvia"},
    {"condicion": lambda ph,h,t,temporada: t>=33,
     "nombre":"YaraVera AMIDAS 40-5-35-5.6(s)","fallback":"Calor extremo, más estable que urea"},
    {"condicion": lambda ph,h,t,temporada: t<=11,
     "nombre":"YaraMila HYDROCOMPLEX 12-11-18","fallback":"Frío extremo, balanceado eficiente"}
     
]





def recomendar_abono(ph, humedad, temperatura, temporada):
    recomendados = []
    for regla in REGLAS_ABONOS:
        if regla["condicion"](ph, humedad, temperatura, temporada):
            # Buscar en Productos
            producto = Productos.objects.filter(nombre__icontains=regla["nombre"]).first()
            if producto:
                recomendados.append(producto.nombre)
                continue
            # Buscar en TipoAbono
            abono = TipoAbono.objects.filter(nombre__icontains=regla["nombre"]).first()
            if abono:
                recomendados.append(abono.nombre)
                continue
            # Si no encontró en la BD → fallback
            recomendados.append(regla["fallback"])
    if not recomendados:
        recomendados.append("NO HAY ABONOS RECOMENDADOS PARA ESOS DATOS")
    return recomendados
