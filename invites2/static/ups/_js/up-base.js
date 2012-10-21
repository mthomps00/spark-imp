// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console) {
    arguments.callee = arguments.callee.caller;
    var newarr = [].slice.call(arguments);
    (typeof console.log === 'object' ? log.apply.call(console.log, console, newarr) : console.log.apply(console, newarr));
  }
};

// make it safe to use console.log always
(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();){b[a]=b[a]||c}})((function(){try
{console.log();return window.console;}catch(err){return window.console={};}})());


// place any jQuery/helper plugins in here, instead of separate, slower script files.



$(document).ready(function() {
	// Add objects that should automatically receive a "first" or "last" class
	
	function initClassFixing(){
		var first_last = new Array('table tr', 'table td', 'dl dt', 'ul li', '.table_container .table_default');
	
		for (var i=0; i<first_last.length; i++){
			var f = first_last[i];
			$(f+":first-child").addClass("first");
			$(f+":last-child").addClass("last");
		}
	
		$("table tr:odd").addClass("odd");
	}
	
	function initTabs(){
		/* Bind tabbing action from all uls with a class of 'tabs' to all divs
		/  with a class of '.pane' that share the same container div */
		try {
			$("ul.tabs").tabs("> .pane",{
				current:'active'
			});	
		
			// Bind tabbing action from all uls with a class of 'pills' to all divs
			// with a class of '.pane' that share the same container div
			$("ul.pills").tabs("> .pane",{
				current:'active'
			});	
		} catch(e){
			trace('Error loading tabs ' + e);
		}
	}
	
	function initDropDowns(){
		// Set dropdowns on click
		$(document.body).delegate(".dropdown-trigger", "click", function() {
			var t = $(this).closest(".dropdown");
			t.toggleClass("dropdown-active");
		});
		
		// Set dropdowns on hover
		$(document.body).delegate(".dropdown-trigger-hover", "mouseenter mouseleave", function() {
			var t = $(this).closest(".dropdown");
			t.toggleClass("dropdown-active");
		});
	}

	function initToolTips(){
    	// Show tooltips on hover
		$(document.body).delegate(".tip-trigger", "mouseenter mouseleave", function() {
			$(this).toggleClass("tip-active");
		});

		// Show popovers on hover
		$(document.body).delegate(".pop-trigger", "mouseenter mouseleave", function() {
			$(this).toggleClass("pop-active");
  		});
  	}

	function initModals(){
		// Apply modal action to anything with ID of "modal"
		// Launch when user clicks any object with a class of "modal-trigger"
		$('.modal-trigger').click(function(){
				$('.modal').modal();
			});
		// Create a close button for the modal, dismiss modal by clicking the background
		$('.close-modal, .simplemodal-overlay').live('click', function(){
			$.modal.close();
		});
		if ($.modal){
			// Don't let opacity be set by the plugin
			$.modal.defaults.opacity = 'inherit';
			// Add a class to overlay and container when the modal is shown
			$.modal.defaults.onShow = function(){
				$('.simplemodal-overlay').addClass('overlay-active');
				$('.simplemodal-container').addClass('modal-active');
			}
		}
	}

  	initClassFixing();
  	initTabs();
  	initDropDowns();
  	initToolTips();
  	initModals();
  	
}); /* end jQuery functions */

/* Universal Functions */

function trace(msg){
	try{console.log(msg);} catch(e){}
}

Array.prototype.getRandom = function(){
	var r = Math.floor(Math.random() * this.length);
	return this[r];
}

Array.prototype.getLast = function(){
	var l = this.length - 1;
	return this[l];
}

Array.prototype.remove = function(removeMe){
	var index = this.indexOf(removeMe);
	if (index > -1){
		this.splice(index, 1);
	}
	return this;
}

Array.prototype.fill = function(size, oneBased){
	for (var i = 0; i<size; i++){
		var j = i;
		if (oneBased){
			j = i + 1;
		}
		this.push(j);
	}
	return this;
}