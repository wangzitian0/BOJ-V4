function changeFrameHeight(ifmid){
    var ifm= document.getElementById(ifmid);
    var subWeb = document.frames ? document.frames["iframepage"].document :
    ifm.contentDocument;
    if(ifm != null && subWeb != null) {
        ifm.height = subWeb.body.scrollHeight;
    }
}

function activateTag(tagid){
    var tag= document.getElementById(tagid);
    tag.setAttribute("class", "active");
}