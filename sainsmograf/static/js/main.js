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

      $(window).scroll(function () {
          var scroll = $(window).scrollTop();
          var height = parseInt($('.main-nav').css('height'));
          var currentPos = 0,
              newPos = 0;

          if (isNaN(height)) {
            return;
          }

          if (scroll > position) {
              // scrolling down
              if ($('.main-nav').hasClass('main-nav-fixed')) {
                currentPos = parseInt($('.main-nav').css('top'));
                newPos = currentPos - (scroll - position);
                newPos = newPos < (-height) ? (-height) : newPos;

                $('.main-nav').css('top', newPos);
              }

          } else {
              // scrolling up
              if ($('.main-nav').hasClass('main-nav-absolute')) {
                $('.main-nav').removeClass('main-nav-absolute').addClass('main-nav-fixed').css('top', -height);
              }
              else if ($('.main-nav').hasClass('main-nav-fixed')) {
                currentPos = parseInt($('.main-nav').css('top'));
                newPos = currentPos + (position - scroll);
                newPos = newPos > 0 ? 0 : newPos;

                $('.main-nav').css('top', newPos);
              }
          }

          position = scroll;
      }); 

    }
  });

}).call(this, jQuery);
