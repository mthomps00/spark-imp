function setSCFooter(){
	if ($('.mod-inner').hasClass('index')){
		var wt = $(window).scrollTop();
		var ww = $(window).width();
		var limitY = $('.footer-info').offset().top;
		console.log('ww = ' + ww);
		if ((wt > limitY - $(window).height()) && (ww >= 768)) {
			console.log('start')
			var targetY = limitY - $(".footer-scene").outerHeight();
			$('.footer-scene').addClass('footer-scene-end');
			$('.footer-scene').css('top', targetY);
			$('.camp-scene').addClass('camp-scene-end');
			var campSceneY = $('#main-homepage').outerHeight() - $('.camp-scene').outerHeight();
			$('.camp-scene').css('top', campSceneY);
		} else {
			stopFooterAnimation();
		}
	} else {
		stopFooterAnimation();
	}
}

function stopFooterAnimation(){
	$('.footer-scene').removeClass('footer-scene-end');
	$('.camp-scene').removeClass('camp-scene-end');
	$('.footer-scene, .camp-scene').attr('style', '');
}

function stopHeaderAnimation(){
	$('.nav-logo').removeClass('fixed');
}

function setSCHeaderOld(){
	var wt = $(window).scrollTop();
	if (wt > 165 && $('.mod-inner').hasClass('index')){
		$('.nav-logo').addClass('fixed');
	} else {
		stopHeaderAnimation();
	}
}

function setSCHeader(){
	var wt = $(window).scrollTop();
	if (wt > 390 && $('.mod-inner').hasClass('index')){
		$('.nav-logo-img').addClass('down-page');
	} else {
		$('.nav-logo-img').removeClass('down-page');
	}
}

function refreshSCElements(){
	if ($('.mod-inner').hasClass('index') && !$('html').hasClass('oldie')){
		setSCFooter();
		$('.mod-inner').addClass('animateable');
		setSCHeader();
	} else {
		$('.mod-inner').removeClass('animateable');
	}
}

$(document).ready(function(){
	$(window).scroll(refreshSCElements);
	$(window).resize(refreshSCElements);
	$('#mod').pjax('a', {
		fragment:'#mod',
		container:'#mod'
	});
});






















