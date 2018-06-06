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
  var imageSrc = $(this).attr('src');

  $('.js-download').attr('href', imageSrc);
  $('.js-modal-image').attr('src', imageSrc);

  $(document).on('click', '.js-heart', function() {
   $(this).toggleClass('active');
  });
 });
})();
