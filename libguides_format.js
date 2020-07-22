$(document).ready(function(){
  
  $("div.article").each( function(){
   var author = $(this).find("div.author > span").text();
   var articleTitle = $(this).find("div.articleTitle");
   
   if (author.length > 4) {
     articleTitle.append("<br><span class='author'>By " + author + "</span");
     
  }
   $(this).find(".articleDesc").remove(); 
  })
})
