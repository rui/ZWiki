//
// This TOC implementation is inspired by Janko Jovanovic,
// http://www.jankoatwarpspeed.com/post/2009/08/20/Table-of-contents-using-jQuery.aspx
//
var auto_generate_toc = function() {
    var toc_element = $("#content p:first");
    if (toc_element != undefined && toc_element.html() != "[[TOC]]") {
        var headers_list = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        if (!headers_list.length) {
            return;
        }
    } else {
        toc_element.hide();
    }


    var toc_element = $("#toc");
    if (!toc_element.length) {
        $("#content").before(
            $('<div id="toc" class="draggable" />').append('<p>Table of Contents</p><ul />')
        );

        $(".draggable").draggable();
    }


    $("h1, h2, h3, h4, h5, h6").each(function(i) {
        var cur = $(this);
        cur.attr("id", "title" + i);
    
        // var pos = cur.position().top / $("#content").height() * $(window).height();

        var id_ = "link" + i;
        var class_ = cur[0].tagName.toLowerCase();
        var href_ = "#title" + i;
        //var title = cur.attr("tagName");
        var title = cur.html();
        var text = cur.html();
        var element =  '<li><a id="' + id_ + '" class="' + class_ + '" href="' + href_ + '" title="' + title + '">' + text + '</a></li>';

        $("#toc ul").append(element);
    
        // $("#link" + i).css("top", pos);
    });

    var zIndexNumber = 10000;
    $("#toc").css('zIndex', zIndexNumber)
        .attr("title", "this is draggable and resizable");
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

    prettyPrint();
});