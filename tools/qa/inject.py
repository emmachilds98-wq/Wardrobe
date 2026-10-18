# Adds window.__dw (the 3D builder, photo reader and outfits) to a COPY of docs/index.html for the QA scripts.
# Never run it on docs/index.html itself.
import sys,re
p=sys.argv[1]; s=open(p).read()
i=s.rindex('})();\n</script>')
hook='window.__dw={pose:(typeof poseRig==="function"?{rig:poseRig,solve:poseSolve,apply:poseApply,rest:poseSkinRest,mix:poseMix}:null),drapeArch:(typeof drapeArch==="function"?drapeArch:null),hoodOn:(typeof hoodOn==="function"?hoodOn:null),get GTPL(){return typeof GTPL==="undefined"?null:GTPL;},set GTPL(v){GTPL=v;},garmentsFor:(typeof garmentsFor==="function"?garmentsFor:null),bottomCut:(typeof bottomCut==="function"?bottomCut:null),figure:figure,figDefs:(typeof figDefs==="function"?figDefs:null),trueFor:trueFor,LOOK:LOOK,TRUE:TRUE,loadThree:loadThree,make3D:make3D,effPieces:effPieces,photoOf:function(id){return photoOf(byId[id]);},setLite:function(v){LITE3D=!!v;},get fitById(){return fitById;},get fits(){return fits;},descOf:descOf,formalOf:formalOf,derive:derive,swapOpts:swapOpts,get byId(){return byId;},wear:function(w){w=w||{};ZIPM=w.zip||"";TUCKM=w.tuck||"";TURNM=w.turn||"";}};\n'
s=s[:i]+hook+s[i:]
open(p,'w').write(s)
