startList = function(){
 if (document.all&&document.getElementById) {
  navRoot = document.getElementById("nav");
  for (i=0; i<navRoot.childNodes.length; i++) {
   node = navRoot.childNodes[i];
   if (node.nodeName=="LI") {
    node.onmouseover=function() {
     this.className+=" over"; }
    node.onmouseout=function() {
     this.className=this.className.replace(" over", ""); }
    for (j=0; j<node.childNodes.length; j++) {
     n2 = node.childNodes[j];
     if (n2.nodeName=="UL")             {
      for (k=0; k<n2.childNodes.length; k++) {
       n3 = n2.childNodes[k];
       if (n3.nodeName=="LI") {
        n3.onmouseover=function() {
         this.className+=" hli"; }
        n3.onmouseout=function() {
         this.className=this.className.replace(" hli", ""); } } } } } } } } }
window.onload=startList;
function selectproj()
{
    document.getElementById('subThis').disabled=false;
}
