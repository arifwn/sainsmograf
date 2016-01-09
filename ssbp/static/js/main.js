(function ($) {
  'use strict';

  var root = this;
    if (!root.console) {
    root.console = {
      log: function() {}
    };
  }

  $(function () {

    if ($('.main-nav').data('float') == 'no') {

    }
    else {
      
      // scroll detection
      var position = $(window).scrollTop();
      var $mainNav = $('.main-nav');

      $(window).scroll(function () {
          var scroll = $(window).scrollTop();
          var height = parseInt($mainNav.css('height'));
          var currentPos = 0,
              newPos = 0;

          if (isNaN(height)) {
            return;
          }

          if (scroll > position) {
              // scrolling down
              if ($mainNav.hasClass('main-nav-fixed')) {
                currentPos = parseInt($mainNav.css('top'));
                newPos = currentPos - (scroll - position);
                newPos = newPos < (-height) ? (-height) : newPos;

                $mainNav.css('top', newPos);
              }

          } else {
              // scrolling up
              if ($mainNav.hasClass('main-nav-absolute')) {
                $mainNav.removeClass('main-nav-absolute').addClass('main-nav-fixed').css('top', -height);
              }
              else if ($mainNav.hasClass('main-nav-fixed')) {
                currentPos = parseInt($mainNav.css('top'));
                newPos = currentPos + (position - scroll);
                newPos = newPos > 0 ? 0 : newPos;

                $mainNav.css('top', newPos);
              }
          }

          position = scroll;
          if (position === 0) {
            $mainNav.css('top', 0);
          }
      }); 

    }
  });

}).call(this, jQuery);
