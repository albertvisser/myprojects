function subsel() {
    var s = document.getElementById("selSectie").value;
    var selects = new Array('selUser','selFunc','selTech','selTest');
    document.getElementById("txtEn").style.display = 'none';
    for (x in selects) {
        sel = selects[x];
        document.getElementById(sel).style.display = 'none';
        if (sel == s) {
            document.getElementById(sel).style.display = 'inline';
            document.getElementById("txtEn").style.display = 'inline';
        }
    }
}
function submit_form(x) {
    var s = document.getElementById(x).value;
    document.getElementById(x).form.action = s;
    document.getElementById(x).form.submit();
}
// getElementById(x).style.visiblity= visible|hidden
// getElementById(x).style.display= none|inline
