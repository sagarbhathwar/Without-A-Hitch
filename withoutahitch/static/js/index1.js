// makes the parallax elements
function parallaxIt() {
  // create variables
  var $fwindow = $(window);
  var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  var $contents = [];
  var $backgrounds = [];

  // for each of content parallax element
  $('[data-type="content"]').each(function(index, e) {
    var $contentObj = $(this);

    $contentObj.__speed = ($contentObj.data('speed') || 1);
    $contentObj.__fgOffset = $contentObj.offset().top;
    $contents.push($contentObj);
  });

  // for each of background parallax element
  $('[data-type="background"]').each(function() {
    var $backgroundObj = $(this);

    $backgroundObj.__speed = ($backgroundObj.data('speed') || 1);
    $backgroundObj.__fgOffset = $backgroundObj.offset().top;
    $backgrounds.push($backgroundObj);
  });

  // update positions
  $fwindow.on('scroll resize', function() {
    scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    $contents.forEach(function($contentObj) {
      var yPos = $contentObj.__fgOffset - scrollTop / $contentObj.__speed;

      $contentObj.css('top', yPos);
    })

    $backgrounds.forEach(function($backgroundObj) {
      var yPos = -((scrollTop - $backgroundObj.__fgOffset) / $backgroundObj.__speed);

      $backgroundObj.css({
        backgroundPosition: '50% ' + yPos + 'px'
      });
    });
  });

  // triggers winodw scroll for refresh
  $fwindow.trigger('scroll');
};

parallaxIt();