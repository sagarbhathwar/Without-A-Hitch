$(window).scroll(function() {
   if($("#test").offset().top - $(window).scrollTop() <= 100)
  {
    $("#header").css("top", "0");
  }else{
    $("#header").css("top", "20px");
  }
});