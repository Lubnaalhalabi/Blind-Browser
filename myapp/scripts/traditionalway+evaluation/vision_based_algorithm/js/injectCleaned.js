var nodes = document.getElementsByTagName("*");
for(var i = 0; i<nodes.length; i++)
{
    var checkspace = nodes[i].getAttribute("data-bbox").split(" ");
    var checkcss = nodes[i].getAttribute("data-style").toLowerCase();
    if(checkspace[4]==0 || checkcss.includes("display:none")|| checkcss.includes("visibility:hidden")|| checkcss.includes("hidden:true"))
    {
        var attclean = document.createAttribute("data-cleaned");
        attclean.value = "true";
        nodes[i].setAttributeNode(attclean);
    }
}