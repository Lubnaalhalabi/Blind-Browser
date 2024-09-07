function getOffset(element)
{
  var bound = element.getBoundingClientRect();

  return {
    top: bound.top + window.scrollY,
    left: bound.left + window.scrollX,
    width: bound.width,
    height: bound.height
  };
}
var nodes = document.getElementsByTagName("*");
for (var i = 0; i < nodes.length; i++) {
    var att = document.createAttribute("data-bbox");
    
    var rect = nodes[i].getBoundingClientRect();
    var x = rect.left + window.scrollX;
    var y = rect.top + window.scrollY;
    var width = rect.width;
    var height = rect.height;
    var space = width * height;

    if(typeof x === 'undefined' || typeof y === 'undefined')
        {
            //var svg = document.getElementsByTagName('path')[0];
            var offset = getOffset(nodes[i]);
            var x = offset.left;
            var y = offset.top;
            var width = offset.width;
            var height = offset.height;
            var space = width*height;
        }
    att.value = "" + x + " " + y + " " + width + " " + height + " " + space;
    nodes[i].setAttributeNode(att);
}

