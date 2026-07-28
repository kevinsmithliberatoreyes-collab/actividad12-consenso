import time

class NodoRaft:
    def __init__(self, nodo_id):
        self.nodo_id = nodo_id
        self.estado = 'Seguidor'  # Los estados posibles: Seguidor, Candidato, Líder
        self.votos_recibidos = 0
        self.log = []
        self.activo = True

    def solicitar_votos(self, nodos):
        if not self.activo:
            return False
            
        self.estado = 'Candidato'
        self.votos_recibidos = 1  # Empieza votando por sí mismo
        print(f"[Nodo {self.nodo_id}] no detecta al líder. Iniciando elección, estado: Candidato.")

        # Pide el voto a los demás nodos
        for nodo in nodos:
            if nodo.nodo_id != self.nodo_id and nodo.activo:
                print(f"  -> Nodo {nodo.nodo_id} emite su voto a favor del Nodo {self.nodo_id}")
                self.votos_recibidos += 1

        # Si obtiene más de la mitad de los votos, gana la elección
        if self.votos_recibidos > len(nodos) // 2:
            self.estado = 'Líder'
            print(f"👑 [Nodo {self.nodo_id}] ha sido elegido LÍDER con {self.votos_recibidos} votos.")
            return True
        return False

    def replicar_dato(self, nodos, dato):
        if self.estado != 'Líder' or not self.activo:
            return
            
        print(f"\n[Líder {self.nodo_id}] Iniciando replicación del dato: '{dato}'")
        self.log.append(dato)
        confirmaciones = 1 # El líder ya lo registró en su propio log

        # Manda el dato a los seguidores
        for nodo in nodos:
            if nodo.nodo_id != self.nodo_id and nodo.activo:
                nodo.log.append(dato)
                print(f"  -> Nodo {nodo.nodo_id} replicó el dato '{dato}' exitosamente.")
                confirmaciones += 1

        # El consenso se alcanza si la mayoría lo guardó
        if confirmaciones > len(nodos) // 2:
            print(f"✅ CONSENSO ALCANZADO: El dato '{dato}' está asegurado en la mayoría de los nodos.")

def simular_raft():
    # Creamos nuestro cluster de 3 nodos
    nodos = [NodoRaft(1), NodoRaft(2), NodoRaft(3)]

    print("--- INICIO DE LA SIMULACIÓN DE CONSENSO (RAFT) ---")
    time.sleep(1)

    # 1. Elección del líder inicial
    lider_inicial = nodos[0]
    lider_inicial.solicitar_votos(nodos)
    time.sleep(1)

    # 2. Replicación de un valor simple ("A=1")
    lider_inicial.replicar_dato(nodos, "A=1")
    time.sleep(1)

    # 3. Simulación de fallo
    print("\n💥 ALERTA: Simulando caída del sistema. El Líder (Nodo 1) ha dejado de responder.")
    lider_inicial.activo = False
    time.sleep(1)

    # 4. Recuperación del consenso (Nueva elección)
    print("\n--- INICIANDO PROTOCOLO DE RECUPERACIÓN ---")
    nuevo_lider = nodos[1] # El Nodo 2 nota la caída y se postula
    nuevo_lider.solicitar_votos(nodos)
    time.sleep(1)

    # 5. El nuevo líder sigue trabajando y replica otro valor
    nuevo_lider.replicar_dato(nodos, "B=2")
    time.sleep(1)

    # Mostramos cómo quedaron los registros de cada máquina
    print("\n--- ESTADO FINAL DE LAS BITÁCORAS (LOGS) ---")
    for nodo in nodos:
        estado_actual = "Activo" if nodo.activo else "Caído"
        rol = nodo.estado if nodo.activo else "Inactivo"
        print(f"Nodo {nodo.nodo_id} ({estado_actual} - {rol}) -> Log guardado: {nodo.log}")

if __name__ == '__main__':
    simular_raft()
