#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar pagos entre dos archivos CSV:
- Comparacion.csv (archivo del cliente)
- Comparacion - copia.csv (archivo del proveedor)

El script identifica:
1. Pagos que están solo en el archivo del cliente
2. Pagos que están solo en el archivo del proveedor
3. Considera coincidencias en el mismo mes aunque las fechas exactas no coincidan
"""

import csv
from datetime import datetime
from collections import defaultdict
import sys


def parse_date(date_str):
    """
    Parsea una fecha en formato DD/MM/YYYY o D/MM/YYYY o D/M/YYYY
    Retorna un objeto datetime o None si no se puede parsear
    """
    date_str = date_str.strip().strip('"')
    if not date_str:
        return None
    
    # Intentar diferentes formatos
    formats = ['%d/%m/%Y', '%d/%m/%y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def get_month_year(date_obj):
    """Retorna una tupla (mes, año) de un objeto datetime"""
    if date_obj:
        return (date_obj.month, date_obj.year)
    return None


def parse_amount(amount_str):
    """
    Parsea un monto como string y retorna un float
    """
    if not amount_str or amount_str.strip() == '':
        return None
    
    amount_str = amount_str.strip().strip('"').replace(',', '')
    try:
        return float(amount_str)
    except ValueError:
        return None


def load_client_file(filepath):
    """
    Carga el archivo del cliente (Comparacion.csv)
    Columnas: Cuenta, Fecha, Numero, Descripcion, Monto, Tipo_de_Transferencia
    """
    payments = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fecha = parse_date(row['Fecha'])
            monto = parse_amount(row['Monto'])
            
            if fecha and monto:  # Solo agregar si tiene fecha y monto válidos
                payments.append({
                    'fecha': fecha,
                    'mes_año': get_month_year(fecha),
                    'monto': monto,
                    'descripcion': row['Descripcion'].strip(),
                    'tipo': row['Tipo_de_Transferencia'].strip(),
                    'cuenta': row['Cuenta'].strip(),
                    'numero': row['Numero'].strip(),
                    'fecha_str': row['Fecha'].strip()
                })
    
    return payments


def load_provider_file(filepath):
    """
    Carga el archivo del proveedor (Comparacion - copia.csv)
    Columnas: Fecha, Valor, Medio_de_Pago
    """
    payments = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fecha = parse_date(row['Fecha'])
            valor = parse_amount(row['Valor'])
            
            if fecha and valor:  # Solo agregar si tiene fecha y valor válidos
                payments.append({
                    'fecha': fecha,
                    'mes_año': get_month_year(fecha),
                    'monto': valor,
                    'medio_pago': row['Medio_de_Pago'].strip().strip('"'),
                    'fecha_str': row['Fecha'].strip().strip('"')
                })
    
    return payments


def group_by_month_and_amount(payments):
    """
    Agrupa los pagos por mes/año y monto
    Retorna un diccionario: {(mes, año, monto): [lista de pagos]}
    """
    groups = defaultdict(list)
    for payment in payments:
        key = (payment['mes_año'][0], payment['mes_año'][1], payment['monto'])
        groups[key].append(payment)
    return groups


def compare_payments(client_payments, provider_payments):
    """
    Compara los pagos de cliente y proveedor
    Retorna dos listas:
    - only_in_client: pagos que están solo en el cliente
    - only_in_provider: pagos que están solo en el proveedor
    """
    # Agrupar pagos por mes y monto
    client_groups = group_by_month_and_amount(client_payments)
    provider_groups = group_by_month_and_amount(provider_payments)
    
    # Crear copias para marcar los que ya fueron emparejados
    client_remaining = []
    provider_remaining = []
    
    # Marcar los pagos emparejados
    matched_client = set()
    matched_provider = set()
    
    # Primero, buscar coincidencias exactas (mes, año, monto)
    for key in client_groups:
        if key in provider_groups:
            # Hay coincidencias para este mes/monto
            client_list = client_groups[key]
            provider_list = provider_groups[key]
            
            # Emparejar uno a uno hasta donde sea posible
            pairs_to_match = min(len(client_list), len(provider_list))
            
            for i in range(pairs_to_match):
                matched_client.add(id(client_list[i]))
                matched_provider.add(id(provider_list[i]))
    
    # Los no emparejados van a las listas de "solo en"
    for payment in client_payments:
        if id(payment) not in matched_client:
            client_remaining.append(payment)
    
    for payment in provider_payments:
        if id(payment) not in matched_provider:
            provider_remaining.append(payment)
    
    return client_remaining, provider_remaining


def print_report(only_in_client, only_in_provider):
    """
    Imprime el reporte de comparación
    """
    print("=" * 80)
    print("REPORTE DE COMPARACIÓN DE PAGOS")
    print("=" * 80)
    print()
    
    print("-" * 80)
    print(f"PAGOS SOLO EN CLIENTE (Comparacion.csv): {len(only_in_client)} registros")
    print("-" * 80)
    if only_in_client:
        for payment in sorted(only_in_client, key=lambda x: x['fecha']):
            print(f"Fecha: {payment['fecha_str']:<15} Monto: ${payment['monto']:>15,.2f}")
            print(f"  Descripción: {payment['descripcion']}")
            print(f"  Tipo: {payment['tipo']:<25} Cuenta: {payment['cuenta']}")
            print()
    else:
        print("No hay pagos únicos en el archivo del cliente.")
        print()
    
    print("-" * 80)
    print(f"PAGOS SOLO EN PROVEEDOR (Comparacion - copia.csv): {len(only_in_provider)} registros")
    print("-" * 80)
    if only_in_provider:
        for payment in sorted(only_in_provider, key=lambda x: x['fecha']):
            print(f"Fecha: {payment['fecha_str']:<15} Valor: ${payment['monto']:>15,.2f}")
            print(f"  Medio de Pago: {payment['medio_pago']}")
            print()
    else:
        print("No hay pagos únicos en el archivo del proveedor.")
        print()
    
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Total pagos solo en cliente: {len(only_in_client)}")
    print(f"Total pagos solo en proveedor: {len(only_in_provider)}")
    print("=" * 80)


def main():
    """
    Función principal
    """
    client_file = 'Comparacion.csv'
    provider_file = 'Comparacion - copia.csv'
    
    print(f"Cargando archivo del cliente: {client_file}")
    client_payments = load_client_file(client_file)
    print(f"  -> {len(client_payments)} pagos cargados")
    
    print(f"Cargando archivo del proveedor: {provider_file}")
    provider_payments = load_provider_file(provider_file)
    print(f"  -> {len(provider_payments)} pagos cargados")
    print()
    
    print("Comparando pagos...")
    only_in_client, only_in_provider = compare_payments(client_payments, provider_payments)
    print()
    
    print_report(only_in_client, only_in_provider)


if __name__ == '__main__':
    main()
