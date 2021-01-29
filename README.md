# Fully-Generalized-APRX-Layout-Automation

Function accepts a configuration structure, of the format discussed below.

This function can be used to fully customize and export page-based maps with text, analysis figures, etc. into a PDF book.

Example "layoutRoutines" object and function call is below:

        aprx = r"C:\Users\silas.frantz\Desktop\_SHORTCUTS\_APRX\PD_OA.aprx" if ThisUser(
                ) == 'silas.frantz' else r"\\ace-ra-fs1\data\GIS\_Prospects\_APRX\PD_OA.aprx"
        layout = "Parcel Dissolve Layout"

        pageConfigs = [
            ( #Layout Routine 1
            (layout, aprx), (
                { #Page 1 - inAOI
                ("Title", "Text_Element"):(
                    (),
                    pDict['name'] + "\n" +
                    pDict['county'] + ", " + pDict['state'] + "\n" +
                    "Parcel Dissolves - Top Owners" + "\n"
                    "In AOI by Tax Address"),
                ("DEM", "Picture_Element"):(
                    None,
                    micro_legend),
                ("Inset Frame", "Mapframe_Element"):(
                    (polyWM, 6.0),
                    {}),
                ("Parcel Dissolve Frame", "Mapframe_Element"):(
                    (polyWM, 1.15),
                    {'This AOI':[None, None, pDict['defQ1']],
                     'Parcels In':[outPolyFc, 'File Geodatabase', None]})
                },
                { #Page 2 - outAOI
                ("Title", "Text_Element"):(
                    (),
                    pDict['name'] + "\n" +
                    pDict['county'] + ", " + pDict['state'] + "\n" +
                    "Parcel Dissolves - Top Owners" + "\n"
                    "In " + "Buffer" if posbuff>0 else "County" + " by Tax Address"),
                ("DEM", "Picture_Element"):(
                    None,
                    macro_legend),
                ("Inset Frame", "Mapframe_Element"):(
                    (polyWM, 6.0),
                    {}),
                ("Parcel Dissolve Frame", "Mapframe_Element"):(
                    (outPolyExtentPolyWM, 0.95),
                    {'This AOI':[None, None, pDict['defQ1']],
                     'Parcels Out':[outPolyFc, 'File Geodatabase', None]})
                }
                ,)
                ,)
                ]

        AprxAutomation(outPdfX, pageConfigs, res=96)
