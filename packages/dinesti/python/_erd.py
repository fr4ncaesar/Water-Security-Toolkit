# Copyright (2013) Sandia Corporation. Under the terms of Contract# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government # retains certain rights in this software.## This software is released under the FreeBSD license as described # in License.txtimport subprocessimport _guifrom multiprocessing import Processimport tempfileimport base64import osimport json # Python 2.6 or laterdef run(sCall, sUuid, sAttribute, sSourceId, sNodeId, sTime0, sTime1, sZero, sMax, sBands):	config = _gui.getConfig()	sExe = config["config_erd_exe"]	#	doc = _gui.getDoc(sUuid)	sName = doc["name"]	#	if sCall == "static":		sNodeId = sNodeId	elif sCall == "dynamic":		sNodeId = ""	elif sCall == "dynamic1":		sNodeId = ""	elif sCall == "dynamic2":		sNodeId = ""	elif sCall == "dynamic3":		sNodeId = ""	elif sCall == "dynamic4":		sNodeId = ""	elif sCall == "dynamic5":		sNodeId = ""	else:		sNodeId = ""	#	#_gui.debugPrint("sExe=" + sExe)	#_gui.debugPrint("erd_file_name=" + sDir + sName + "/couchdb_tevasim.erd")	#_gui.debugPrint("sAttribute=" + sAttribute)	#_gui.debugPrint("sNodeId=" + sNodeId)	#_gui.debugPrint("sSourceId=" + sSourceId)	#_gui.debugPrint("sTime0=" + sTime0)	#_gui.debugPrint("sTime1=" + sTime1)	#_gui.debugPrint("sZero=" + sZero)	#_gui.debugPrint("sMax=" + sMax)	#_gui.debugPrint("nBands=" + sBands)	#	sDir = tempfile.gettempdir()	sFilename = sUuid + ".erd"	files = [sUuid + ".erd", sUuid + ".index.erd", sUuid + "-1.qual.erd", sUuid + "-1.hyd.erd"]	for file in files:		sText64 = _gui.getFile(sUuid, file)		try:			res = json.loads(sText64)			sError = res.get("error")			bError = not (sError == None)		except:			sError = ""			bError = False		if bError: break		sText = base64.b64decode(sText64)		f = open(sDir + "/" + file, "w")		f.write(sText)		f.close()	#	if bError:		sText = "{'Error':'One of the *.erd files is missing from the couch document!'}"	else:		sText = _gui.startProcess([sExe, sDir + "/" + sUuid + ".erd", sCall, sAttribute, sNodeId, sSourceId, sTime0, sTime1, sZero, sMax, sBands])	#_gui.debugPrint(len(sText))	for file in files:		_gui.removeFile(sDir + "/" + file)	return sTextdef main():	_gui.setHost()	for req in _gui.getRequests():		sDb = _gui.getQuery(req, "db")		_gui.setDatabase(sDb)		sCall      = _gui.getQuery(req, "call"          )		sUuid      = _gui.getQuery(req, "uuid"          )		sAttribute = _gui.getQuery(req, "attribute"     )		sSourceId  = _gui.getQuery(req, "sourceId"      )		sNodeId    = _gui.getQuery(req, "nodeId"        )		sTime0     = _gui.getQuery(req, "t0",       "-1")		sTime1     = _gui.getQuery(req, "t1",       "-1")		sZero      = _gui.getQuery(req, "zero",     "0" )		sMax       = _gui.getQuery(req, "max",      "0" )		sBands     = _gui.getQuery(req, "bands",    "9" )		#		sText = run(sCall, sUuid, sAttribute, sSourceId, sNodeId, sTime0, sTime1, sZero, sMax, sBands)		_gui.respondJSON(json.dumps(sText))if __name__ == "__main__":	main()