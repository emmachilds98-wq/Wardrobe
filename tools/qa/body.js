// Edit Dave's other body types and cloth fits, for checking clothes on more than his saved shape.
// charFor(page source, name) gives the "dw-char" setting the page would save for that choice: one of the page's own
// body types (PRESETS: slim, average, athletic, heavier), or his saved shape with clothes "close" or "loose" (the
// Cloth fit slider at either end). "dave" (or nothing) is his saved shape, as the page starts.
//   const { charFor } = require("./qa/body"); const ch = charFor(html, "heavier");
//   await page.addInitScript(c => localStorage.setItem("dw-char", JSON.stringify(c)), ch);
// The QA scripts take it from QA_BODY (node tools/qa/zoom.js ... with QA_BODY=loose) and check_3d.js from --body.
function lit(src, name) {
  const m = src.match(new RegExp("var " + name + "=(\\{[\\s\\S]*?\\});"));
  return m ? Function("return " + m[1])() : null;
}
function names(src) { return ["dave"].concat(Object.keys(lit(src, "PRESETS") || {}).filter(k => k !== "dave"), ["close", "loose"]); }
function charFor(src, name) {
  if (!name || name === "dave") return null;
  const DEF = lit(src, "CHAR_DEF"), PRE = lit(src, "PRESETS"), KEYS = JSON.parse((src.match(/var BODY_KEYS=(\[[^\]]*\])/) || [])[1] || "[]");
  const ch = Object.assign({}, DEF);
  if (name === "close" || name === "loose") ch.clothFit = name === "close" ? -1 : 1;
  else if (PRE && PRE[name]) KEYS.forEach(k => { ch[k] = PRE[name][k] != null ? PRE[name][k] : 0; });
  else throw new Error("body is one of " + names(src).join(", "));
  return ch;
}
module.exports = { charFor, names };
