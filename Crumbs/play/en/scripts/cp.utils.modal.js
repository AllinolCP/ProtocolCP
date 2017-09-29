if(typeof CP === 'undefined') {
	CP = {};
}

if(!CP.utils) {
	CP.utils = {};
}

CP.utils.Modal = function(options) {
	// options that can overwritten
	this.options = {
		overlayOpacity: 0.8,
		overlayClickClose: true,
		showClose: true,
		contentCloseDelegate: null,
		centerOnResize: true,
		transitionDuration: 250,
		onOpenComplete: function(){},
		onCloseComplete: function(){},
		onOpenStart: function(){},
		onCloseStart: function(){}
	};
	jQuery.extend(true, this.options, options);
	
	// states
	this.isOpen = false;
	this.isLoading = false;
	
	this.inject();
	this.attach();
};
CP.utils.Modal.prototype.inject = function(){
	// remove before appending
	jQuery('#modal-overlay, #modal-window, #modal-loading').remove();
	// create and embed required elements
	this.overlay = jQuery('<div id="modal-overlay"></div>').appendTo('body');
	this.loading = jQuery('<div id="modal-loading"></div>').appendTo('body');
	this.modal = jQuery('<div id="modal-window"></div>').appendTo('body');
	// optional - close button
	if(this.options.showClose){
		this.closeButton = jQuery('<a class="modal-close" href="#">close</a>').appendTo(this.modal);
	}
	this.modalContent = jQuery('<div id="modal-content"></div>').appendTo(this.modal);
	// set overlay opacity to value in options
	this.overlay.css('opacity', this.options.overlayOpacity);
	this.body = jQuery('body');
};
CP.utils.Modal.prototype.attach = function(){
	var self = this;
	// overlay and loading resize handler
	jQuery(window).resize(function(){
		self.positionOverlay();
		self.centerElement(self.loading);
	});
	
	// optional - content triggered close event
	if(this.options.contentCloseDelegate != null){
		this.modalContent.delegate(this.options.contentCloseDelegate, 'click', function(e){
			e.preventDefault();
			self.close();
		});
	}
	// optional - hide on overlay click
	this.overlay.click(function(e){
		e.stopPropagation();
		
		if(self.options.overlayClickClose){
			self.close();
		}
	});
	
	// optional - close button
	if(this.options.showClose){
		// hide on close button click
		this.closeButton.click(function(e){
			e.preventDefault();
			self.close();
		});
	}
	// optional - window resize handler
	if(this.options.centerOnResize){
		jQuery(window).resize(function(){
			self.centerElement(self.modal);
		});
	}
};
CP.utils.Modal.prototype.centerElement = function(element){
	// usefull dimensions
	var elementWidth = element.width();

	var elementHeight = element.height();
	var windowWidth = jQuery(window).width();
	var windowHeight = jQuery(window).height();
	var scrollTop = jQuery(window).scrollTop();
	// calculate center
	var left = (windowWidth / 2) - (elementWidth / 2);
	var top = scrollTop + ((windowHeight / 2) - (elementHeight / 2));
	// bounding
	if(top < 0 ) top = 0;
	if(left < 0) left = 0;
	// set position
	element.css({
		top: top,
		left: left
	});
}
CP.utils.Modal.prototype.positionOverlay = function(){
	// ie6 alternate overlay size other browsers use css
	if(jQuery.browser.msie && jQuery.browser.version === '6.0'){
		this.overlay.css('height', jQuery(document).height());
	}
};
CP.utils.Modal.prototype.positionModal = function(){
	this.centerElement(this.modal);
};
CP.utils.Modal.prototype.showLoading = function(){
	if(this.isOpen){
		// already open just show loading indicator
		this.modal.fadeOut(this.options.transitionDuration);
		this.loading.fadeIn(this.options.transitionDuration);
	}else{
		// not open yet
		this.overlay.fadeIn(this.options.transitionDuration);
		this.positionOverlay();
		this.loading.fadeIn(this.options.transitionDuration);
		this.centerElement(this.loading);
	}
	this.isLoading = true;
};
CP.utils.Modal.prototype.open = function(modalContent, openCallback, closeCallback){
	var self = this;
	if(!this.isOpen){
		if(this.isLoading){
			// modal is already in loading state just open content
			this.loading.hide();
			this.modalContent.append(modalContent);
			this.modal.fadeIn(this.options.transitionDuration, function() {
				// callbacks
				self.options.onOpenComplete();
				
				if(closeCallback) self.activeCloseCallback = closeCallback;
			});
			this.options.onOpenStart();
			if(openCallback) openCallback();
			this.centerElement(this.modal);
			// update state
			this.isOpen = true;
			this.isLoading = false;
			this.body.addClass('modal-active');
		} else{
			// fresh modal nothing is open yet
			this.overlay.fadeIn(self.options.transitionDuration, function(){
				self.modalContent.append(modalContent);
				self.modal.fadeIn(self.options.transitionDuration, function() {
					// callbacks
					self.options.onOpenComplete();

					if(closeCallback) self.activeCloseCallback = closeCallback;
				});
				self.options.onOpenStart();
				if(openCallback) openCallback();
				self.centerElement(self.modal);
				// update state
				self.isOpen = true;
				self.isLoading = false;
				self.body.addClass('modal-active');
			});
			this.positionOverlay();
		}
	}else{
		// window already open just refresh content
		this.modal.css({visibility: 'hidden'}); ////to support interapp linking, instead of //this.modal.hide();
		this.modalContent.empty();
		this.modalContent.append(modalContent);
		this.options.onOpenStart();
		this.modal.css({visibility: 'visible'}); //to support interapp linking, instead of //this.modal.show();
		this.centerElement(this.modal);
		// update state
		this.isOpen = true;
		this.isLoading = false;
		this.body.addClass('modal-active');
		// callbacks
		this.options.onOpenComplete();
		if(openCallback) openCallback();
		if(closeCallback) this.activeCloseCallback = closeCallback;
	}
};
CP.utils.Modal.prototype.close = function(callback){
	if(this.isOpen){
		var self = this;
		
		//If you are in IE, find all embedded objects and replace them with divs. fadeout doesn't play too nice them
		if(jQuery.browser.msie) {
			var embeddedObjects = self.modalContent.find('object'); //Pro, Swfobject 2.x only uses object element!
			
			embeddedObjects.each(function(index, embObj) {
				embeddedObjects.replaceWith('<div id="' + embeddedObjects.attr('id') + '" />');
			});
		}
		
		// callback
		this.options.onCloseStart();
		
		// hide everything
		this.modal.fadeOut(this.options.transitionDuration, function(){
			self.modalContent.empty();
			self.loading.hide();
			self.overlay.hide();
			
			// update state
			self.isLoading = false;
			self.isOpen = false;
			
			// remove class to body to signify closed modal
			self.body.removeClass('modal-active');
			
			// callbacks
			self.options.onCloseComplete();
			if(callback) callback();
			if(self.activeCloseCallback) {
				self.activeCloseCallback();
				self.activeCloseCallback = null;
			}
		});
	}
};