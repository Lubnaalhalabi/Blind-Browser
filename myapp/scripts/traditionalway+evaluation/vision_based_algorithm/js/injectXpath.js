var Xpath = {};
Xpath.getElementTreeXPath = function(element) {
    var paths = [];
    for (; element && element.nodeType == Node.ELEMENT_NODE; element = element.parentNode) {
        var index = 0;
        var hasFollowingSiblings = false;
        for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
                continue;

            if (sibling.nodeName == element.nodeName)
                ++index;
        }

        for (var sibling = element.nextSibling; sibling && !hasFollowingSiblings; sibling = sibling.nextSibling) {
            if (sibling.nodeName == element.nodeName)
                hasFollowingSiblings = true;
        }

        var tagName = (element.prefix ? element.prefix + ":" : "") + element.localName;
        var pathIndex = (index || hasFollowingSiblings ? "[" + (index + 1) + "]" : "");
        paths.splice(0, 0, tagName + pathIndex);
    }

    return paths.length ? "/" + paths.join("/") : null;
};
var nodes = document.getElementsByTagName("*");
for (var i = 0; i < nodes.length; i++) {
    var attXPath = document.createAttribute("data-xpath");
    attXPath.value = Xpath.getElementTreeXPath(nodes[i]);
    nodes[i].setAttributeNode(attXPath);
}
