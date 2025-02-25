# -*- coding: utf8 -*-
import arcpy
import os
import math
from arcpy import env

# Настройки окружения
env.overwriteOutput = True
env.workspace = r"D:\KN.gdb"

def reclass_kod1(kod1):
    """Классификация кода в категории"""
    try:
        kod1 = int(kod1)
        if not 0 < kod1 < 496:
            return "error"
        
        ranges = {
            'DK': [(1, 24), (406, 406)],
            'B': [(25, 26)],
            'DP': [(27, 63), (407, 408)],
            'DPB0': [(64, 64), (371, 395), (401, 405)],
            'DPB1': [(65, 72), (82, 98), (409, 409)],
            'DPB2': [(73, 73), (99, 104), (115, 118)],
            'DPB3': [(75, 75), (119, 123)],
            'DPB4': [(74, 74), (76, 76), (105, 114), (124, 139)],
            'TPB': [(77, 81), (140, 148), (456, 493)],
            'DB1': [(149, 169), (276, 294), (410, 455)],
            'DB2': [(170, 207), (295, 298)],
            'DB3': [(208, 242), (299, 302)],
            'DB4': [(243, 245), (303, 306)],
            'TDBV': [(266, 266), (271, 271)],
            'TDBN': [(246, 249), (307, 319), (396, 396)],
            'TBV': [(267, 270), (272, 275)],
            'TBN': [(250, 265), (320, 370), (397, 400)]
        }
        
        for category, range_list in ranges.items():
            if any(start <= kod1 <= end for start, end in range_list):
                return category
        return "error"
    except (ValueError, TypeError):
        return "error"

def class_soil(kk1, kk2):
    """Расчет контрастности почвы"""
    if kk2 == "error" or kk1 not in SOIL_VALUES:
        return 0
    return SOIL_VALUES.get(kk1, {}).get(kk2, 0)

def kk_intensity(kk):
    """Определение интенсивности контрастности"""
    thresholds = [
        (float('-inf'), 1, "Не контрастный"),
        (1, 3, "Слабо контрастный"),
        (3, 5, "Средне контрастный"),
        (5, 7, "Сильно контрастный"),
        (7, float('inf'), "Крайне контрастный")
    ]
    return next(label for min_val, max_val, label in thresholds if min_val <= kk < max_val)

