// var listColors=["#800080","#FF00FF","#000080","#0000FF","#008080","#00FFFF","#008000","#00FF00","#808000","#FFFF00","#800000","#FF0000","#000000","#808080"];


// return (function draw(left, top, width, height, path) {
// for(var i = 0; i<left.length; i++)
// {
// color=i%listColors.length
// document.body.innerHTML += "<div id='border' style='border-style:solid;border-width: thick;z-index:9999;position:absolute;color:"+listColors[i]+";left:"+left[i]+"px;top:"+top[i]+"px;height:"+height[i]+"px;width:"+width[i]+"px;'></div>"
// }

// })(arguments[0], arguments[1], arguments[2], arguments[3]);

var listColors = ["#800080", "#FF00FF", "#000080", "#0000FF", "#008080", "#00FFFF", "#008000", "#00FF00", "#808000", "#FFFF00", "#800000", "#FF0000", "#000000", "#808080"];

return (function draw(left, top, width, height, path) {
    for (var i = 0; i < left.length; i++) {
        var color = listColors[i % listColors.length];
        var element = document.evaluate(path[i], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

        if (element) {
            var tagName = element.tagName.toLowerCase();
            
            // Directly apply border
            element.style.border = 'thick solid ' + color;
            element.style.position = 'relative'; // Ensure it doesn't disrupt layout
            element.style.zIndex = '9999'; // Ensure it stays on top
        } else {
            // If the element is not found, draw an overlay div as a fallback
            var overlay = document.createElement('div');
            overlay.style.border = 'thick solid ' + color;
            overlay.style.position = 'absolute';
            overlay.style.left = left[i] + 'px';
            overlay.style.top = top[i] + 'px';
            overlay.style.width = width[i] + 'px';
            overlay.style.height = height[i] + 'px';
            overlay.style.zIndex = '9999';
            document.body.appendChild(overlay);
        }
    }
})(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4]); // pass arguments[4] for path
