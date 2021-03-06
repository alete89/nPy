# -*- coding: utf-8 -*-

import os
import sys
from . import csvdb
from . import paramFinder
from . import process
from ..gui import paramForm
import collections

if len(sys.argv) == 2:
    STARTING_PATH = sys.argv[1]
else:
    STARTING_PATH = os.getcwd()

# print "STARTING_PATH: " + str(STARTING_PATH)

CFG_PATH = STARTING_PATH + '/cfg'
TABLA_DE_SECUENCIAS_PATH = STARTING_PATH + r"/tablaDeSecuencias.csv"

# Si no hay tabla de secuencias, la creo con un ejemplo
if not os.path.isfile(TABLA_DE_SECUENCIAS_PATH):
    HEADER = "id;menu;submenu;posicion en menu;orden en secuencia;comando;loop\n"
    LINE = "1;Ejemplo;ping;1;1;ping 127.0.0.1;1"
    with open(TABLA_DE_SECUENCIAS_PATH, 'w') as nueva_tabla:
        nueva_tabla.write(HEADER)
        nueva_tabla.write(LINE)


process = process.Process()


def getTreeViewInitialPath():
    initial = getValueFromCfg('treeViewInitialPath=')
    if initial == '':
        from PyQt4 import QtCore
        initial = QtCore.QDir.rootPath()
    return initial


def getSeqTablePath():
    # el primer paso para modificar el archivo de tablaDesecuencias
    # La idea es poder seleccinar el archivo tablaDeSecuencias
    # desde la tab Environment.
    seqTablePath = getValueFromCfg('tablaDeSecuenciasPath=')
    if seqTablePath == '':
        from PyQt4 import QtCore
        seqTablePath = QtCore.QDir.rootPath()
    return seqTablePath


def getTreeViewRootPath():
    root = getValueFromCfg('treeViewRootPath=')
    if root == '':
        from PyQt4 import QtCore
        root = QtCore.QDir.rootPath()
    return root


def updateCfgPath(dirName, numLine):
    if numLine == 0:
        fullLine = 'treeViewInitialPath=' + "'" + str(dirName) + "'"
    elif numLine == 1:
        fullLine = 'treeViewRootPath=' + "'" + str(dirName) + "'"
    updateValueFromCfg(fullLine, numLine)


def getValueFromCfg(clave):
    with open(CFG_PATH, 'r') as f:
        text = f.read()
    return text.split(clave)[1].split("\n")[0].replace("'", "").replace('"', '')


def updateValueFromCfg(fullLine, nLine):
    lines = open(CFG_PATH, 'r+').read().splitlines()
    lines[nLine] = fullLine
    open(CFG_PATH, 'w').write('\n'.join(lines))


def fullDataSet(path=TABLA_DE_SECUENCIAS_PATH):
    return csvdb.getDataFromCsv(path)


def menuList(dataSet):
    distinct = csvdb.distinct(dataSet, 1)
    sortedList = csvdb.sortDataSet(distinct, 1)
    return csvdb.getColumn(sortedList, 1)


def subMenuList(menu, dataSet):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    subMenuDistinct = csvdb.distinct(subMenuFilter, 2)
    subMenuSorted = csvdb.sortDataSet(subMenuDistinct, 3)
    subMenuColumn = csvdb.getColumn(subMenuSorted, 2)
    return subMenuColumn


def idList(menu, dataSet):
    subMenuFilter = csvdb.dataFilter(dataSet, 1, menu)
    subMenuSorted = csvdb.sortDataSet(subMenuFilter, 3)
    return csvdb.getColumn(subMenuSorted, 0)


def PreEjecutarComandos(subMenu, mw):
    mw.tabWidget.setCurrentWidget(mw.tabOutputs)
    secuencia = csvdb.dataFilter(fullDataSet(), 2, subMenu)
    ordenada = csvdb.sortDataSet(secuencia, 4)

    rows_with_params = paramFinder.getParameters(ordenada)
    params = csvdb.getColumn(rows_with_params, 7)
    # print params

    comandos = csvdb.getColumn(rows_with_params, 5)

    newParams, ok = paramForm.paramForm.getNewParams(params)
    newComandos = []
    for row in comandos:  # zipear juntos los for para que no repita (posible bug)
        for old, new in zip(params, newParams):
            if isinstance(old, collections.Iterable):
                for subold, subnew in zip(old, new):
                    # evaluar reemplazar por índice de parámetro (old vs new) en lugar de por el texto
                    row = row.replace(subold, subnew)
                    row = row.replace("<", "")
                    row = row.replace(">", "")
            else:
                # evaluar reemplazar por índice de parámetro (old vs new) en lugar de por el texto
                row = row.replace(old, new)
                row = row.replace("<", "")
                row = row.replace(">", "")
        newComandos.append(row)

    # print newComandos

    loops = csvdb.getColumn(ordenada, 6)
    if ok:
        mw.terminalOutput.append("iniciando secuencia: " + subMenu)
        process.ejecutarSecuencia(newComandos, loops, mw)


def matarProceso(mw):
    process.killCurrentProcess(mw)


def getHeaders(path=TABLA_DE_SECUENCIAS_PATH):
    return csvdb.getHeader(path)


def saveTable(table, path=TABLA_DE_SECUENCIAS_PATH, header=getHeaders()):
    dataset = table.getDataSet()
    csvdb.SaveCSV(path, dataset, header)


# Si no hay archivo de configuración, lo creo en el Root
if not os.path.isfile(CFG_PATH):
    # determino el root
    root, path = os.path.splitdrive(STARTING_PATH)
    if not root:  # Windows
        root = '/'  # Unix

    with open(CFG_PATH, 'w') as cfg:
        cfg.write("treeViewInitialPath=\ntreeViewRootPath=\n")
    updateCfgPath(STARTING_PATH, 0)  # working path
    updateCfgPath(root, 1)  # Rootpath
