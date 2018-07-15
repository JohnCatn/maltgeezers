$('#modalReview').on('show.bs.modal', function(event) {
  //hide the footer as we'll reload the share buttons
  $('.modal-footer').hide()
  var button = $(event.relatedTarget) // Button that triggered the modal
  var review_id = button.data('id') // Extract info from data-* attributes
  var modal = $(this);
  $.ajax({
    type: "GET",
    url: get_reviews_url + review_id,
    data: '',
    cache: false,
    success: function(data) {
      console.log(data);

      $('.modal-title').html(data.name);
      $('#distillery').html(data.distillery);
      $('#notes').html(data.notes);
      $('#tasting_notes').html(data.tasting_notes);
      $('#max_rating').html(data.max_rating);
      $('#avg_rating').html(data.avg_rating);
      $('#min_rating').html(data.min_rating);
      $('#tasting_date').html(data.tasting.date);
      if (data.age == 0) {
        $('.age').hide();
      } else {
        $('#age').html(data.age);
      }
      $('.js-modal-image').attr('src', data.img_url);
      $('.fb-share-button').attr('data-href', data._links.review)
      $('.twitter-share-button').attr('data-url', data._links.review)
      $('.twitter-share-button').attr('data-hashtags', 'whisky, ' + data.distillery)
      $('.twitter-share-button').attr('data-text', 'Checkout the Maltgeezers review for ' + data.title)
      //reload facebook controls
      // Facebook
      var f = $('<div class="fb-share-button" data-layout="button" data-size="small" data-mobile-iframe="true">');
      $(f).attr('data-href', data._links.review);
      $('#fbholder').empty();
      $(f).appendTo($('#fbholder'));
      FB.XFBML.parse(document);
      // Update the twitter share
      // Remove the iframe
      $('#SocialTwitter iframe').remove();

      // Generate new markup
      $('<a>', {
        class: 'twitter-share-button',
        id: 'tweet_btn',
        href: 'http://twitter.com/intent/tweet',
        'data-url': data._links.review,
        'data-hashtags': 'whisky, ' + data.distillery,
        'data-text': 'Checkout the Maltgeezers review for ' + data.distillery + ' '  + data.name
      }).appendTo('#SocialTwitter');


      // Reload the widget
      //twttr.widgets.load();
      $.when( twttr.widgets.load() ).done(function() {
             $('.modal-footer').show()
      });
      //$('.modal-footer').show()


    },
    error: function(err) {
      console.log(err);
    }
  });
})
