// Apply formatting for each article
$(document).ready(function(){  
  $("div.article").each( function(){
   var author = $(this).find("div.author > span").text();
   var articleTitle = $(this).find("div.articleTitle");
   
   if (author.length > 4) {
     articleTitle.append("<br><span class='author'>By " + author + "</span");     
  }
   $(this).find(".articleDesc").remove(); 
  })

// Cover Images
// Set the cover image on the left with the current cover
  var currentCover = $(".s-lib-jqtabs").find("li.active a").attr('href');
  currentCover = $('div' + currentCover).find('img').attr('src');

  // set img src to title div 
$(".journalCover img").attr('src', currentCover)

// This finds the current tab, locates the image, moves it to the proper location, then hides it

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
//  e.target // newly activated tab
//  e.relatedTarget // previous active tab
  var my = $(e.target).attr('href');
  
// get div with my id
var myDiv = $("div" + my);

// find .coverImage
img = $(myDiv).find('.coverImg img').attr('src');
  
// set img src to title div 
$(".journalCover img").attr('src', img)
  
// hide coverImg
//$(".coverImg").hide();

})

})
})
