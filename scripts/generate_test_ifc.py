#!/usr/bin/env python3
"""
Generate a minimal but valid IFC 2x3 file with 4 walls and a slab,
all with proper IfcExtrudedAreaSolid geometry.

Works offline — no external download required.
Output:  data/samples/test_building.ifc

Usage:
  python scripts/generate_test_ifc.py
  python scripts/generate_test_ifc.py --output path/to/out.ifc
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from textwrap import dedent


# ─── Minimal IFC 2×3 STEP text ───────────────────────────────────────────────
# One project → site → building → storey containing 4 walls + 1 slab.
# Each element has an IfcExtrudedAreaSolid representation.
# GUIDs are deterministic 22-char base64-IFC strings (valid per ISO 10303-21).
IFC_TEMPLATE = dedent("""\
    ISO-10303-21;
    HEADER;
    FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'), '2;1');
    FILE_NAME('test_building.ifc', '2024-01-01T00:00:00', ('Architex'), (''), 'IfcOpenShell', '', '');
    FILE_SCHEMA(('IFC2X3'));
    ENDSEC;
    DATA;

    /* ── Units ── */
    #1=IFCPROJECT('0AAAAAAAAAAAAAAAAAAAAAA',$,'Architex Test',$,$,$,$,(#10),#20);
    #10=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#11,$);
    #11=IFCAXIS2PLACEMENT3D(#12,$,$);
    #12=IFCCARTESIANPOINT((0.,0.,0.));
    #13=IFCDIRECTION((0.,0.,1.));
    #14=IFCDIRECTION((1.,0.,0.));
    #20=IFCUNITASSIGNMENT((#21,#22,#23));
    #21=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
    #22=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
    #23=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);

    /* ── Site → Building → Storey ── */
    #30=IFCSITE('1AAAAAAAAAAAAAAAAAAAAAA',$,'Site',$,$,#31,$,$,.ELEMENT.,$,$,$,$,$);
    #31=IFCLOCALPLACEMENT($,#32);
    #32=IFCAXIS2PLACEMENT3D(#12,$,$);
    #40=IFCBUILDING('2AAAAAAAAAAAAAAAAAAAAAA',$,'Building',$,$,#41,$,$,.ELEMENT.,$,$,$);
    #41=IFCLOCALPLACEMENT(#31,#42);
    #42=IFCAXIS2PLACEMENT3D(#12,$,$);
    #50=IFCBUILDINGSTOREY('3AAAAAAAAAAAAAAAAAAAAAA',$,'Ground Floor',$,$,#51,$,$,.ELEMENT.,0.);
    #51=IFCLOCALPLACEMENT(#41,#52);
    #52=IFCAXIS2PLACEMENT3D(#12,$,$);

    /* ── Spatial hierarchy ── */
    #90=IFCRELAGGREGATES('RAGG1AAAAAAAAAAAAAAAAAA',$,$,$,#1,(#30));
    #91=IFCRELAGGREGATES('RAGG2AAAAAAAAAAAAAAAAAA',$,$,$,#30,(#40));
    #92=IFCRELAGGREGATES('RAGG3AAAAAAAAAAAAAAAAAA',$,$,$,#40,(#50));

    /* ── Shared profile: 5 m × 0.2 m rectangle (wall cross-section) ── */
    #100=IFCRECTANGLEPROFILEDEF(.AREA.,'WallProfile',#101,5.,0.2);
    #101=IFCAXIS2PLACEMENT2D(#102,$);
    #102=IFCCARTESIANPOINT((0.,0.));

    /* ── Shared profile: 6 m × 6 m rectangle (slab) ── */
    #110=IFCRECTANGLEPROFILEDEF(.AREA.,'SlabProfile',#111,6.,6.);
    #111=IFCAXIS2PLACEMENT2D(#112,$);
    #112=IFCCARTESIANPOINT((0.,0.));

    /* ── Extrusion directions ── */
    #120=IFCDIRECTION((0.,0.,1.));   /* vertical */
    #121=IFCDIRECTION((1.,0.,0.));   /* +X */
    #122=IFCDIRECTION((0.,1.,0.));   /* +Y */

    /* ═══ Wall 1 — South (+X direction, origin 0,0,0) ═══ */
    #200=IFCWALL('WALL1AAAAAAAAAAAAAAAAAA',$,'South Wall',$,$,#201,#205,$);
    #201=IFCLOCALPLACEMENT(#51,#202);
    #202=IFCAXIS2PLACEMENT3D(#203,#120,#121);
    #203=IFCCARTESIANPOINT((0.,0.,0.));
    #205=IFCPRODUCTDEFINITIONSHAPE($,$,(#206));
    #206=IFCSHAPEREPRESENTATION(#10,'Body','SweptSolid',(#207));
    #207=IFCEXTRUDEDAREASOLID(#100,#208,#120,3.);
    #208=IFCAXIS2PLACEMENT3D(#209,$,$);
    #209=IFCCARTESIANPOINT((0.,0.,0.));

    /* ═══ Wall 2 — North (+X direction, origin 0,5,0) ═══ */
    #210=IFCWALL('WALL2AAAAAAAAAAAAAAAAAA',$,'North Wall',$,$,#211,#215,$);
    #211=IFCLOCALPLACEMENT(#51,#212);
    #212=IFCAXIS2PLACEMENT3D(#213,#120,#121);
    #213=IFCCARTESIANPOINT((0.,5.,0.));
    #215=IFCPRODUCTDEFINITIONSHAPE($,$,(#216));
    #216=IFCSHAPEREPRESENTATION(#10,'Body','SweptSolid',(#217));
    #217=IFCEXTRUDEDAREASOLID(#100,#218,#120,3.);
    #218=IFCAXIS2PLACEMENT3D(#219,$,$);
    #219=IFCCARTESIANPOINT((0.,0.,0.));

    /* ═══ Wall 3 — West (+Y direction, origin 0,0,0) ═══ */
    #220=IFCWALL('WALL3AAAAAAAAAAAAAAAAAA',$,'West Wall',$,$,#221,#225,$);
    #221=IFCLOCALPLACEMENT(#51,#222);
    #222=IFCAXIS2PLACEMENT3D(#223,#120,#122);
    #223=IFCCARTESIANPOINT((0.,0.,0.));
    #225=IFCPRODUCTDEFINITIONSHAPE($,$,(#226));
    #226=IFCSHAPEREPRESENTATION(#10,'Body','SweptSolid',(#227));
    #227=IFCEXTRUDEDAREASOLID(#100,#228,#120,3.);
    #228=IFCAXIS2PLACEMENT3D(#229,$,$);
    #229=IFCCARTESIANPOINT((0.,0.,0.));

    /* ═══ Wall 4 — East (+Y direction, origin 5,0,0) ═══ */
    #230=IFCWALL('WALL4AAAAAAAAAAAAAAAAAA',$,'East Wall',$,$,#231,#235,$);
    #231=IFCLOCALPLACEMENT(#51,#232);
    #232=IFCAXIS2PLACEMENT3D(#233,#120,#122);
    #233=IFCCARTESIANPOINT((5.,0.,0.));
    #235=IFCPRODUCTDEFINITIONSHAPE($,$,(#236));
    #236=IFCSHAPEREPRESENTATION(#10,'Body','SweptSolid',(#237));
    #237=IFCEXTRUDEDAREASOLID(#100,#238,#120,3.);
    #238=IFCAXIS2PLACEMENT3D(#239,$,$);
    #239=IFCCARTESIANPOINT((0.,0.,0.));

    /* ═══ Slab — floor (6m × 6m × 0.25m) ═══ */
    #250=IFCSLAB('SLAB1AAAAAAAAAAAAAAAAAA',$,'Ground Slab',$,$,#251,#255,$,.FLOOR.);
    #251=IFCLOCALPLACEMENT(#51,#252);
    #252=IFCAXIS2PLACEMENT3D(#253,#120,#121);
    #253=IFCCARTESIANPOINT((-0.5,-0.5,-0.25));
    #255=IFCPRODUCTDEFINITIONSHAPE($,$,(#256));
    #256=IFCSHAPEREPRESENTATION(#10,'Body','SweptSolid',(#257));
    #257=IFCEXTRUDEDAREASOLID(#110,#258,#120,0.25);
    #258=IFCAXIS2PLACEMENT3D(#259,$,$);
    #259=IFCCARTESIANPOINT((0.,0.,0.));

    /* ── Containment: all products in Ground Floor ── */
    #300=IFCRELCONTAINEDINSPATIALSTRUCTURE('CONT1AAAAAAAAAAAAAAAAAA',$,$,$,(#200,#210,#220,#230,#250),#50);

    ENDSEC;
    END-ISO-10303-21;
""")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a test IFC file for ifc_to_mesh.py")
    parser.add_argument(
        "--output",
        default="data/samples/test_building.ifc",
        help="Output path for the generated IFC file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = pathlib.Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(IFC_TEMPLATE, encoding="utf-8")

    print("[OK] Test IFC generated")
    print(f"  output:   {output}")
    print(f"  elements: 4 × IfcWall  +  1 × IfcSlab  (all with IfcExtrudedAreaSolid geometry)")
    print()
    print("Next step:")
    print(f"  python scripts/ifc_to_mesh.py --input {output} --output outputs/test_building.obj")
    return 0


if __name__ == "__main__":
    sys.exit(main())
