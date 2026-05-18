// $('body').hide()

$('.view-item_header').click(function(e) {
	e.preventDefault();

	var $row = $(this).closest('li.view-item');
	var $content = $row.find('.view-item_content');

	if ($row.hasClass('active')) {
		$content.slideUp();
		$row.removeClass('active');
	} else {
		$('.faq .view-item.active').removeClass('active').find('.view-item_content').slideUp();
		$row.addClass('active');
		$content.slideDown();
	}
});

if (document.querySelector('.s-reviews .swiper')) {
	const swiper1 = new Swiper('.s-reviews .swiper', {
		speed: 500,
		navigation: {
			nextEl: '.r-next',
			prevEl: '.r-prev',
		},
		breakpoints: {
			1080: {
				slidesPerView: 3,
				spaceBetween: 32,
			},
			820: {
				slidesPerView: 2,
				spaceBetween: 24,
			},
			768: {
				slidesPerView: 3,
				spaceBetween: 24,
			},
			420: {
				slidesPerView: 1.4,
				spaceBetween: 16,
			},
			320: {
				slidesPerView: 1,
				spaceBetween: 16,
			}
		},
	});
}

Fancybox.bind("[data-fancybox]", {
  // Your custom options
});

// "Скачать" dropdown toggle
$(document).on('click', '.download_btn', function(e) {
	e.preventDefault();
	e.stopPropagation();
	var $row = $(this).closest('.report-row');
	$('.report-row.open').not($row).removeClass('open');
	$row.toggleClass('open');
});

$(document).on('click', function(e) {
	if (!$(e.target).closest('.download_wrap').length) {
		$('.report-row.open').removeClass('open');
	}
});


document.addEventListener('DOMContentLoaded', () => {
  const element = document.getElementById('scroll-box1');
  if (element) {
    new SimpleBar(document.getElementById('scroll-box1'));
  }
	const element2 = document.getElementById('scroll-box2');
  if (element2) {
    new SimpleBar(document.getElementById('scroll-box2'));
  }
	const element3 = document.getElementById('scroll-box3');
  if (element3) {
    new SimpleBar(document.getElementById('scroll-box3'));
  }
});