# Глобальный словарь для ускорения доступа
SOIL_VALUES = {
    "DK": {"DK": 0, "B": 1, "DP": 3, "DPB0": 4, "DPB1": 5, "DPB2": 6.6, "DPB3": 7.6, "DPB4": 8.6, "TPB": 9.6, "DB1": 6.6, "DB2": 7.6, "DB3": 8.6, "DB4": 9.6, "TDBV": 10.6, "TDBN": 11.6, "TBV": 12.3, "TBN": 13.3},
    "B": {"B": 0, "DK": 1, "DP": 2, "DPB0": 3, "DPB1": 4, "DPB2": 5.6, "DPB3": 6.6, "DPB4": 7.6, "TPB": 8.6, "DB1": 5.6, "DB2": 6.6, "DB3": 7.6, "DB4": 8.6, "TDBV": 9.6, "TDBN": 10.6, "TBV": 11.3, "TBN": 12.3},
    "DP": {"DP": 0, "DK": 3, "B": 2, "DPB0": 1, "DPB1": 2, "DPB2": 3.6, "DPB3": 4.6, "DPB4": 5.6, "TPB": 6.6, "DB1": 3.6, "DB2": 4.6, "DB3": 5.6, "DB4": 6.6, "TDBV": 7.6, "TDBN": 8.6, "TBV": 9.3, "TBN": 10.3},
    "DPB0": {"DPB0": 0, "DK": 4, "B": 3, "DP": 1, "DPB1": 1, "DPB2": 2.6, "DPB3": 3.6, "DPB4": 4.6, "TPB": 5.6, "DB1": 2.6, "DB2": 3.6, "DB3": 4.6, "DB4": 5.6, "TDBV": 6.6, "TDBN": 7.6, "TBV": 8.3, "TBN": 9.3},
    "DPB1": {"DPB1": 0, "DK": 5, "B": 4, "DP": 2, "DPB0": 1, "DPB2": 1, "DPB3": 2, "DPB4": 3, "TPB": 4, "DB1": 1, "DB2": 2, "DB3": 3, "DB4": 4, "TDBV": 5, "TDBN": 6, "TBV": 6.7, "TBN": 7.7},
    "DPB2": {"DPB2": 0, "DK": 6.6, "B": 5.6, "DP": 3.6, "DPB0": 2.6, "DPB1": 1, "DPB3": 1, "DPB4": 2, "TPB": 3, "DB1": 0, "DB2": 1, "DB3": 2, "DB4": 3, "TDBV": 4, "TDBN": 5, "TBV": 5.7, "TBN": 6.7},
    "DPB3": {"DPB3": 0, "DK": 7.6, "B": 6.6, "DP": 4.6, "DPB0": 3.6, "DPB1": 2, "DPB2": 1, "DPB4": 1, "TPB": 2, "DB1": 1, "DB2": 0, "DB3": 1, "DB4": 2, "TDBV": 3, "TDBN": 4, "TBV": 4.7, "TBN": 5.7},
    "DPB4": {"DPB4": 0, "DK": 8.6, "B": 7.6, "DP": 5.6, "DPB0": 4.6, "DPB1": 3, "DPB2": 2, "DPB3": 1, "TPB": 1, "DB1": 2, "DB2": 1, "DB3": 0, "DB4": 1, "TDBV": 2, "TDBN": 3, "TBV": 3.7, "TBN": 4.7},
    "TPB": {"TPB": 0, "DK": 9.6, "B": 8.6, "DP": 6.6, "DPB0": 5.6, "DPB1": 4, "DPB2": 3, "DPB3": 2, "DPB4": 1, "DB1": 3, "DB2": 2, "DB3": 1, "DB4": 0, "TDBV": 1, "TDBN": 2, "TBV": 2.7, "TBN": 3.7},
    "DB1": {"DB1": 0, "DK": 6.6, "B": 5.6, "DP": 3.6, "DPB0": 2.6, "DPB1": 1, "DPB2": 0, "DPB3": 1, "DPB4": 2, "TPB": 3, "DB2": 1, "DB3": 2, "DB4": 3, "TDBV": 4, "TDBN": 5, "TBV": 5.7, "TBN": 6.7},
    "DB2": {"DB2": 0, "DK": 7.6, "B": 6.6, "DP": 4.6, "DPB0": 3.6, "DPB1": 2, "DPB2": 1, "DPB3": 0, "DPB4": 1, "TPB": 2, "DB1": 1, "DB3": 1, "DB4": 2, "TDBV": 3, "TDBN": 4, "TBV": 4.7, "TBN": 5.7},
    "DB3": {"DB3": 0, "DK": 8.6, "B": 7.6, "DP": 5.6, "DPB0": 4.6, "DPB1": 3, "DPB2": 2, "DPB3": 1, "DPB4": 0, "TPB": 1, "DB1": 2, "DB2": 1, "DB4": 1, "TDBV": 2, "TDBN": 3, "TBV": 3.7, "TBN": 4.7},
    "DB4": {"DB4": 0, "DK": 9.6, "B": 8.6, "DP": 6.6, "DPB0": 5.6, "DPB1": 4, "DPB2": 3, "DPB3": 2, "DPB4": 1, "TPB": 0, "DB1": 3, "DB2": 2, "DB3": 1, "TDBV": 1, "TDBN": 2, "TBV": 2.7, "TBN": 3.7},
    "TDBV": {"TDBV": 0, "DK": 10.6, "B": 9.6, "DP": 7.6, "DPB0": 6.6, "DPB1": 5, "DPB2": 4, "DPB3": 3, "DPB4": 2, "TPB": 1, "DB1": 4, "DB2": 3, "DB3": 2, "DB4": 1, "TDBN": 1, "TBV": 1.7, "TBN": 2},
    "TDBN": {"TDBN": 0, "DK": 11.6, "B": 10.6, "DP": 8.6, "DPB0": 7.6, "DPB1": 6, "DPB2": 5, "DPB3": 4, "DPB4": 3, "TPB": 2, "DB1": 5, "DB2": 4, "DB3": 3, "DB4": 2, "TDBV": 1, "TBV": 0.7, "TBN": 1.7},
    "TBV": {"TBV": 0, "DK": 12.3, "B": 11.3, "DP": 9.3, "DPB0": 8.3, "DPB1": 6.7, "DPB2": 5.7, "DPB3": 4.7, "DPB4": 3.7, "TPB": 2.7, "DB1": 5.7, "DB2": 4.7, "DB3": 3.7, "DB4": 2.7, "TDBV": 1.7, "TDBN": 0.7, "TBN": 1},
    "TBN": {"TBN": 0, "DK": 13.3, "B": 12.3, "DP": 10.3, "DPB0": 9.3, "DPB1": 7.7, "DPB2": 6.7, "DPB3": 5.7, "DPB4": 4.7, "TPB": 3.7, "DB1": 6.7, "DB2": 5.7, "DB3": 4.7, "DB4": 3.7, "TDBV": 2, "TDBN": 1.7, "TBV": 1}
}

