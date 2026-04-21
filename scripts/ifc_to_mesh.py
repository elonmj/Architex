#!/usr/bin/env python3
"""
Convert IFC geometry to mesh files (OBJ or PLY) using IfcOpenShell.

Usage examples:
  python scripts/ifc_to_mesh.py --input ./samples/model.ifc --output ./outputs/model.obj
  python scripts/ifc_to_mesh.py --input ./samples/model.ifc --output ./outputs/model.ply --limit 200
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable, List, Sequence, Tuple

import ifcopenshell
import ifcopenshell.geom


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert IFC file to OBJ or PLY mesh.")
    parser.add_argument("--input", required=True, help="Path to IFC input file")
    parser.add_argument("--output", required=True, help="Path to output mesh (.obj or .ply)")
    parser.add_argument(
        "--types",
        nargs="*",
        default=["IfcWall", "IfcSlab", "IfcColumn", "IfcBeam", "IfcDoor", "IfcWindow", "IfcRoof", "IfcStair"],
        help="IFC entity types to include (default: common architectural elements)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional max number of IFC products to process (0 = no limit)",
    )
    parser.add_argument(
        "--world-coords",
        action="store_true",
        help="Bake placements into global coordinates for easier downstream use",
    )
    return parser.parse_args()


def _triangles_from_faces(raw_faces: Sequence[int]) -> List[Tuple[int, int, int]]:
    if len(raw_faces) % 3 != 0:
        raise ValueError("Unexpected face buffer size: not divisible by 3")
    return [
        (raw_faces[i], raw_faces[i + 1], raw_faces[i + 2])
        for i in range(0, len(raw_faces), 3)
    ]


def _vertices_from_buffer(raw_vertices: Sequence[float]) -> List[Tuple[float, float, float]]:
    if len(raw_vertices) % 3 != 0:
        raise ValueError("Unexpected vertex buffer size: not divisible by 3")
    return [
        (raw_vertices[i], raw_vertices[i + 1], raw_vertices[i + 2])
        for i in range(0, len(raw_vertices), 3)
    ]


def collect_products(model: ifcopenshell.file, include_types: Iterable[str], limit: int) -> List[object]:
    products: List[object] = []
    include = [t.strip() for t in include_types if t.strip()]

    for type_name in include:
        products.extend(model.by_type(type_name))

    # Remove duplicates by GlobalId while preserving order.
    deduped: List[object] = []
    seen = set()
    for product in products:
        gid = getattr(product, "GlobalId", None)
        if not gid or gid in seen:
            continue
        seen.add(gid)
        deduped.append(product)

    if limit > 0:
        deduped = deduped[:limit]

    return deduped


def build_mesh(model: ifcopenshell.file, products: Sequence[object], world_coords: bool) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, world_coords)

    all_vertices: List[Tuple[float, float, float]] = []
    all_faces: List[Tuple[int, int, int]] = []

    for product in products:
        # Products without geometric representation are skipped.
        if not getattr(product, "Representation", None):
            continue

        try:
            shape = ifcopenshell.geom.create_shape(settings, product)
        except Exception:
            continue

        verts = _vertices_from_buffer(shape.geometry.verts)
        faces = _triangles_from_faces(shape.geometry.faces)

        if not verts or not faces:
            continue

        offset = len(all_vertices)
        all_vertices.extend(verts)
        all_faces.extend((a + offset, b + offset, c + offset) for a, b, c in faces)

    return all_vertices, all_faces


def write_obj(path: pathlib.Path, vertices: Sequence[Tuple[float, float, float]], faces: Sequence[Tuple[int, int, int]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for x, y, z in vertices:
            handle.write(f"v {x} {y} {z}\n")
        for a, b, c in faces:
            # OBJ indices are 1-based.
            handle.write(f"f {a + 1} {b + 1} {c + 1}\n")


def write_ply(path: pathlib.Path, vertices: Sequence[Tuple[float, float, float]], faces: Sequence[Tuple[int, int, int]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write("ply\n")
        handle.write("format ascii 1.0\n")
        handle.write(f"element vertex {len(vertices)}\n")
        handle.write("property float x\n")
        handle.write("property float y\n")
        handle.write("property float z\n")
        handle.write(f"element face {len(faces)}\n")
        handle.write("property list uchar int vertex_indices\n")
        handle.write("end_header\n")

        for x, y, z in vertices:
            handle.write(f"{x} {y} {z}\n")
        for a, b, c in faces:
            handle.write(f"3 {a} {b} {c}\n")


def main() -> int:
    args = parse_args()

    input_path = pathlib.Path(args.input).expanduser().resolve()
    output_path = pathlib.Path(args.output).expanduser().resolve()

    if not input_path.exists():
        print(f"[ERROR] IFC input not found: {input_path}")
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        model = ifcopenshell.open(str(input_path))
    except Exception as exc:
        print(f"[ERROR] Failed to open IFC: {exc}")
        return 3

    products = collect_products(model, args.types, args.limit)
    if not products:
        print("[ERROR] No IFC products selected. Check --types or input model content.")
        return 4

    vertices, faces = build_mesh(model, products, world_coords=args.world_coords)
    if not vertices or not faces:
        print("[ERROR] Geometry extraction produced an empty mesh.")
        return 5

    suffix = output_path.suffix.lower()
    if suffix == ".obj":
        write_obj(output_path, vertices, faces)
    elif suffix == ".ply":
        write_ply(output_path, vertices, faces)
    else:
        print("[ERROR] Output extension must be .obj or .ply")
        return 6

    print("[OK] Mesh written")
    print(f"  input:    {input_path}")
    print(f"  output:   {output_path}")
    print(f"  products: {len(products)}")
    print(f"  vertices: {len(vertices)}")
    print(f"  faces:    {len(faces)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
