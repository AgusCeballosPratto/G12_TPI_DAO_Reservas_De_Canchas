#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple para verificar que la funcionalidad de checkboxes en torneos funciona
"""

import sys
import os
sys.path.insert(0, 'src')

from controller.controlador_reservas import ControladorReservas
from models.torneo import Torneo

def test_crear_torneo():
    """Test para crear un torneo con reservas seleccionadas"""
    
    print("=== Test de creación de torneo ===")
    
    # Inicializar controlador
    controlador = ControladorReservas()
    
    # Obtener reservas disponibles
    reservas = controlador.listar_reservas()
    print(f"Reservas disponibles: {len(reservas)}")
    
    if len(reservas) >= 2:
        # Simular selección de las primeras 2 reservas
        reservas_seleccionadas = [reservas[0][0], reservas[1][0]]  # IDs de las primeras 2 reservas
        
        print(f"Reservas seleccionadas para el torneo: {reservas_seleccionadas}")
        
        try:
            # Crear torneo de prueba
            torneo = Torneo("Torneo Test", "2025-11-02", "2025-11-04", "Tenis")
            controlador.crear_torneo(torneo)
            
            print("✓ Torneo creado exitosamente")
            
            # Obtener el ID del torneo recién creado
            torneos = controlador.mostrar_torneos()
            id_torneo = None
            for torneo_creado in torneos:
                if torneo_creado[1] == "Torneo Test":
                    id_torneo = torneo_creado[0]
                    break
            
            if id_torneo:
                print(f"✓ ID del torneo creado: {id_torneo}")
                
                # Asociar reservas al torneo
                from dao.reserva_dao import ReservaDAO
                reserva_dao = ReservaDAO()
                
                for reserva_id in reservas_seleccionadas:
                    reserva_dao.adjuntar_torneo(reserva_id, id_torneo)
                    print(f"✓ Reserva {reserva_id} asociada al torneo {id_torneo}")
                
                # Verificar que las reservas ahora tienen torneo asignado
                reservas_actualizadas = controlador.listar_reservas()
                for reserva in reservas_actualizadas:
                    if reserva[0] in reservas_seleccionadas:
                        print(f"✓ Reserva {reserva[0]} ahora tiene torneo_id: {reserva[8] if len(reserva) > 8 else 'N/A'}")
                
                print("\n✅ Test completado exitosamente!")
                
            else:
                print("❌ No se pudo encontrar el torneo creado")
                
        except Exception as e:
            print(f"❌ Error durante el test: {e}")
            import traceback
            traceback.print_exc()
    
    else:
        print("❌ No hay suficientes reservas para hacer el test")

if __name__ == "__main__":
    test_crear_torneo()