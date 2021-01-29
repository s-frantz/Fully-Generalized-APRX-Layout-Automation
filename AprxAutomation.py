def AprxAutomation(pdfPath, layoutRoutines, res=300):

    def ConfigureAndExportMapPage():

        def ModifyElement():

            def ConfigureLayers(layerDict):

                def ReplaceDataSource():
                    try:
                        oldConnectionDict = thisLayer.connectionProperties
                        newConnectionDict = {'connection_info': {'database': os.path.dirname(newSourcePath)},
                                            'dataset': newSourcePath.split("\\")[-1],
                                            'workspace_factory': workspace_factory}
                        thisLayer.updateConnectionProperties(oldConnectionDict, newConnectionDict)
                    except Exception as e:
                        print(e)
                        print('Source of ' + layerName + ' could not be replaced.')

                layerList = [l.name for l in map.listLayers()]

                for layerName, layerParams in layerDict.items():

                    if layerName not in layerList:
                        arcpy.AddWarning(layerName + " could not be found in the map.")
                        continue

                    newSourcePath = layerParams[layerDictVals.index('newSourcePath')]
                    workspace_factory = layerParams[layerDictVals.index('workspace_factory')]
                    defQ = layerParams[layerDictVals.index('defQ')]

                    thisLayer    =   [l for l in map.listLayers() if l.name == layerName][0]
                    layersToRestoreAfterExport.append((thisLayer, thisLayer.visible))
                    thisLayer.visible = True

                    if newSourcePath != None:
                        ReplaceDataSource()

                    if defQ != None:
                        thisLayer.definitionQuery = defQ

                return


            if elementType.lower()=='text_element':

                element.text = fill

                if len(resize)==2:
                    size,width = resize
                    element.textSize = size
                    if element.elementWidth > width:
                        element.elementWidth = width

            elif elementType.lower()=='picture_element':

                element.sourceImage = fill
                # if a resize protocol becomes needed, write it here!

            elif elementType.lower()=='mapframe_element':

                extentPoly, extentScale = resize

                mapName = elementName.split(" Frame")[0]
                map = aprx.listMaps(mapName)[0]

                ConfigureLayers(layerDict=fill)

                if extentPoly is not None and extentScale is not None:
                    ##try:
                    ##    extentObject = extentPoly.extent
                    ##except:
                    ##    extentObject = extentPoly # sometimes it's nice to input an extent object directly
                    element.camera.setExtent(extentPoly.extent) # i think extentPoly can be a describe object!
                    element.camera.scale *= extentScale

            return


        layoutName, aprxPath = layoutSpecs
        aprx = arcpy.mp.ArcGISProject(aprxPath)
        lyt = aprx.listLayouts(layoutName)[0]
        global layersToRestoreAfterExport
        layersToRestoreAfterExport = []

        for pageElementSpecs, pageElementMod in pageRoutine.items():
            elementName, elementType = pageElementSpecs
            resize, fill = pageElementMod
            try:
                element = lyt.listElements(elementType, elementName)[0]
            except IndexError:
                raise IndexError("Could not find element type, name in layout: ", elementType, elementName)
            ModifyElement()

        arcpy.AddMessage("                      -- Exporting page "+str(pageCount))
        lyt.exportToPDF(pdfTempPage, resolution=res)
        pdfMasterObj.appendPages(pdfTempPage)
        os.remove(pdfTempPage)

        for restoration in layersToRestoreAfterExport:
            layerObject, formerVis = restoration
            arcpy.AddMessage("                       + "+ layerObject.name)  # removedis
            layerObject.visible = formerVis

        del layersToRestoreAfterExport

        return



    import arcpy, os, time

    layerDictVals   =   ['newSourcePath', 'workspace_factory', 'defQ']

    pdfDir = os.path.dirname(pdfPath)
    if not os.path.exists(pdfDir):
        os.makedirs(pdfDir)

    pdfMasterObj  =   arcpy.mp.PDFDocumentCreate(pdfPath)

    arcpy.AddMessage(time.strftime("%Y-%m-%d @ %H:%M:%S") + " -- Starting pdf automation...")

    pageCount = 0
    for layoutRoutine in layoutRoutines:
        layoutSpecs, pageRoutines = layoutRoutine
        for pageRoutine in pageRoutines:
            pageCount +=1
            pdfTempPage = os.path.join(
                os.path.dirname(pdfPath), 
                "TempPage_{}_{}.pdf".format(
                    time.strftime("%Y%m%d%H%M%S"),
                    str(pageCount)
                    )
                )
            ConfigureAndExportMapPage()

    pdfMasterObj.saveAndClose()

    arcpy.AddMessage(time.strftime("%Y-%m-%d @ %H:%M:%S") +" -- Completed pdf automation!")