// Parallax Image
// Author: Arif Widi Nugroho <arif@sainsmograf.com>

/*
 usage:
  <div class="parallax full-width" style="height: {{ viewport height }};">
    <img src="{{ image_url }}" alt="">
  </div>
*/

(function ($) {
  var root = this;
  var parallaxUtils = root.parallaxUtils = {};

  parallaxUtils.parallaxWindows = {};
  parallaxUtils.parallaxImages = {};
  parallaxUtils.idCount = 0;

  parallaxUtils.windowResize = function(target) {
    var $target = $(target);
    var aspectRatio = $target.data('aspect-ratio');

    if (aspectRatio !== void 0) {
      var parallaxWindowWidth = $target.width();
      var computedHeight = parallaxWindowWidth / aspectRatio;

      if (computedHeight) {
        $target.css('height', computedHeight);
      }
    }
  };

  parallaxUtils.parallax = function (target) {
    parallaxUtils.parallaxWindows[target] = $(target);
    parallaxUtils.parallaxImages[target] = parallaxUtils.parallaxWindows[target].find('img');

    var aspectRatio = parallaxUtils.parallaxWindows[target].data('aspect-ratio');

    if (aspectRatio !== void 0) {
      var parallaxWindowWidth = parallaxUtils.parallaxWindows[target].width();
      var computedHeight = parallaxWindowWidth / aspectRatio;

      if (computedHeight) {
        parallaxUtils.parallaxWindows[target].css('height', computedHeight);
      }
    }

    $(window).on('scroll', function (e) {
      var parallaxWindow = parallaxUtils.parallaxWindows[target];
      var parallaxImage = parallaxUtils.parallaxImages[target];
      var parallaxOffset = parallaxImage.height() - parallaxWindow.height();
      var parallaxWindowTopPosition = parallaxWindow.offset().top;
      var parallaxWindowHeight = parallaxWindow.height();
      var windowTopPosition = $(window).scrollTop();
      var windowHeight = $(window).height();

      if (((windowTopPosition - (parallaxWindowTopPosition + parallaxWindowHeight)) > 0) || ((parallaxWindowTopPosition - (windowTopPosition + windowHeight)) > 0) ) {
        return;
      }

      var offset = ((windowTopPosition - (parallaxWindowTopPosition + parallaxWindowHeight)) / (parallaxWindowHeight + windowHeight)) * parallaxOffset;
      parallaxImage.css('top', offset);
    });

    parallaxUtils.parallaxImages[target].load(function () {
      $(window).scroll();
    });
    $(window).scroll();
  };

  parallaxUtils.init = function () {
    var elements = $('.parallax');
    for (var i = 0; i < elements.length; i++) {
      var targetElement = elements[i];
      parallaxUtils.idCount += 1;
      var generatedID = 'parallax_' + parallaxUtils.idCount;
      $(targetElement).attr('id', generatedID);
      parallaxUtils.parallax('#' + generatedID);
    };

    $(window).on('resize', function(e) {
      var elements = $('.parallax');
      for (var i = 0; i < elements.length; i++) {
        var targetElement = elements[i];
        parallaxUtils.windowResize(targetElement);
      };
    });
  };

  $(function () {
    if ($('body').data('use-paralax')) {
      parallaxUtils.init();
    }
  });

}).call(this, jQuery);
