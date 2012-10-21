$(document).ready(function() {

	$(".style-example").each(function(){
		var html = $(this).html();
		html = html.replace(/</g, "&lt;");
		html = html.replace(/>/g, "&gt;");
		html = html.trim();
		$(this).parents('.style-node').find('.code-snip').find('code').html(html);
	}); 
	
	$("ul.style-tabs").tabs(".style-panes > .style-pane",{
		current:'active'
	});	

});