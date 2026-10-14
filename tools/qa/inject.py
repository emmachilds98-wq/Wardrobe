# Adds window.__dw (the 3D builder, photo reader and outfits) to a COPY of docs/index.html for the QA scripts.
# Never run it on docs/index.html itself.
import sys,re
p=sys.argv[1]; s=open(p).read()
i=s.rindex('})();\n</script>')
# (its loadThree also fetches every garment template, which the page itself fetches only as an outfit needs it)
hook='window.__dw={bottomCut:(typeof bottomCut==="function"?bottomCut:null),figure:figure,figDefs:(typeof figDefs==="function"?figDefs:null),trueFor:trueFor,LOOK:LOOK,TRUE:TRUE,loadThree:function(){return loadThree().then(function(B){return Promise.all(DRAPEF.map(gtplGet)).then(function(){return B;});});},make3D:make3D,effPieces:effPieces,photoOf:function(id){return photoOf(byId[id]);},setLite:function(v){LITE3D=!!v;},get fitById(){return fitById;},get fits(){return fits;},descOf:descOf,formalOf:formalOf,derive:derive,swapOpts:swapOpts,get byId(){return byId;},wear:function(w){w=w||{};ZIPM=w.zip||"";TUCKM=w.tuck||"";TURNM=w.turn||"";}};\n'
s=s[:i]+hook+s[i:]
open(p,'w').write(s)
