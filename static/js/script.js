


function showRatings() {
    document.getElementById("ratings").style.display = " block";
    document.getElementById("ratings").style.display = " flex";  
    document.getElementById("reviews").style.display = "none"; 

}

function showReviews() {
    document.getElementById("reviews").style.display = " block";
    document.getElementById("ratings").style.display = "none";


}



var $star_rating = $('.star-rating .fa');

var SetRatingStar = function() {
  return $star_rating.each(function() {
    if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
      return $(this).removeClass('fa-star-o').addClass('fa-star');
    } else {
      return $(this).removeClass('fa-star').addClass('fa-star-o');
    }
  });
};

$star_rating.on('click', function() {
  $star_rating.siblings('input.rating-value').val($(this).data('rating'));
  return SetRatingStar();
});

SetRatingStar();