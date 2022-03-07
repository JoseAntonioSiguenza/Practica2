import math
import pandas as pd
from math import e
def hola_f(hola):
    print('hola')


def Richford_Rice(F, T, P, compuestos_u, comp, v_prima):
    compuestos = ["metano", 'etileno', 'etano', 'propileno',
                  'propano', 'isobutano', 'n-butano', 'isopentano',
                  'n-pentano', 'n-hexano', 'n-heptano', 'n-octano',
                  'n-nonano', 'n-decano']
    # PUEDO METER TODO ESTO EN UN DICCIONARIO
    met_prop = [1.955, 11, 6.077]
    pent_prop = [6.16, 39.66, 30.33]
    hexa_prop = [6.896, 45.58, 39.29]
    # PUEDO METER TODO ESTO EN UN DICCIONARIO
    for i in range(len(comp)):
        comp[i] = float(comp[i])
    d_const = {'metano': [-292860, 0, 8.2445, -0.8951, 59.8465, 0],
               'etileno': [-600076.875, 0, 7.90595, -0.84677, 42.94594, 0],
               'etano': [-687248.25, 0, 7.90694, -0.88600, 49.02654, 0],
               'propileno': [-923484.6875, 0, 7.71725, -0.87871, 47.67624, 0],
               'propano': [-970688.5625, 0, 7.15059, -0.76984, 0, 6.90224],
               'isobutano': [-1166846, 0, 7.72668, -0.92213, 0, 0],
               'n-butano': [-1280557, 0, 7.94986, -0.96455, 0, 0],
               'isopentano': [-1481583, 0, 7.58071, -0.93159, 0, 0],
               'n-pentano': [-1524891, 0, 7.33129, -0.89143, 0, 0],
               'n-hexano': [-1778901, 0, 6.96783, -0.84634, 0, 0],
               'n-heptano': [-2013803, 0, 6.52914, -0.79543, 0, 0],
               'n-octano': [0, -7646.81641, 12.48457, -0.73152, 0, 0],
               'n-nonano': [-2551040, 0, 5.96313, -0.67818, 0, 0],
               'n-decano': [0, -9760.45703, 13.80354, -0.71470, 0, 0]}
    met = [25.416469359478626, 4.8832938718957255, 0.2]
    pent = [0.24083326739343747, -0.34162502967295316, 0.45]
    hexa = [0.0937883528265127, -0.31717407651072055, 0.35]
    d_ki = {}
    for key in d_const:
        ki = 0
        ki = e ** ((d_const[key][0] / (T ** 2)) + (d_const[key][1] / (T ** 1)) + (d_const[key][2]) + (
                    d_const[key][3] * math.log(P)) + (d_const[key][4] / (P ** 2)) + (d_const[key][5] / (P ** 1)))
        d_ki[key] = [ki]
    ki = []
    for i in range(len(compuestos_u)):
        ki.append(d_ki[compuestos_u[i]])
    ec = []
    print('Resultados:')
    for i in range(len(comp)):
        ec_1 = (((ki[i][0]) - 1) * comp[i])
        ec_2 = ((ki[i][0] - 1) * v_prima) + 1
        ec_3 = ec_1 / ec_2
        ec.append(ec_3)
    # REFACTORIZAR PARA QUE SI EL VALOR DE sum(ec) es muy alto, el paso se ajuste a 0.01 por ejemplo
    count = 0
    if sum(ec) < 0:
        while abs(sum(ec)) > 0.0001:
            ec = []
            ecs = []
            v_prima -= 0.00001
            for i in range(len(comp)):
                ec_1 = (((ki[i][0]) - 1) * comp[i])
                ec_2 = ((ki[i][0] - 1) * v_prima) + 1
                ec_3 = ec_1 / ec_2
                ec.append(ec_3)
                ecs.append([ec_1, ec_2, ec_3])
            count += 1
        print("El valor de v' fue", v_prima, 'y se necesitaron', count, 'iteraciones')
    else:
        while abs(sum(ec)) > 0.0001:
            ec = []
            ecs = []
            v_prima += 0.00001
            for i in range(len(comp)):
                ec_1 = (((ki[i][0]) - 1) * comp[i])
                ec_2 = ((ki[i][0] - 1) * v_prima) + 1
                ec_3 = ec_1 / ec_2
                ec.append(ec_3)
                ecs.append([ec_1, ec_2, ec_3])

            count += 1
        print("El valor de v' fue", v_prima, 'y se necesitaron', count, 'iteraciones')
    xi, yi, k_is = [], [], []
    for i in range(len(comp)):
        xi.append(((comp[i] / ecs[i][1])))
        yi.append((xi[i] * ki[i][0]))  # REVISA MANANA
        k_is.append(round(ki[i][0] * 100) / 100)
    df = pd.DataFrame({'zi': comp,
                       'ki': k_is,
                       'xi': xi,
                       'yi': yi}, index=compuestos_u)
    print(' ')
    print(df)
    print(' ')
    print('∑ xi =', sum(xi), '∑ yi =', sum(yi))
    V = round((F * v_prima) * 100) / 100
    L = round((F - (F * v_prima)) * 100) / 100
    print('F =', F, 'kgmol/h, V =', V, 'kgmol/h y L =', L, 'kgmol/h')
    # DEFINIR FUNCION PARA CALCULAR V,L y el balnce de energía
    # def destilador_adiabatico(F):

    T_alimen = (T - 491.67) * 5 / 9
    T_flash = T_alimen + 0.1
    hv = yi[0] * (met_prop[0] + met_prop[2] * (T_flash - T_alimen)) \
         + yi[1] * (pent_prop[0] + pent_prop[2] * (T_flash - T_alimen)) \
         + yi[2] * (hexa_prop[0] + hexa_prop[2] * (T_flash - T_alimen))
    print('hv: ', hv)
    hl = xi[0] * (met_prop[1] * (T_flash - T_alimen)) \
         + xi[1] * (pent_prop[1] * (T_flash - T_alimen)) \
         + xi[2] * (hexa_prop[1] * (T_flash - T_alimen))
    print('hl: ', hl)
    hf = met[2] * (met_prop[1] * (T_flash - T_alimen)) \
         + pent[2] * (pent_prop[1] * (T_flash - T_alimen)) \
         + hexa[2] * (hexa_prop[1] * (T_flash - T_alimen))
    print('hf: ', hf)
    print('')
    ## Balance de energía
    bal = (V * hv) + (L * hl) - (F * hf)
    print('El balance dio', bal, 'kJ/h')
    acum = 0
    if bal < 0:
        while bal < 0.0001:
            T_flash -= 0.00001
            # for i in range(len(comp)):
            hv = yi[0] * (met_prop[0] + met_prop[2] * (T_flash - T_alimen)) \
                 + yi[1] * (pent_prop[0] + pent_prop[2] * (T_flash - T_alimen)) \
                 + yi[2] * (hexa_prop[0] + hexa_prop[2] * (T_flash - T_alimen))
            hl = xi[0] * (met_prop[1] * (T_flash - T_alimen)) \
                 + xi[1] * (pent_prop[1] * (T_flash - T_alimen)) \
                 + xi[2] * (hexa_prop[1] * (T_flash - T_alimen))
            hf = met[2] * (met_prop[1] * (T_flash - T_alimen)) \
                 + pent[2] * (pent_prop[1] * (T_flash - T_alimen)) \
                 + hexa[2] * (hexa_prop[1] * (T_flash - T_alimen))
            bal = (V * hv) + (L * hl) - (F * hf)
            acum += 1
        print("El valor del balance fue de ", bal, 'kJ/h, el valor de la temperatura de operación del flash fue de ',
              T_flash, '˚C y se necesitaron', acum, 'iteraciones')

    else:
        while bal > 0.0001:
            T_flash += 0.00001
            # for i in range(len(comp)):
            hv = yi[0] * (met_prop[0] + met_prop[2] * (T_flash - T_alimen)) \
                 + yi[1] * (pent_prop[0] + pent_prop[2] * (T_flash - T_alimen)) \
                 + yi[2] * (hexa_prop[0] + hexa_prop[2] * (T_flash - T_alimen))
            hl = xi[0] * (met_prop[1] * (T_flash - T_alimen)) \
                 + xi[1] * (pent_prop[1] * (T_flash - T_alimen)) \
                 + xi[2] * (hexa_prop[1] * (T_flash - T_alimen))
            hf = met[2] * (met_prop[1] * (T_flash - T_alimen)) \
                 + pent[2] * (pent_prop[1] * (T_flash - T_alimen)) \
                 + hexa[2] * (hexa_prop[1] * (T_flash - T_alimen))
            bal = (V * hv) + (L * hl) - (F * hf)
            acum += 1
        print("El valor del balance fue de ", bal, 'kJ/h\nEl valor de la temperatura de operación del flash fue de ',
              T_flash, '˚C y se necesitaron', acum, 'iteraciones')
print("hola mundo")