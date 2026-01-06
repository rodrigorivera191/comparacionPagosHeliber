# comparacionPagosHeliber

Script para comparar pagos entre dos archivos CSV: archivo del cliente y archivo del proveedor.

## Descripción

Este proyecto compara dos archivos CSV de pagos:
- **Comparacion.csv**: Archivo del cliente con pagos realizados
- **Comparacion - copia.csv**: Archivo del proveedor con pagos recibidos

El script identifica:
1. Pagos que están **solo en el archivo del cliente** pero no en el proveedor
2. Pagos que están **solo en el proveedor** pero no en el cliente
3. Considera coincidencias de pagos en el **mismo mes** aunque las fechas exactas no coincidan

## Requisitos

- Python 3.x

## Uso

Ejecutar el script de comparación:

```bash
python3 comparar_pagos.py
```

El script:
1. Carga ambos archivos CSV
2. Compara los pagos por mes y monto
3. Genera un reporte detallado mostrando:
   - Pagos solo en el cliente (no encontrados en proveedor)
   - Pagos solo en el proveedor (no encontrados en cliente)
   - Resumen con totales

## Formato de Archivos

### Comparacion.csv (Cliente)
```csv
Cuenta,Fecha,Numero,Descripcion,Monto,Tipo_de_Transferencia
23354500,26/08/2025,N-050-00000007984-026,ABONO CUENTA - ANTICIPO HELIBERT,7500000,Copapel
```

### Comparacion - copia.csv (Proveedor)
```csv
"Fecha","Valor","Medio_de_Pago"
"22/04/2025","10000000","CUENTA BANCOLOMBIA"
```

## Lógica de Comparación

El script compara pagos considerando:
- **Mes y año**: Los pagos se agrupan por mes/año
- **Monto**: El valor del pago debe coincidir exactamente
- Si dos pagos tienen el mismo mes/año y monto, se consideran el mismo pago aunque las fechas exactas difieran

## Ejemplo de Salida

```
================================================================================
REPORTE DE COMPARACIÓN DE PAGOS
================================================================================

--------------------------------------------------------------------------------
PAGOS SOLO EN CLIENTE (Comparacion.csv): 13 registros
--------------------------------------------------------------------------------
Fecha: 26/08/2025      Monto: $   7,500,000.00
  Descripción: ABONO CUENTA - ANTICIPO HELIBERT
  Tipo: Copapel                   Cuenta: 23354500

--------------------------------------------------------------------------------
PAGOS SOLO EN PROVEEDOR (Comparacion - copia.csv): 29 registros
--------------------------------------------------------------------------------
Fecha: 19/05/2025      Valor: $   2,000,000.00
  Medio de Pago: CUENTA BANCOLOMBIA

================================================================================
RESUMEN
================================================================================
Total pagos solo en cliente: 13
Total pagos solo en proveedor: 29
================================================================================
```
