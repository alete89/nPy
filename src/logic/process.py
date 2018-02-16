# -*- coding: utf-8 -*-

# Default
import sys
from PyQt4 import QtCore

if sys.platform == "win32":
    # Windows only
    from .winstructs import WinProcInfo
    import ctypes


class Process():
    def __init__(self):
        self.proc = QtCore.QProcess()
        self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.proc.setReadChannelMode(QtCore.QProcess.MergedChannels)
        self.proc.finished.connect(self.processJustFinished)
        self.proc.readyRead.connect(self.hayParaEscribir)

        self.secuencia = []
        self.MainWindowInstance = None
        self.current_process = ""

    def ejecutarSecuencia(self, comandos, parametros, iteraciones, mw):
        self.MainWindowInstance = mw
        for i, _ in enumerate(comandos):
            instruccion = dict(
                comando=comandos[i], parametro=parametros[i], iteraciones=iteraciones[i])
            self.secuencia.append(instruccion)
        self.runNow()

    def runNow(self):
        if not self.secuencia:
            return
        instruccion = self.secuencia[0]
        if int(instruccion['iteraciones']) == 0:  # Iteraciones restantes
            # Si no hay más iteraciones, la saco de la lista.
            del self.secuencia[0]
            self.runNow()
        else:  # Quedan iteraciones
            instruccion['iteraciones'] = str(
                int(instruccion['iteraciones']) - 1)  # Iteraciones -1
            self.current_process = instruccion['comando']
            self.MainWindowInstance.showOutputInTerminal(
                "iniciando proceso: " + self.current_process)
            if not instruccion['parametro']:  # Si no hay parámetros
                self.proc.start(instruccion['comando'])  # lanzo sin parámetros
            else:
                # lanzo con parámetros
                self.proc.start(
                    instruccion['comando'], instruccion['parametro'])

    def hayParaEscribir(self):
        output = self.proc.readAll().data()
        self.MainWindowInstance.showOutputInTerminal(output)

    def getPid(self):
        try:
            if sys.platform == 'win32':
                LPWinProcInfo = ctypes.POINTER(WinProcInfo)
                struct = ctypes.cast(int(self.proc.pid()), LPWinProcInfo)
                pid = struct.contents.dwProcessID
            else:
                pid = int(self.proc.pid())
            return pid
        except TypeError:
            return "No hay proceso corriendo"

    def killCurrentProcess(self, mw):
        mw.showOutputInTerminal(str(self.getPid()))
        self.proc.kill()

    def processJustFinished(self):
        self.MainWindowInstance.showOutputInTerminal(
            "fin de proceso: " + self.current_process)
        self.runNow()