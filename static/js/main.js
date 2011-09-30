//
// Origin: http://www.jankoatwarpspeed.com/post/2009/08/20/Table-of-contents-using-jQuery.aspx
//
var auto_generate_toc = function() {
    // $('<div id="toc" />').append("<p>Table of Contents</p>").appendTo(document.body);

    $("h1, h2, h3, h4, h5, h6").each(function(i) {
        var cur = $(this);
        cur.attr("id", "title" + i);
    
        // var pos = cur.position().top / $("#content").height() * $(window).height();

        var id_ = "link" + i;
        var href_ = "#title" + i;
        var title = cur.attr("tagName");
        var text = cur.html();
        var element =  '<a id="' + id_ + '" href="' + href_ + '" title="' + title + '">' + text + '</a>';
        console.log(element);

        $("#toc").append(element);
    
        // $("#link" + i).css("top", pos);
    });
}

var auto_increase_width_size = function() {
    $(".auto-increase-width-size").focusin(function(evt) {
        $(this).css("width", "400px");
    });

    $(".auto-increase-width-size").focusout(function(evt) {
        $(this).css("width", "146px");
    });
}

$(document).ready(function() {
    auto_increase_width_size();

    auto_generate_toc();

    // $("p").first().text() == "[[TOC]]"
});