# ==============================================================================
# BATERÍA DE PRUEBAS DE CASOS BORDE (Fase 3)
# ==============================================================================

import inventario

def probar_casos_borde():
    print("Iniciando pruebas de casos borde...\n")
    errores = 0

    # 1. Matriz vacía
    mat_vacia = []
    assert inventario.producto_mas_caro(mat_vacia) is None, "Error: producto_mas_caro con matriz vacía"
    assert inventario.producto_mas_barato(mat_vacia) is None, "Error: producto_mas_barato con matriz vacía"
    assert inventario.valor_total(mat_vacia) == 0.0, "Error: valor_total con matriz vacía"
    assert inventario.stock_bajo(mat_vacia, 10) == [], "Error: stock_bajo con matriz vacía"
    assert inventario.busqueda_secuencial(mat_vacia, 101) == (-1, 0), "Error: busqueda_secuencial vacía"
    assert inventario.busqueda_binaria(mat_vacia, 101) == (-1, 0), "Error: busqueda_binaria vacía"
    print("[PASS] Matriz vacía manejada correctamente.")

    # 2. Carga del CSV real
    mat = inventario.cargar_csv("inventario.csv")
    assert len(mat) >= 15, "Error: inventario.csv debe tener al menos 15 productos"
    print(f"[PASS] Carga inicial: {len(mat)} productos válidos.")

    # 3. Pruebas de ABM con datos inválidos o extremos
    # Alta con código duplicado
    assert not inventario.alta_producto(mat, 101, "Test", "Cat", 100.0, 5), "Error: permitió código duplicado"
    # Alta con precio negativo
    assert not inventario.alta_producto(mat, 999, "Test", "Cat", -50.0, 5), "Error: permitió precio negativo"
    # Alta con stock negativo
    assert not inventario.alta_producto(mat, 999, "Test", "Cat", 100.0, -2), "Error: permitió stock negativo"
    # Alta con código inválido
    assert not inventario.alta_producto(mat, -10, "Test", "Cat", 100.0, 5), "Error: permitió código negativo"
    # Alta con nombre vacío
    assert not inventario.alta_producto(mat, 999, "", "Cat", 100.0, 5), "Error: permitió nombre vacío"
    print("[PASS] Validaciones de alta_producto superadas (rechaza inválidos).")

    # 4. Modificar stock
    # Producto inexistente
    assert not inventario.modificar_stock(mat, 9999, 5), "Error: modificó producto inexistente"
    # Dejar stock negativo
    stock_actual = mat[0][4]
    assert not inventario.modificar_stock(mat, mat[0][0], -(stock_actual + 10)), "Error: permitió stock menor a 0"
    # Modificación válida (sumar y luego restar para dejar igual)
    cod_test = mat[0][0]
    assert inventario.modificar_stock(mat, cod_test, 10), "Error: falló modificación positiva de stock"
    assert inventario.modificar_stock(mat, cod_test, -10), "Error: falló modificación negativa de stock"
    print("[PASS] Modificar stock validado (rechaza negativos y no existentes).")

    # 5. Búsqueda secuencial y binaria
    inventario.ordenar_burbuja(mat, 0) # aseguramos orden por codigo
    # Primer elemento
    pos1, c1 = inventario.busqueda_secuencial(mat, mat[0][0])
    pos1_b, cb1 = inventario.busqueda_binaria(mat, mat[0][0])
    assert pos1 == 0 and pos1_b == 0, "Error buscando primer elemento"

    # Último elemento
    ultimo_idx = len(mat) - 1
    pos_u, cu = inventario.busqueda_secuencial(mat, mat[ultimo_idx][0])
    pos_ub, cub = inventario.busqueda_binaria(mat, mat[ultimo_idx][0])
    assert pos_u == ultimo_idx and pos_ub == ultimo_idx, "Error buscando último elemento"

    # Elemento inexistente
    pos_no, _ = inventario.busqueda_secuencial(mat, 99999)
    pos_nob, _ = inventario.busqueda_binaria(mat, 99999)
    assert pos_no == -1 and pos_nob == -1, "Error con elemento inexistente"
    print(f"[PASS] Búsquedas verificadas en extremos y no existentes (Secuencial y Binaria).")

    # 6. Ordenamientos (Selección, Burbuja, Inserción)
    for col in [0, 1, 3, 4]:
        copia_sel = [fila.copy() for fila in mat]
        copia_bur = [fila.copy() for fila in mat]
        copia_ins = [fila.copy() for fila in mat]

        inventario.ordenar_seleccion(copia_sel, col)
        inventario.ordenar_burbuja(copia_bur, col)
        inventario.ordenar_insercion(copia_ins, col)

        # Verificamos que queden ordenadas de menor a mayor
        for k in range(len(copia_sel) - 1):
            assert copia_sel[k][col] <= copia_sel[k + 1][col], f"Fallo orden seleccion col {col}"
            assert copia_bur[k][col] <= copia_bur[k + 1][col], f"Fallo orden burbuja col {col}"
            assert copia_ins[k][col] <= copia_ins[k + 1][col], f"Fallo orden insercion col {col}"

    print("[PASS] Los 3 métodos de ordenamiento validados en múltiples columnas.")

    # 7. Reportes
    total = inventario.valor_total(mat)
    assert total > 0, "Error: valor total debería ser positivo"
    mas_caro = inventario.producto_mas_caro(mat)
    mas_barato = inventario.producto_mas_barato(mat)
    assert mas_caro[3] >= mas_barato[3], "Error: mas_caro no puede ser menor que mas_barato"
    bajos = inventario.stock_bajo(mat, 10)
    for p in bajos:
        assert p[4] < 10, "Error: producto filtrado no cumple umbral"
    print("[PASS] Reportes de inventario verificados.")

    print("\nTODAS LAS PRUEBAS DE CASOS BORDE PASARON CON ÉXITO (0 ERRORES).")

if __name__ == "__main__":
    probar_casos_borde()
