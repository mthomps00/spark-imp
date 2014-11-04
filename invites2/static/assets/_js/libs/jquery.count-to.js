(function($) {
    $.fn.countTo = function(options) {
        // merge the default plugin settings with the custom options
        options = $.extend({}, $.fn.countTo.defaults, options || {});
		var countLimit = 1000;
		var c = 0;
        // how many times to update the value, and how much to increment the value on each update
        if (options.from == 'cv'){
        	options.from = parseFloat($(this).text().replace('$', '').replace(',','')) * 1;
        }
        var loops = Math.ceil(options.speed / options.refreshInterval),
            increment = (options.to - options.from) / loops;

        return $(this).each(function() {
            var _this = this,
                loopCount = 0,
                value = options.from,
                interval = setInterval(updateTimer, options.refreshInterval);
			
		
            function updateTimer() {
            	c++;
            	if (c > countLimit){
            		return;
            	}
                value += increment;
                loopCount++;
                var nt = value.toFixed(options.decimals);
				if (options.format && options.format != null){
					try {
						nt = $.formatNumber(nt, options.format);
					} catch(e){
						//trace('formatNumber not avaiable');
					}
				}
				if (nt == ''){
					nt = 0;
				}
                $(_this).text(nt);

                if (typeof(options.onUpdate) == 'function') {
                    options.onUpdate.call(_this, value);
                }

                if (loopCount >= loops) {
                    clearInterval(interval);
                    value = options.to;

                    if (typeof(options.onComplete) == 'function') {
                        options.onComplete.call(_this, value);
                    }
                }
            }
        });
    };

    $.fn.countTo.defaults = {
        from: 'cv',  // the number the element should start at
        to: 100,  // the number the element should end at
        speed: 800,  // how long it should take to count between the target numbers
        refreshInterval: 20,  // how often the element should be updated
        decimals: 0,  // the number of decimal places to show
        onUpdate: null,  // callback method for every time the element is updated,
        onComplete: null,  // callback method for when the element finishes updating
        format:null, //number format to use
    };
})(jQuery);