def process_feature_class(fc):
    """Обработка одного класса объектов"""
    input_soil = os.path.join(env.workspace, fc)
    out_table = os.path.join(env.workspace, f"Stat_{fc}")
    sym_stats = os.path.join(env.workspace, f"{fc}_Out")
    stats_mean_kk = os.path.join(env.workspace, f"{fc}_OutKK")

    # Создание выходной таблицы
    arcpy.CreateTable_management(env.workspace, f"Stat_{fc}")

    # Расчет КК по Юодису
    arcpy.AddGeometryAttributes_management(input_soil, "AREA", "", "HECTARES")
    arcpy.AddField_management(input_soil, "KK1", "TEXT")
    with arcpy.da.UpdateCursor(input_soil, ["KK1", "Kod1"]) as cursor:
        for row in cursor:
            row[0] = reclass_kod1(row[1])
            cursor.updateRow(row)

    arcpy.Statistics_analysis(input_soil, sym_stats, "POLY_AREA SUM", "KK1")
    with arcpy.da.SearchCursor(sym_stats, ["SUM_POLY_AREA", "KK1"]) as cursor:
        fon_soil = max(cursor, key=lambda x: x[0])
        sum_soil_area = sum(row[0] for row in cursor if row[0] is not None)

    arcpy.AddField_management(input_soil, "KK", "FLOAT")
    with arcpy.da.UpdateCursor(input_soil, ["KK", "KK1"]) as cursor:
        for row in cursor:
            row[0] = class_soil(fon_soil[1], row[1])
            cursor.updateRow(row)

    arcpy.Statistics_analysis(input_soil, stats_mean_kk, "KK MEAN;POLY_AREA SUM", "KK1")

    # Расчет KR
    arcpy.AddGeometryAttributes_management(input_soil, "AREA;PERIMETER_LENGTH", "METERS", "SQUARE_METERS")
    arcpy.AddField_management(input_soil, "KR", "FLOAT")
    with arcpy.da.UpdateCursor(input_soil, ["KR", "PERIMETER", "POLY_AREA"]) as cursor:
        for row in cursor:
            row[0] = row[1] / (2 * math.sqrt(row[2] * math.pi))
            cursor.updateRow(row)

    arcpy.AddField_management(input_soil, "Persent", "FLOAT")
    with arcpy.da.SearchCursor(input_soil, "POLY_AREA") as cursor:
        sum_soil_area_m = sum(row[0] for row in cursor if row[0] is not None)
    with arcpy.da.UpdateCursor(input_soil, ["Persent", "POLY_AREA"]) as cursor:
        for row in cursor:
            row[0] = row[1] / sum_soil_area_m if sum_soil_area_m else 0
            cursor.updateRow(row)

    # Расчет KS и KN
    with arcpy.da.SearchCursor(input_soil, ["KR", "POLY_AREA", "KK", "Persent"]) as cursor:
        data = [(row[0], row[1], row[2], row[3]) for row in cursor if all(r is not None for r in row)]
        sum_kr = sum(kr for kr, _, _, _ in data)
        max_area = max(area for _, area, _, _ in data)
        kk_uodis = sum(kk * (p * 100) for _, _, kk, p in data) / 20
        sum_area_ha = sum_soil_area_m / 10000
        ks_sum = (sum_kr * (sum_area_ha - (max_area / 10000))) / (sum_area_ha ** 2)

    with arcpy.da.SearchCursor(stats_mean_kk, ["MEAN_KK", "SUM_POLY_AREA"]) as cursor:
        kk_monitoring = sum(kk * (area / sum_area_ha) for kk, area in cursor if kk is not None and area is not None)

    kk_uodis_int = kk_intensity(kk_uodis)
    kn_uodis = ks_sum * kk_uodis
    kn_monitoring = ks_sum * kk_monitoring

    # Запись результатов
    fields = ["KK_uodis", "KK_monitoring", "KK_uodis_int", "KS_sum", "KN_uodis", "KN_monitoring", "MAX_Area", "SUM_Area", "Names"]
    for field in fields:
        arcpy.AddField_management(out_table, field, "FLOAT" if field != "KK_uodis_int" and field != "Names" else "TEXT")

    with arcpy.da.InsertCursor(out_table, fields) as cursor:
        cursor.insertRow((kk_uodis, kk_monitoring, kk_uodis_int, ks_sum, kn_uodis, kn_monitoring, max_area, sum_soil_area_m, fc))

    print(f"Processed {fc}")

def main():
    """Основная функция обработки всех полигональных классов"""
    for fc in arcpy.ListFeatureClasses("", "Polygon"):
        process_feature_class(fc)

if __name__ == "__main__":
    main()