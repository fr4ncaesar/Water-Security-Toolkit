# Copyright (2013) Sandia Corporation. Under the terms of Contract# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government # retains certain rights in this software.## This software is released under the FreeBSD license as described # in License.txtimport timeimport stringimport subprocessimport osimport tempfilefrom multiprocessing import Processimport _guiimport json # Python 2.6 or laterdef createTsgFile(data, duration=0):	temp = tempfile.NamedTemporaryFile(delete = False, suffix = '.tsg')	for row in data:		a0 = row.get("a0")		a1 = row.get("a1", "")		a2 = row.get("a2", 100)		a3 = row.get("a3", 0)		a4 = row.get("a4", duration)		if a1 == ""  : a1 = "FLOWPACED"		temp.write(str(a0) + "    ")		temp.write(str(a1) + "    ")		temp.write(str(a2) + "    ")		temp.write(str(a3) + "    ")		temp.write(str(a4) + "    ")		temp.write("\n")		break # only print out the first scenario in the list	return tempdef createInpFile(docFile_INP):	text = _gui.getFile(docFile_INP["docId"], docFile_INP["fileName"])	temp = tempfile.NamedTemporaryFile(delete = False, suffix='.inp')	temp.write(text)	return tempdef createSensorFile(sensors):	temp = tempfile.NamedTemporaryFile(delete = False, suffix='.sen')	bFirst = True	for row in sensors:		if row == None: continue		if bFirst:			bFirst = False			temp.write(row)		else:			temp.write("\n" + row)	return tempdef createGrabFile(nTime, locations):	temp = tempfile.NamedTemporaryFile(delete = False, suffix='.sen')	for row in locations:		if row == None: continue		temp.write("(" + row + "," + str(nTime) + ")\n")	return tempdef runExe(fINP, fWQM, fTSG, fSEN, doc, bDelTemp=None):	nStart = time.time()	sInstallDir = _gui.getInstallDir()	sUuid = doc["_id"]	sOutputPrefix = sUuid if len(sUuid) > 0 else doc["prefix"]	#	args = []	args.append(sInstallDir + "packages/sim/merlion/applications/measuregen")	args.append("--output-prefix")	args.append(sOutputPrefix)	args.append("--epanet-rpt-file")	args.append(sOutputPrefix + "_MEASURES_epanet.rpt")	if fWQM <> None:                                # try to use the water quality model file first if it exists in the couch database		args.append("--wqm")                        # if not then use the inp file		args.append(fWQM.name)	elif fINP <> None:		args.append("--inp")		args.append(fINP.name)	args.append("--tsg")	args.append(fTSG.name)	args.append("--start-sensing-time")	args.append(str(doc.get("sensorStart", 0)/60))  # default to zero	if doc.get("sensorStop") <> None:               # the last time increment can leave out the stop time		args.append("--stop-sensing-time")          # and the measuregen code knows to just spit out results		args.append(str(doc["sensorStop"]/60))      # till the end which is just one time increment	args.append("--measures-per-hour")	args.append(str(doc.get("sensorPerHour", 1)))   # default to one	args.append("--threshold")	args.append(str(doc.get("sensorThreshold", 0))) # default to zero	#args.append("--concentrations") # TODO - only for testing the "Gabe" simulation animation hack	args.append(fSEN.name)	fARG = tempfile.NamedTemporaryFile(delete = False, suffix = '.args')	for iarg in args:		fARG.write(iarg + " ")	fARG.close()	#	p = subprocess.Popen(args, stdout = subprocess.PIPE)	doc = _gui.getDoc(sUuid)	doc["pid"] = str(p.pid)	doc["status"] = "Running"	_gui.setDoc(sUuid, doc)	doc = _gui.getDoc(sUuid)	com = p.communicate()	sOut = com[0]	#	#_gui.raiseDebugError("stopping to retrieve json file from the tmp directory")	sfile = sOutputPrefix + "_MEASURES.json"	if os.path.exists(sfile):		f = open(sfile,"r")		results = json.load(f)	else:		results = {"Error": "the results file was not found"}	#	doc = _gui.getDoc(sUuid)	doc["results"] = results	doc["debug_fileTSG"] = str(fTSG.name)	doc["debug_stdout"] = com[0]	doc["returnCode"] = p.returncode	if com[1] == None:		doc["debug_stderr"] = "\0"	else:		doc["debug_stderr"] = com[1]	#	sKill = "Signal handler called from"	index = string.find(sOut, sKill)	doc["debug_stdout_find_error_index"] = index	#	bDelTemp = doc.get("deleteTempFiles", bDelTemp)	if _gui.bDeleteTempFiles(override=bDelTemp):		_gui.removeFiles([fINP, fWQM, fTSG, fSEN, fARG])		_gui.removeFile(sOutputPrefix + "_MEASURES.log")		_gui.removeFile(sOutputPrefix + "_MEASURES.json")		_gui.removeFile(sOutputPrefix + "_MEASURES.dat")		_gui.removeFile(sOutputPrefix + "_MEASURES_epanet.rpt")	#	if index == -1 and 	p.returncode == 0:		doc["status"] = "Complete"	elif index == -1:		doc["status"] = "Error"	else:		doc["status"] = "Stopped"	#	doc["timer"] = time.time() - nStart	_gui.setDoc(sUuid, doc)	return docdef runThreaded(doc, sOutputPrefix, sDir, bThreaded=True):	sUuid = doc.get("_id")	if sUuid == None: return {"Error": "couch document doesnt contain _id key.", "doc": doc}	sInstallDir = _gui.getConfig("config_install_dir")	#	inp_info = doc["docFile_INP"]	tsg_info = doc["input_TSG"]	duration = inp_info["duration"]	fINP = createInpFile(inp_info)	fWQM = _gui.createWqmFile(inp_info)	fTSG = createTsgFile(tsg_info, duration)	fSEN = createSensorFile(doc["sensorList"])	_gui.closeFiles([fINP, fWQM, fTSG, fSEN])	#	if bThreaded:		p = Process(target=runExe, args=(fINP, fWQM, fTSG, fSEN, doc, None))		p.start()		return {}	else:		return runExe(fINP, fWQM, fTSG, fSEN, doc, None)	returndef run(sCall, sUuid, bThreaded=True):	if sCall == "rename":		return False	if sCall == "delete":		return False	sDir = tempfile.gettempdir()	os.chdir(sDir)	doc = _gui.getDoc(sUuid)	retVal = runThreaded(doc, sUuid, sDir, True)	retVal["call"] = sCall	retVal["uuid"] = sUuid	retVal["py"  ] = "_measure"	return _gui.respondJSON(json.dumps(retVal))def main():	_gui.setHost()	for req in _gui.getRequests():		sDb = _gui.getQuery(req, "db")		_gui.setDatabase(sDb)		sCall = _gui.getQuery(req, "call")		sUuid = _gui.getQuery(req, "uuid")		bRetVal = run(sCall, sUuid, True)		if bRetVal: continue		_gui.respondJSON(json.dumps({"db": sDb, "call": sCall, "uuid": sUuid}))if __name__ == "__main__":	main()