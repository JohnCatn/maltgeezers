(function() {
 // Masonry grid setup
 $('.grid').masonry({
  itemSelector: '.grid__item',
  columnWidth: '.grid__sizer',
  gutter: 15,
  percentPosition: true
 });

 // Image replacement handler
 $(document).on('click', '.grid__item', function() {
   $(document).on('click', '.js-heart', function() {
     $(this).toggleClass('active');
  });
 });
})();
