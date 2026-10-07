# Adds window.__dw (the 3D builder, photo reader and outfits) to a COPY of docs/index.html for the QA scripts.
# Never run it on docs/index.html itself.
import sys,re
p=sys.argv[1]; s=open(p).read()
i=s.rindex('})();\n</script>')
hook='window.__dw={figure:figure,figDefs:(typeof figDefs==="function"?figDefs:null),trueFor:trueFor,LOOK:LOOK,TRUE:TRUE,loadThree:loadThree,make3D:make3D,effPieces:effPieces,photoOf:function(id){return photoOf(byId[id]);},get fitById(){return fitById;},get fits(){return fits;}};\n'
s=s[:i]+hook+s[i:]
open(p,'w').write(s)
