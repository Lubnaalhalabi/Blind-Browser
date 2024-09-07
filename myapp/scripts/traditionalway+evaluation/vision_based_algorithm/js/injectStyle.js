var nodes = document.getElementsByTagName("*");
for (var i = 0; i < nodes.length; i++) {
    var attStyle = document.createAttribute("data-style");
    var css = window.getComputedStyle(nodes[i]);
    var cssAtts = "";
    for (var j = 0; j < css.length; j++) {
        var val = css[j] + ":" + css.getPropertyValue("" + css[j]);
        cssAtts += val + ";";
    }
    attStyle.value = cssAtts;
    nodes[i].setAttributeNode(attStyle);
}
